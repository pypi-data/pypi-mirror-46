# -*- coding: utf-8 -*-

"""Utility methods that are used across the frkl-suite (https://frkl.io) of tools."""

import copy
import json
import logging
import pprint
import re
import subprocess  # nosec
from collections import Mapping, OrderedDict, Sequence
from distutils.spawn import find_executable

import jinja2
import toml
from dogpile.cache import make_region, register_backend
from dogpile.cache.api import NO_VALUE, CacheBackend
from jinja2 import Environment, TemplateSyntaxError, Undefined, meta
from ruamel import yaml as ruamel_yaml
from ruamel.yaml import YAML, RoundTripRepresenter
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.compat import StringIO
from six import string_types

from .defaults import *  # noqa

log = logging.getLogger("frutils")

yaml = YAML()

DEFAULT_ENV = Environment(autoescape=True)


# utility methods/classes
# =======================


class StringYAML(YAML):
    """Wraps :class:~YAML to be able to dump a string from a yaml object.

    More details: http://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string

    Args:
        **kwargs (dict): arguments for the underlying :class:~YAML class
    """

    def __init__(self, **kwargs):
        super(StringYAML, self).__init__(**kwargs)

    def dump(self, data, stream=None, split_multiline_strings=True, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        if split_multiline_strings:
            ruamel_yaml.scalarstring.walk_tree(data)

        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


DEFAULT_STRING_YAML = StringYAML()
DEFAULT_STRING_YAML.default_flow_style = True


def ordered_load(text):
    """Loads a yaml stream into an OrderedDict

    """
    return yaml.load(text)  # nosec


def special_dict_to_dict(value):
    """Converts any 'special' dict (like CommentedMap, OrderedDict) to a 'normal' one.

    Args:
        value (dict): the 'special' dict
    Returns:
        dict: the 'normal' dict
    """

    if isinstance(value, (list, tuple, CommentedSeq)):
        result = []
        for v in value:
            result.append(special_dict_to_dict(v))
    elif isinstance(value, (dict, CommentedMap, OrderedDict)):
        result = {}
        for key, value in value.items():
            if isinstance(value, (dict, OrderedDict, CommentedMap)):
                result[key] = special_dict_to_dict(value)
            elif isinstance(value, (list, tuple, CommentedSeq)):
                result[key] = special_dict_to_dict(value)
            else:
                result[key] = value

        return result
    else:
        result = value

    return result


def list_of_special_dicts_to_list_of_dicts(value):

    result = []
    for sd in value:
        result.append(special_dict_to_dict(sd))

    return result


def is_sequence(obj):
    """Checks whether an object is a list-type thing, but not a string.

    Args:
        obj: the object in question

    Returns:
        bool: whether the object is a sequence-type but not string

    """

    return isinstance(obj, Sequence) and not isinstance(obj, string_types)


def is_list_of_strings(input_obj):
    """Helper method to determine whether an object is a list or tuple of only strings (or string_types).

    Args:
      input_obj (object): the object in question

    Returns:
      bool: whether or not the object is a list of strings
    """

    return (
        bool(input_obj)
        and isinstance(input_obj, (list, tuple, CommentedSeq))
        and not isinstance(input_obj, string_types)
        and all(isinstance(item, string_types) for item in input_obj)
    )


def dict_merge(dct, merge_dct, copy_dct=True):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    Copied from: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

    Args:
      dct (dict): dict onto which the merge is executed
      merge_dct (dict): dct merged into dct
      copy_dct (bool): whether to (deep-)copy dct before merging (and leaving it unchanged), or not (default: copy)

    Returns:
      dict: the merged dict (original or copied)
    """

    if copy_dct:
        dct = copy.deepcopy(dct)

    for k, v in merge_dct.items():
        if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], Mapping):
            dict_merge(dct[k], merge_dct[k], copy_dct=False)
        else:
            dct[k] = merge_dct[k]

    return dct


def merge_list_of_dicts(dicts, starting_dict=None):
    """Merges a list of dicts.

    Args:
      dicts (list): list of dicts to be merged in order
      starting_dict (dict): (optional) existing dict where the others are merged into

    Returns:
      dict: the merged dict (same as starting_dict)
    """

    if starting_dict is None:
        starting_dict = {}
    for d in dicts:
        dict_merge(starting_dict, d, copy_dct=False)

    return starting_dict


def is_url_or_abbrev(url, abbrevs=DEFAULT_URL_ABBREVIATIONS_FILE):

    if url.startswith("http://") or url.startswith("https://"):
        return True
    for key in abbrevs.keys():
        if url.startswith("{}:".format(key)):
            return True

    return False


def get_key_path_value(source_dict, key_path, split_token=".", default_value=None):
    """Queries the source dict tree for the register key, split up using the split_token.

    Args:
      source_dict (dict): the source dictionary
      key_path (str): a key-path, e.g. 'key1.child_key1.test_key'
      split_token (str): the character to split the register_key value with
      default_value: the default value to return if no key matches

    Return:
      object: the value for the matching in the tree, or None
    """

    temp_dict = source_dict
    tokens = key_path.split(split_token)

    for key in tokens[0:-1]:

        temp_dict = temp_dict.get(key, None)
        if temp_dict is None:
            return default_value
        elif not isinstance(temp_dict, dict):
            return default_value

    return temp_dict.get(tokens[-1], default_value)


def add_key_to_dict(target_dict, key_path, value, split_token=".", ordered=True):
    """Add a key into the key path of a dictionary.

    Args:
      target_dict (dict): the dictionary to add to
      key_path (str): the path to the value (e.g. key1.child_key.test)
      value: the value to insert
      split_token (str): the character to split the key_path with.
      ordered (bool): whether to use OrderedDicts instead of 'normal' ones
    """

    log.debug("Adding value '{}' as key '{}' to dict.".format(value, key_path))
    if ordered:
        temp_dict = OrderedDict()
    else:
        temp_dict = {}

    orig_temp_dict = temp_dict

    tokens = key_path.split(split_token)

    for key in tokens[0:-1]:
        if ordered:
            temp_dict.setdefault(key, OrderedDict())
        else:
            temp_dict.setdefault(key, {})
        temp_dict = temp_dict[key]

    temp_dict[tokens[-1]] = value
    dict_merge(target_dict, orig_temp_dict, copy_dct=False)


def append_key_to_dict(target_dict, key_path, value, split_token="."):
    """Appends a key into the key path of a dictionary.

    The value either needs to be a list or tuple, or nonexistent. If this is not the case, this function will throw an exception.

    Args:
      target_dict (dict): the dictionary to add to
      key_path (str): the path to the value (e.g. key1.child_key.test)
      value: the value to append
      split_token (str): the character to split the key_path with.
    """

    log.debug("Adding value '{}' as key '{}' to dict.".format(value, key_path))

    temp_dict = copy.deepcopy(target_dict)
    orig_temp_dict = temp_dict

    tokens = key_path.split(split_token)

    for key in tokens[0:-1]:
        temp_dict.setdefault(key, {})
        temp_dict = temp_dict[key]

    old_value = temp_dict.get(tokens[-1], None)
    if old_value is None:
        temp_dict[tokens[-1]] = [value]
    elif isinstance(old_value, (list, tuple)):
        old_value.append(value)
    else:
        raise Exception(
            "Value for key_path '{}' is not a list or tuple, can't append.".format(
                key_path
            )
        )

    dict_merge(target_dict, orig_temp_dict, copy_dct=False)


def flatten_lists(lists):
    """Utility method to flatten a list of lists.

    This will only flatten the first sublist, any deeper list-structure will be preserved.

    Args:
      lists (list): a list of lists
    Returns:
      list: the flattened list
    """
    result = [item for sublist in lists for item in sublist]
    return result


def string_is_templated(text, jinja_env):
    """Utility method to determine whether a string has template markers in it.

    This is pretty simplistic, it only checks whether one of the template marker strings
    (e.g. '}}', or '{%') are contained in the text. It doesn't check for matching opening/
    closed brackets etc.

    Args:
      text (str): the text in question
      jinja_env (Environment): the jinja environment
    Returns:
      bool: whether the text is templated or not
    """

    if not isinstance(text, string_types):
        return False

    block_start_string = jinja_env.block_start_string
    if block_start_string in text:
        return True
    variable_start_string = jinja_env.variable_start_string
    if variable_start_string in text:
        return True

    # don't really need those
    # block_end_string = jinja_env.block_end_string
    # variable_end_string = jinja_env.variable_end_string

    return False


def get_template_keys(
    data, init_keys=None, ignore_unknown_types=True, jinja_env=None, keep_omit=False
):
    """Gets a list of used template keys in all keys/values of a python object.

    Args:
        data: the input
        init_keys (set): initial set of keys
        ignore_unknown_types (bool): whether to ignore unknown types
        jinja_env (dict): the delimiter profile
        keep_omit (bool): whether to keep the 'omit' keyword

    Returns:
        set: a set of template keys
    """
    if init_keys is None:
        init_keys = set()

    if isinstance(data, string_types):
        keys = get_template_keys_from_string(data, jinja_env=jinja_env)
        init_keys.update(keys)
        if keep_omit and "omit" in init_keys:
            init_keys.remove("omit")
        return init_keys
    elif isinstance(data, (list, tuple, CommentedSeq)):
        for d in data:
            get_template_keys(
                d,
                init_keys=init_keys,
                ignore_unknown_types=ignore_unknown_types,
                jinja_env=jinja_env,
            )
        if keep_omit and "omit" in init_keys:
            init_keys.remove("omit")
        return init_keys
    elif isinstance(data, (dict, CommentedMap, OrderedDict)):
        for k, v in data.items():
            get_template_keys(
                k,
                init_keys=init_keys,
                ignore_unknown_types=ignore_unknown_types,
                jinja_env=jinja_env,
            )
            get_template_keys(
                v,
                init_keys=init_keys,
                ignore_unknown_types=ignore_unknown_types,
                jinja_env=jinja_env,
            )
        if keep_omit and "omit" in init_keys:
            init_keys.remove("omit")
        return init_keys
    else:
        if ignore_unknown_types:
            if keep_omit and "omit" in init_keys:
                init_keys.remove("omit")
            return init_keys
        else:
            raise Exception("Can't get template keys from type '{}'".format(type(data)))


class DictionaryBackend(CacheBackend):
    def __init__(self, arguments):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, NO_VALUE)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        self.cache.pop(key)


register_backend("dictionary", "frutils.frutils", "DictionaryBackend")


def key_func(namespace, fn, **kw):

    if fn.__name__ == "get_template_keys_from_string":

        def generate_key(*arg):
            if not isinstance(arg[0], string_types) or not string_is_templated(
                arg[0], jinja_env=arg[1]
            ):
                key = "NO_TEMPLATE"
            else:
                key = arg[0]

            return key

        return generate_key

    else:
        raise Exception("Invalid cache target function")


region = make_region(name="template_keys", function_key_generator=key_func)
region.configure("dictionary")


@region.cache_on_arguments()
def get_template_keys_from_string(text, jinja_env=None):
    """Retrieves all template keys that are contained in a string.

    Args:
      text (str): the text in question
      jinja_delimiter_profile (dict): the delimiter profile
    Returns:
      list: a list of strings
    """
    # print("XXX")
    # import traceback
    # traceback.print_stack()

    if not isinstance(text, string_types) or not string_is_templated(
        text, jinja_env=jinja_env
    ):
        return []

    if jinja_env is None:
        jinja_env = DEFAULT_ENV

    try:
        ast = jinja_env.parse(text)
        result = meta.find_undeclared_variables(ast)

        return result
    except (TemplateSyntaxError) as e:
        log.debug(str(e.__dict__))
        raise e


class IgnoreUndefinedJinjaVariable(Undefined):
    def __fail__with_undefined_error(self, *args, **kwargs):

        log.debug("Missing jinja var")
        return None


def simple_replace_string_in_obj(obj, key, repl):
    """Replaces string in object recursively, non-jinja-termplate version.

    Args:
        obj: the object
        key: the string to be replaced
        repl: the replacement string

    Returns:
        tuple: the replaced object, and a boolean that indicates whether there was any change or not
    """

    changed_global = False
    if isinstance(obj, Mapping):
        result = CommentedMap()
        for k, v in obj.items():
            repl_value, changed = simple_replace_string_in_obj(v, key=key, repl=repl)
            if changed:
                changed_global = True
            result[k] = repl_value
    elif isinstance(obj, (list, tuple, CommentedSeq)):
        result = []
        for v in obj:
            repl_value, changed = simple_replace_string_in_obj(v, key=key, repl=repl)
            if changed:
                changed_global = True
            result.append(repl_value)
    elif isinstance(obj, string_types):
        if key in obj:
            changed_global = True
            result = obj.replace(key, repl)
        else:
            result = obj
    else:
        result = obj

    return result, changed_global


def replace_string(
    template_string,
    replacement_dict=None,
    jinja_env=None,
    # block_start_string=DEFAULT_BLOCK_START_STRING,
    # block_end_string=DEFAULT_BLOCK_END_STRING,
    # variable_start_string=DEFAULT_VARIABLE_START_STRING,
    # variable_end_string=DEFAULT_VARIABLE_END_STRING,
    # additional_jinja_extensions=None,
    local_env_vars_key=False,
    # local_env_vars_key=DEFAULT_LOCAL_ENV_VARS_KEY,
    # ignore_undefined=False,
):
    """Replace template markers with values from a replacement dictionary within a string.

    Args:
      template_string (str): the template string
      replacement_dict (dict): the dictionary with the replacement strings
      jinja_env: an existing jinja env to use, if specified, the following paramters will be ignored
      # block_start_string (str): the string to indicate a template block start
      # block_end_string (str): the string to indicate a template block end
      # variable_start_string (str): the string to indicate a template variable start
      # variable_end_string (str): the string to indicate a template variable end
      # additional_jinja_extensions (list): a list of jinja extensions to use
      local_env_vars_key (str): the key to use under which to put local environment variables
      # ignore_undefined (bool): whether to skip replacement when encountering undefined variables (True), or error out (False)
    """

    # if additional_jinja_extensions is None:
    #     additional_jinja_extensions = []
    if replacement_dict is None:
        replacement_dict = {}

    if local_env_vars_key:
        sub_dict = copy.deepcopy({local_env_vars_key: os.environ})

        dict_merge(sub_dict, replacement_dict, copy_dct=False)

    else:
        sub_dict = replacement_dict

    match = False

    if jinja_env is not None:
        env = jinja_env
    else:
        raise Exception("No environment provided.")

    if not string_is_templated(template_string, env):
        return template_string

    for k, v in sub_dict.items():
        match = "{} {} {}".format(env.variable_start_string, k, env.variable_end_string)
        if template_string == match:
            return v

    if isinstance(template_string, jinja2.runtime.Undefined):
        return ""

    result = env.from_string(template_string).render(sub_dict)

    if isinstance(result, jinja2.runtime.Undefined):
        result = ""
    return result


def replace_strings_in_obj(
    source_obj,
    replacement_dict=None,
    jinja_env=None,
    local_env_vars_key=False,
    # local_env_vars_key=DEFAULT_LOCAL_ENV_VARS_KEY,
):
    """Replace keys/values with template values within an object.

    strings, dicts and lists are supported (for now), everything else is ignored.

    Args:
      source_obj (object): the source object containing the strings to replace
      replacement_dict (dict): the dictionary with the replacement strings
      jinja_env: an existing jinja env, if specified, the following parameters will be ignored
      local_env_vars_key (str): the key to use under which to put local environment variables
    """

    if isinstance(source_obj, (dict, OrderedDict, CommentedMap)):
        # dictionary
        dict_class = source_obj.__class__
        ret = dict_class()
        for k, v in source_obj.items():
            ret[
                replace_strings_in_obj(
                    k,
                    replacement_dict,
                    jinja_env=jinja_env,
                    local_env_vars_key=local_env_vars_key,
                )
            ] = replace_strings_in_obj(
                v,
                replacement_dict,
                jinja_env=jinja_env,
                local_env_vars_key=local_env_vars_key,
            )
        return ret
    elif isinstance(source_obj, string_types):

        # string
        result = replace_string(
            source_obj,
            replacement_dict,
            jinja_env=jinja_env,
            local_env_vars_key=local_env_vars_key,
        )

        if not string_is_templated(source_obj, jinja_env):
            return source_obj
        return result
    elif isinstance(source_obj, (list, tuple, CommentedSeq)):
        # list (or the like)
        ret = []
        for item in source_obj:
            ret.append(
                replace_strings_in_obj(
                    item,
                    replacement_dict,
                    jinja_env=jinja_env,
                    local_env_vars_key=local_env_vars_key,
                )
            )
        return ret
    else:
        # anything else
        return source_obj


def reindent(s, numSpaces, keep_current=True, line_nrs=False):
    """Reindents a string.

    Args:
        s (str): the string
        numSpaces (int): the indent
        keep_current (bool): keep a potential current indention and add to it
    Returns:
        str: the indented string
    """

    # s = string.split(s, '\n')
    s = s.split("\n")
    if keep_current:
        s = [(numSpaces * " ") + line for line in s]
    else:
        s = [(numSpaces * " ") + line.lstrip() for line in s]

    if line_nrs is not False:
        if isinstance(line_nrs, int):
            begin = line_nrs
        else:
            begin = 0

        temp = []
        for index, line in enumerate(s):
            temp.append("{:3d} {}".format(index + begin, line))

        s = temp

    s = "\n".join(s)

    return s


class IgnoreAliasRepresenter(RoundTripRepresenter):
    def __init__(self, default_style=None, default_flow_style=None, dumper=None):

        super(IgnoreAliasRepresenter, self).__init__(
            default_style=default_style,
            default_flow_style=default_flow_style,
            dumper=dumper,
        )

    def ignore_aliases(self, data):
        return True


def readable(
    python_object,
    out="raw",
    safe=False,
    indent=0,
    sort_keys=False,
    ignore_aliases=False,
):
    """Utility method to print out readable strings from python objects (mostly dicts).

    Args:
        python_object (obj): the object to print
        out (str): the format of the output (available: 'yaml', 'json', 'raw', and 'pformat')
        safe (bool): whether to use a 'safe' way of converting to string (if available in the output format type)
        indent (int): the indentation (optional)
        sort_keys (boolean): whether to sort a (root-level) dictionary (only works for YAML so far)
    """

    if out is None:
        out = "raw"

    if out == "yaml":
        if isinstance(python_object, OrderedDict) or (
            sort_keys and isinstance(python_object, Mapping)
        ):
            temp = CommentedMap()
            if sort_keys:
                for k in sorted(python_object):
                    temp[k] = python_object[k]
            else:
                for k in python_object:
                    temp[k] = python_object[k]
        else:
            temp = python_object

        if safe:
            ryaml = StringYAML(typ="safe")
            ryaml.default_flow_style = False
            output_string = ryaml.dump(temp)
            # output_string = yaml.safe_dump(
            # python_object,
            # default_flow_style=False,
            # encoding='utf-8',
            # allow_unicode=True)
        else:
            ryaml = StringYAML()
            if ignore_aliases:
                ryaml.Representer = IgnoreAliasRepresenter
            ryaml.default_flow_style = False
            output_string = ryaml.dump(temp)

            # output_string = yaml.dump(
            # python_object,
            # default_flow_style=False,
            # encoding='utf-8',
            # allow_unicode=True)
    elif out == "json":
        output_string = json.dumps(python_object, sort_keys=4, indent=4)
    elif out == "raw":
        output_string = str(python_object)
    elif out == "pformat":
        output_string = pprint.pformat(python_object)
    else:
        raise Exception(
            "No valid output format provided. Supported: 'yaml', 'json', 'raw', 'pformat'"
        )

    if indent != 0:
        output_string = reindent(output_string, indent)

    return output_string


def readable_raw(python_object, indent=0):
    """Shortcut for using the :func:`readable` method with the 'raw' format."""

    return readable(python_object, out="raw", indent=indent)


def readable_json(python_object, indent=0):
    """Shortcut for using the :func:`readable` method with the 'json' format."""

    return readable(python_object, out="json", indent=indent)


def readable_yaml(
    python_object, indent=0, safe=False, sort_keys=False, ignore_aliases=False
):
    """Shortcut for using the :func:`readable` method with the 'yaml' format."""

    result = readable(
        python_object,
        out="yaml",
        indent=indent,
        safe=safe,
        sort_keys=sort_keys,
        ignore_aliases=ignore_aliases,
    )
    return result


def readable_pformat(python_object, indent=0):
    """Shortcut for using the :func:`readable` method with the 'pformat' format."""

    return readable(python_object, out="pformat", indent=indent)


def ensure_parent_dir(path):
    """Makes sure a parent directory exists.

    Args:
        path: the path to a file

    Returns:
        str: the parent dir
    """

    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    elif not os.path.isdir(os.path.realpath(parent)):
        raise Exception(
            "Can't create parent dir, file already exists: {}".format(parent)
        )

    return parent


def calculate_cache_location_for_url(url, postfix=None):
    """Utility method to get a unique path that can be used for caching a download."""

    REPL_CHARS = "[^_\\-A-Za-z0-9.]+"
    if postfix is not None:
        temp = os.path.join(url, postfix)
    else:
        temp = url
    path = re.sub(REPL_CHARS, os.sep, temp)
    return path


def can_passwordless_sudo():
    """Checks if the user can use passwordless sudo on this host."""

    if os.geteuid() == 0:
        return True

    sudo_exe_available = find_executable("sudo")
    if not sudo_exe_available:
        return False

    FNULL = open(os.devnull, "w")
    # use -k to ignore any existing sudo token
    p = subprocess.Popen(
        "sudo -k -n true",
        shell=True,  # nosec
        stdout=FNULL,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )
    r = p.wait()
    return r == 0


def get_git_auto_dest_name(repo, parent_dir="~"):
    """Extracts the package/repo name out of a git repo and returns the suggested path where the local copy should live

     Args:
       repo (str): the repo url
       parent_dir (str): the parent path to where the local repo will live

     Returns:
       str: the full path to the local repo
     """

    temp = "{}{}{}".format(parent_dir, os.path.sep, repo.split("/")[-1])

    if temp.endswith(".git"):
        temp = temp[0:-4]

    return temp


def ensure_git_repo_format(repo, dest=None, dest_is_parent=False):
    """Makes sure that the repo is in the format nsbl needs for git repos.

     This format is a dictionary with "repo" and "dest" keys. If only a url is provided,
     the repo name will be calculated using 'get_git_auto_dest_name'.

     Args:
       repo (str, dict): the repository
       dest (str): the (optional) local destination of the repo
       dest_is_parent (bool): whether the provided destination is the parent folder (True), or the full path (False)
     Returns:
       dict: full information for this repo
     """

    if isinstance(repo, string_types):
        if dest:
            if dest_is_parent:
                dest_full = get_git_auto_dest_name(repo, dest)
                return {"repo": repo, "dest": dest_full}
            else:
                return {"repo": repo, "dest": dest}
        else:
            return {"repo": repo, "dest": get_git_auto_dest_name(repo)}
    elif isinstance(repo, dict):
        if "repo" not in repo.keys():
            raise Exception(
                "Repo dictionary needs at least a 'repo' key: {}".format(repo)
            )
        if "dest" not in repo.keys():
            if dest:
                if dest_is_parent:
                    dest_full = get_git_auto_dest_name(repo["repo"], dest)
                    repo["dest"] = dest_full
                else:
                    repo["dest"] = dest
            else:
                repo["dest"] = get_git_auto_dest_name(repo["repo"])
        return repo
    else:
        raise Exception(
            "Repo value needs to be either string or dict format: {}".format(repo)
        )


def generate_custom_abbrevs(abbrevs, default_abbrevs=DEFAULT_URL_ABBREVIATIONS_FILE):
    """Generates abbreviations based on the default abbrevs, overlaying extra ones.

    Args:
        abbrevs (dict, list): list or dict of abbreviations
        default_abbrevs (dict): the base abbrevs

    Return:
        dict: merged abbrevs
        """

    if not isinstance(abbrevs, (list, dict)):
        abbrevs = [abbrevs]

    result = copy.deepcopy(default_abbrevs)
    for a in abbrevs:
        dict_merge(result, abbrevs, copy_dct=False)

    return result


def parse_ssh_config_string(config_string):

    host = None
    port = None
    user = None
    ssh_key = None

    for line in config_string.split("\n"):

        line = line.strip()

        if line.startswith("HostName "):
            host = line.split()[1]
        elif line.startswith("User "):
            user = line.split()[1]
        elif line.startswith("Port "):
            port = int(line.split()[1])
        elif line.startswith("IdentityFile "):
            ssh_key = line.split()[1]

    result = {}
    if host:
        result["host"] = host
    if user:
        result["user"] = user
    if port:
        result["port"] = port
    if ssh_key:
        result["ssh_key"] = ssh_key

    return result


def parse_host_string(host_string):
    """Parse a string to get user, protocol, host, etc.

    Args:
        host_string (str): the string
    Returns:
        dict: a dict containing the differnt parts
    """

    if not host_string:
        return {}

    username = None
    protocol = None
    host = None
    port = None

    if "://" in host_string:
        protocol, host = host_string.split("://")
    else:
        host = host_string

    if "@" in host:
        username, host = host.split("@")

    if ":" in host:
        host, port = host.split(":")

    result = {}
    if protocol:
        result["protocol"] = protocol

    if username:
        result["user"] = username

    if host:
        result["host"] = host

    if port:
        result["port"] = int(port)

    return result


def unsorted_to_sorted_dict(unsorted):

    result = CommentedMap()
    for k in sorted(unsorted):
        result[k] = unsorted[k]

    return result


# from: https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-pytho
def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def intersect_lists(lists):

    if not lists:
        return []
    result = set(lists[0])
    for s in lists[1:]:
        s = set(s)
        result = result.intersection(s)
    return result


def get_all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )


# from: http://granitosaurus.rocks/getting-terminal-size.html
def get_terminal_size(fallback=(80, 24)):

    for i in range(0, 3):
        try:
            columns, rows = os.get_terminal_size(i)
        except (OSError, AttributeError):
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback
    return columns, rows


def auto_parse_string(content, content_type="auto", default_if_empty=None):
    """Try to automatically parse a string into a Python object."""

    loaded = None

    if not isinstance(content_type, string_types):
        raise Exception("Input is not a string, but '{}'".format(type(content)))

    if not content:
        if not default_if_empty:
            default_if_empty = {}
        return default_if_empty

    if content_type == "auto":

        if not content.strip()[0] == "{":
            content_type = "yaml"
            try:
                loaded = yaml.load(content)
            except (Exception):
                content_type = None

        if loaded is None and content.strip()[0] == "{":
            content_type = "json"
            try:
                loaded = json.loads(content)
            except (Exception):
                content_type = None

        if loaded is None:
            content_type = "toml"
            try:
                loaded = toml.loads(content)
            except (Exception):
                content_type = None

        if loaded is None:
            raise Exception(
                "Could not parse raw metadata, unknown format. Tried 'yaml', 'json', and 'toml': {}".format(
                    content
                )
            )

        log.debug("Auto-detected content type: {}".format(content_type))

    else:
        if content_type == "yaml":
            try:
                loaded = yaml.load(content)
            except (Exception) as e:
                raise Exception("Could not parse raw metadata as 'yaml': {}".format(e))
        elif content_type == "json":
            try:
                loaded = json.loads(content)
            except (Exception) as e:
                raise Exception("Could not parse raw metadata as 'json': {}".format(e))
        elif content_type == "toml":
            try:
                loaded = toml.loads(content)
            except (Exception) as e:
                raise Exception("Could not parse raw metadata as 'toml': {}".format(e))
        else:
            raise Exception(
                "Unsupported data format for metadata: {}".format(content_type)
            )

    return loaded
