# -*- coding: utf-8 -*-
import copy
import hashlib
import os
import re
from collections import Sequence

from jinja2 import contextfilter
from markupsafe import Markup
from passlib.handlers.sha2_crypt import sha512_crypt
from passlib.hash import postgres_md5
from six import string_types
from slugify import slugify

from .doc import Doc
from .frutils import DEFAULT_ENV, DEFAULT_STRING_YAML, dict_merge

# def top_level_functions(body):
#     return (f for f in body if isinstance(f, ast.FunctionDef))
#
# def parse_ast(filename):
#     with open(filename, "rt") as file:
#         return ast.parse(file.read(), filename=filename)
#


def to_yaml_filter(value):
    """Returns a yaml string of the provided object/dict.

    Args:
      value (object): the input object/dict

    Returns:
      string: a yaml-formatted string
    """

    if not value:
        return ""

    result = DEFAULT_STRING_YAML.dump(value)

    return result.strip()


def negate_filter(value):
    """
    Negates a boolean value.

    If the input is not a boolean, it will be converted to one: bool(value)

    Args:
      value (bool, object): the input
    Returns:
      bool: the inverse
    """

    if not isinstance(value, bool):
        value = bool(value)

    return not value


def negate_or_default_filter(value, default):
    """
    Negates a value if it is a bool, otherwise returns the default value.

    This is useful for example to pipe in potential None values or empty strings, and get back a default value if that is the case.

    Args:
      value (bool): the value
      default (bool): the default if value is not a bool
    Returns:
      bool: the default
    """

    if isinstance(value, bool):
        return negate_filter(value)

    if not isinstance(default, bool):
        raise Exception("negate default needs to be of type bool: {}".format(default))
    return default


def default_if_empty_filter(value, default):
    """
    Returns a default if provided with an empty value.

    Test for empty is: 'not value'. If value is a bool, it will be returned as is.

    Args:
      value (object): the input
      default (object): the default
    Returns:
      object: the value itself, or the default if empty
    """

    if isinstance(value, bool):
        return value

    if not value:
        return default
    else:
        return value


def string_for_boolean_filter(value, true_value, false_value):
    """
    Returns a different object depending on whether the value resolves to True or not.

    Test for True is simply: 'if value'.

    Args:
      value (object): the input
      true_value (object): the result if input is True
      false_value (object): the result if input is False
    Result:
      object: the result
    """

    if value:
        return true_value
    else:
        return false_value


def true_if_not_empty_filter(value):
    """
    Returns true if the value is not empty.

    This is the same as the 'false_if_empty'-filter.

    Args:
      value (object): the input
    Result:
      bool:
    """

    return false_if_empty_filter(value)


# def true_if_all_not_empty_filter(*value):
#
#     for v in value:
#         if not isinstance(v, bool) and not v:
#             return False
#
#     return True


def true_if_all_empty_filter(*value):
    """
    Returns true if all values are empty.

    Boolean 'False' doesn't count as empty.
    """

    for v in value:
        if isinstance(v, bool) or v:
            return False

    return True


def false_if_not_empty_filter(value):
    """
    Returns 'false' if the provided value is not empty.

    Args:
      value (object): the value
    Result:
      boolean: the result
    """

    if isinstance(value, bool) or value:
        return False
    else:
        return True


def false_if_all_not_empty_filter(*value):
    """
    Returns false if all provided values are non-empty.

    Args:
      value (list): a list of inputs
    Result:
      bool: true if at least one provided value is empty, false if all are non-empty, or the list is empty
    """

    for v in value:
        if not isinstance(v, bool) and not v:
            return True

    return False


def false_if_all_empty_filter(*value):
    """
    Returns false if all provided values are empty.

    Args:
      value (list): a list of inputs
    Result:
      bool: true if at least one provided value is non-empty, false if all are empty, or the list is empty.
    """

    for v in value:
        if isinstance(v, bool) or v:
            return True

    return False


def true_if_empty_filter(value):
    """
    Returns 'true' if the provided value is empty.

    Args:
      value (object): the value
    Result:
      boolean: the result
    """

    if not isinstance(value, bool) and not value:
        return True
    else:
        return False


def true_if_empty_or_filter(value, *or_values):
    """
    Returns 'true' if the provided value is empty or matches any of the provided values.

    Args:
      value (object): the value
      or_values (list): or_values
    Result:
      boolean: the result
    """

    if not isinstance(value, bool) and not value:
        return True
    else:
        if value in or_values:
            return True
        else:
            return False


def false_if_empty_filter(value):
    """
    Returns 'false' if the provided value is empty.

    Args:
      value (object): the value
    Result:
      boolean: the result
    """

    if not isinstance(value, bool) and not value:
        return False
    else:
        return True


def true_if_equal_filter(*value):
    """
    Returns 'true' if all values are equal, otherwise 'false'.
    """

    first = True
    eq = None
    for v in value:
        if first:
            eq = v
            first = False
            continue
        if eq != v:
            return False

    return True


def false_if_equal_filter(*value):
    """
    Returns 'false' if all values are equal, otherwise 'true'.
    """

    first = True
    eq = None
    for v in value:
        if first:
            eq = v
            first = False
            continue
        if eq != v:
            return True

    return False


def none_if_empty_filter(value):
    """
    Returns None value if input is an empty value.
    Args:
        value: the value

    Returns: None if the value is empty, otherwise the value

    """

    if isinstance(value, string_types):
        value = value.strip()

    if not value:
        return None
    else:
        return value


def basename_filter(path):
    """
    Returns the basename (without trailing slash) of a path.

    Args:
      path (str): the path to a folder or file
    Result:
      str: the basename
    """
    if path.endswith(os.path.sep):
        path = path[:-1]
    return os.path.basename(path)


def dirname_filter(path):
    """
    Returns the dirname (without trailing slash) of a path.

    Args:
      path (str): the path to a folder or file
    Result:
      str: the dirname
    """

    if not path:
        return None

    if path.endswith(os.path.sep):
        path = path[:-1]
    return os.path.dirname(path)


def clean_string_filter(string):
    """
    Returns a string with all non char/digit characters replaced with '_'.
    """
    if isinstance(string, string_types):
        result = re.sub("[^A-Za-z0-9]+", "_", string)
    else:
        result = string

    return result


def none_if_equals_filter(value, equal):
    """
    Returns 'None' if the input equals the other value, otherwise it returns the input.
    """

    if value == equal:
        return None
    else:
        return value


def sha512_crypt_filter(value):

    if not value:
        return None

    hashed_pass = sha512_crypt.using(rounds=5000).hash(value)
    return hashed_pass


def md5sum_filter(input):
    """
    Returns the md5 sum of a string.
    """

    input = input.encode("utf-8")
    result = hashlib.md5(input).hexdigest()
    return result


def postgresql_password_hash_filter(password, username):
    """Returns an encoded string that PostgreSQL accepts as an 'encrypted' password."""

    result = postgres_md5.hash(password, user=username)

    return result


def slugify_filter(input):

    if not input:
        return input

    return slugify(input)


def and_item_filter(a_list, input):

    if isinstance(a_list, string_types):
        a_list = [a_list]
    if not isinstance(a_list, Sequence):
        a_list = [a_list]

    result = a_list + [input]
    return result


def and_items_filter(a_list, *additional_items):

    if isinstance(a_list, string_types):
        a_list = [a_list]
    if not isinstance(a_list, Sequence):
        a_list = [a_list]

    result = copy.copy(a_list)

    for input in additional_items:
        if isinstance(input, string_types):
            input = [input]
        if not isinstance(input, Sequence):
            input = [input]

        result = result + input

    return result


# from: https://stackoverflow.com/questions/8862731/jinja-nested-rendering-on-variable-content
@contextfilter
def subrender_filter(context, value):
    _template = context.eval_ctx.environment.from_string(value)
    result = _template.render(**context)

    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result


ALL_MEMBERS = locals()


def get_all_filter_functions():

    result = {}

    for func_name, func in ALL_MEMBERS.items():
        if not func_name.endswith("filter"):
            continue

        help = func.__doc__
        doc = Doc({"help": help})
        name = func_name[0:-7]

        result[name] = {"func": func, "doc": doc}

    return result


ALL_FRUTIL_FILTERS = get_all_filter_functions()


def get_jinja_default_filters():

    result = {}

    for filter_name, func in DEFAULT_ENV.filters.items():

        help = func.__doc__
        doc = Doc({"help": help})

        result[filter_name] = {"func": func, "doc": doc}

    return result


ALL_DEFAULT_JINJA2_FILTERS = get_jinja_default_filters()

ALL_FILTERS = dict_merge(ALL_DEFAULT_JINJA2_FILTERS, ALL_FRUTIL_FILTERS, copy_dct=True)
