# -*- coding: utf-8 -*-
"""Main module."""
import copy
import json
import logging
import os
import sys

import click
from cerberus import SchemaError, Validator
from passlib.handlers.sha2_crypt import sha512_crypt
from ruamel.yaml.comments import CommentedSeq
from six import string_types

from frutils import StringYAML, is_url_or_abbrev, readable_yaml

from .doc import Doc

# from .exceptions import ParameterException, ParametersException

log = logging.getLogger("frutils")

yaml = StringYAML()

CERBERUS_SCHEMA_SCHEMA = {
    "allof": {"logical": "allof", "type": "list"},
    "allow_unknown": {
        "oneof": [
            {"type": "boolean"},
            {"type": ["dict", "string"], "validator": "bulk_schema"},
        ]
    },
    "allowed": {"type": "list"},
    "anyof": {"logical": "anyof", "type": "list"},
    "coerce": {
        "oneof": [
            {"type": "callable"},
            {
                "schema": {
                    "oneof": [{"type": "callable"}, {"allowed": (), "type": "string"}]
                },
                "type": "list",
            },
            {"allowed": (), "type": "string"},
        ]
    },
    "default": {"nullable": True},
    "default_setter": {
        "oneof": [{"type": "callable"}, {"allowed": (), "type": "string"}]
    },
    "dependencies": {"type": ("dict", "hashable", "list"), "validator": "dependencies"},
    "empty": {"type": "boolean"},
    "excludes": {"schema": {"type": "hashable"}, "type": ("hashable", "list")},
    "forbidden": {"type": "list"},
    "items": {"type": "list", "validator": "items"},
    "keyschema": {
        "forbidden": ["rename", "rename_handler"],
        "type": ["dict", "string"],
        "validator": "bulk_schema",
    },
    "max": {"nullable": False},
    "maxlength": {"type": "integer"},
    "min": {"nullable": False},
    "minlength": {"type": "integer"},
    "noneof": {"logical": "noneof", "type": "list"},
    "nullable": {"type": "boolean"},
    "oneof": {"logical": "oneof", "type": "list"},
    "purge_unknown": {"type": "boolean"},
    "readonly": {"type": "boolean"},
    "regex": {"type": "string"},
    "rename": {"type": "hashable"},
    "rename_handler": {
        "oneof": [
            {"type": "callable"},
            {
                "schema": {
                    "oneof": [{"type": "callable"}, {"allowed": (), "type": "string"}]
                },
                "type": "list",
            },
            {"allowed": (), "type": "string"},
        ]
    },
    "required": {"type": "boolean"},
    "schema": {
        "anyof": [{"validator": "schema"}, {"validator": "bulk_schema"}],
        "type": ["dict", "string"],
    },
    "type": {"type": ["string", "list"], "validator": "type"},
    "validator": {
        "oneof": [
            {"type": "callable"},
            {
                "schema": {
                    "oneof": [{"type": "callable"}, {"allowed": (), "type": "string"}]
                },
                "type": "list",
            },
            {"allowed": (), "type": "string"},
        ]
    },
    "valueschema": {
        "forbidden": ["rename", "rename_handler"],
        "type": ["dict", "string"],
        "validator": "bulk_schema",
    },
}

DOC_SCHEMA = {
    "type": "dict",
    "schema": {
        "help": {"type": "string"},
        "short_help": {"type": "string"},
        "examples": {"type": "list", "schema": {"type": "string"}},
    },
}

PARAMETER_SCHEME = {
    "type": {"type": "string", "default": "string"},
    "required": {"type": "boolean", "default": True},
    "default": {"required": False, "empty": True},
    "coerce": {"required": False, "empty": False},
    "excludes": {"required": False, "empty": False},
    "keyschema": {"required": False, "empty": False},
    "valueschema": {"required": False, "empty": False},
}

CLI_SCHEME = {
    "param_type": {
        "type": "string",
        "allowed": ["option", "argument"],
        "default": "option",
    },
    "param_decls": {"type": "list", "schema": {"type": "string"}},
    # "type": {"type": "string"},
    "required": {"type": "boolean"},
    "default": {"type": "string"},
    "nargs": {"type": "integer"},
    "metavar": {"type": "string"},
    "expose_value": {"type": "boolean"},
    "is_eager": {"type": "boolean"},
    "envvar": {"type": "list", "schema": {"type": "string"}},
    "show_default": {"type": "boolean"},
    "prompt": {"type": "boolean"},
    "confirmation_prompt": {"type": "boolean"},
    "hide_input": {"type": "boolean"},
    "is_flag": {"type": "boolean"},
    "multiple": {"type": "boolean"},
    "count": {"type": "boolean"},
    "help": {"type": "string"},
    "enabled": {"type": "boolean", "default": True},
}


class VarsTypeSimple(click.ParamType):

    name = "vars_type"

    def convert(self, value, param, ctx):

        if not isinstance(value, string_types):
            return value

        path = os.path.realpath(os.path.expanduser(value))
        value_type = "string"
        if os.path.exists(path):
            value_type = "local"
        elif is_url_or_abbrev(value):
            value_type = "remote"

        if value_type in ["remote", "local"]:

            raise Exception("Loading a dict from a file not implemented yet.")

        else:
            # try yaml
            log.debug("Trying yaml for value: '{}'".format(value))

            try:
                result = json.loads(value)
            except (Exception):
                try:
                    result = yaml.load(value)
                except (Exception):
                    self.fail("Can't read vars string: {}".format(value))

            return result


class FrutilsNormalizer(Validator):
    def __init__(self, *args, **kwargs):
        try:
            super(FrutilsNormalizer, self).__init__(*args, **kwargs)
        except (SchemaError) as se:
            a = se.args
            click.echo("\nInvalid cerebus schema provided:\n")
            import traceback

            traceback.print_stack()
            click.echo(readable_yaml(a))
            click.echo(
                "\nPlease check the cerebus documentation ( http://docs.python-cerberus.org/en/stable/validation-rules.html) for more information.\n"
            )

            sys.exit(1)

    def _normalize_coerce_sha512_crypt(self, value):

        if not value:
            return None

        hashed_pass = sha512_crypt.using(rounds=5000).hash(value)
        return hashed_pass


def create_default_arg(arg_name):
    """Create a dict to be used to create an option using default values (in luci/lucify).

    Args:
        arg_name (str): the option name

    Returns:
        dict: the configuration for the option to be created

    """
    result = {"type": str, "required": False, "doc": {"help": "n/a"}}

    return result


CLICK_CEREBUS_ARG_MAP = {
    "string": str,
    "float": float,
    "integer": int,
    "boolean": bool,
    "dict": VarsTypeSimple(),
    "password": str,
    # "list": list
}


def get_type_string_for_class(class_obj, default="string", type_map=None):

    if type_map is None:
        type_map = CLICK_CEREBUS_ARG_MAP

    for key, value in type_map.items():

        if value == class_obj:
            return key
    return default


def generate_alias(var_name):

    var_name = var_name.strip("-")
    var_name = var_name.replace("-", "_")
    return var_name


class ParameterException(Exception):
    def __init__(self, parameter, errors="n/a"):
        super(ParameterException, self).__init__(
            "Error with parameter '{}': {}".format(parameter.name, errors)
        )
        self.parameter = parameter
        self.errors = errors


class ParametersException(Exception):
    def __init__(self, parameters, errors="n/a"):
        super(ParametersException, self).__init__(
            "Invalid parameter(s): {}".format(errors)
        )
        self.parameters = parameters
        self.errors = errors


class Parameter(object):
    def __init__(self, param_name, scheme=None, default=None, type_map=None):

        scheme = copy.deepcopy(scheme)

        if type_map is None:
            type_map = CLICK_CEREBUS_ARG_MAP

        self.type_map = type_map

        self.name = param_name

        if scheme is None:
            scheme = {}

        doc = scheme.pop("doc", {"help": "n/a"})

        scheme.pop("__auto_generated__", False)
        scheme.pop("__is_arg__", False)

        self.doc = Doc(doc)

        if "coerce" in scheme.keys():
            coerce = scheme["coerce"]
            if isinstance(coerce, string_types):
                repl = self.type_map.get(coerce, None)
                if repl is not None:
                    scheme["coerce"] = repl

        aliases = scheme.pop("aliases", [])

        if isinstance(aliases, string_types):
            aliases = [aliases]
        if not isinstance(aliases, (list, tuple, CommentedSeq)):
            raise ParameterException(
                self,
                errors="Parameter aliases property needs to be string or list: {}".format(
                    aliases
                ),
            )
        self.aliases = list(set(aliases))
        if not self.aliases:
            self.aliases.append(self.name)

        # p_type = scheme.get("type", None)
        # if p_type != None and p_type in CLICK_CEREBUS_ARG_MAP.keys() and "coerce" not in scheme.keys():
        #     scheme["coerce"] = CLICK_CEREBUS_ARG_MAP[p_type]

        cli_raw = scheme.pop("cli", {})
        cli_validator = FrutilsNormalizer(CLI_SCHEME)

        self.cli = cli_validator.validated(cli_raw)
        if self.cli is None:
            raise ParameterException(self, cli_validator.errors)
        self.cli_param_type = self.cli.pop("param_type")
        self.cli_enabled = self.cli.pop("enabled")

        # if scheme.get("type", "string") == "dict":
        # log.debug("Disabling dict argument '{}' for cli.".format(param_name))
        # self.cli_enabled = False

        for alias in self.cli.get("param_decls", []):
            self.aliases.append(generate_alias(alias))

        scheme_validator = FrutilsNormalizer(PARAMETER_SCHEME, allow_unknown=True)
        self.scheme = scheme_validator.validated(scheme)
        if self.scheme is None:
            raise ParameterException(self, scheme_validator.errors)
        self.default = default

    def set_click_type(self, option_properties, scheme, param_type):

        cerberus_type = scheme["type"]

        # if cerberus_type == "dict":
        #     # this is, for now, only dealing with string keys/values
        #     # option_properties["multiple"] = True
        #     # option_properties["nargs"] = 2
        #     raise Exception("'dict' values not allowed to be used with command-line parser")

        # return

        replacement = self.type_map.get(cerberus_type, None)

        if replacement is not None:
            if replacement == bool:
                if "is_flag" not in option_properties.keys():
                    option_properties["is_flag"] = True
                    # we don't add the type here, otherwise click fails for whatever reason
            else:
                option_properties["type"] = replacement

            return

        if cerberus_type == "list":
            arg_schema = scheme.get("schema", {})
            schema_type = arg_schema.get("type", "string")
            replacement = self.type_map.get(schema_type, click.STRING)
            option_properties["type"] = replacement
            if param_type == "option":
                option_properties["multiple"] = True
            else:
                option_properties["nargs"] = -1

            return

        else:

            raise Exception("Type '{}' not implemented yet.".format(cerberus_type))

    def __str__(self):

        return self.name

    def __repr__(self):

        return "Parameter[name='{}']".format(self.name)

    def get_help(self):

        return self.doc.get_help()

    def get_short_help(self, list_item_format=False):

        return self.doc.get_short_help(list_item_format=list_item_format)

    def set_default(self, default_value):

        self.default = default_value

    def generate_click_parameters(
        self, use_default=True, replace_dashes=True, show_defaults_default=True
    ):
        """Generates a list of parameter objects that can be used with the click library.

        Args:
            init_dict (dict): additional default values for potential keys
            replace_dashes (bool): if set to True, underscore characters in keys will be replaced with dashes
        """

        if not self.cli_enabled:
            return None

        option_properties = copy.deepcopy(self.cli)
        temp_scheme = self.scheme
        if use_default and self.default is not None:
            temp_scheme["default"] = self.default
            if "show_default" not in option_properties.keys():
                option_properties["show_default"] = True

        for property in ["required", "default"]:

            if (
                property in temp_scheme.keys()
                and property not in option_properties.keys()
            ):
                option_properties[property] = temp_scheme[property]

        if "param_decls" not in option_properties.keys():
            if self.cli_param_type == "option":
                decls = []
                for a in self.aliases:
                    if len(a) == 1:
                        decls.append("-{}".format(a))
                    else:
                        if replace_dashes and "_" in a:
                            a = a.replace("_", "-")
                        decls.append("--{}".format(a))
                option_properties["param_decls"] = decls
            elif self.cli_param_type == "argument":
                option_properties["param_decls"] = [self.name]
            else:
                raise Exception(
                    "Invalid parameter type: {}".format(self.cli_param_type)
                )
        if "metavar" not in option_properties.keys():
            option_properties["metavar"] = self.name.upper()

        if "show_default" not in option_properties.keys() and show_defaults_default:
            option_properties["show_default"] = True

        auto_password_prompt = False
        if self.scheme["type"] == "password":
            if self.cli_enabled:
                if "prompt" not in self.cli.keys():
                    if self.scheme.get("default", None) is not None:
                        raise Exception(
                            "Defaults are not supported for password: '{}'".format(
                                self.name
                            )
                        )

                    if option_properties["required"]:
                        # we'll prompt anyway
                        return None
                    auto_password_prompt = True
                    option_properties["type"] = bool
                    option_properties["is_flag"] = True
                    option_properties["required"] = False

        self.set_click_type(option_properties, temp_scheme, self.cli_param_type)
        if self.cli_param_type == "option":
            if not auto_password_prompt:
                option_properties["help"] = self.get_short_help()
            else:
                option_properties["help"] = (
                    self.get_short_help() + " (optional, prompts if this flag is set)"
                )
            p = click.Option(**option_properties)
        else:
            option_properties.pop("show_default", None)
            if (
                "nargs" in option_properties.keys()
                and "default" in option_properties.keys()
            ):
                option_properties.pop("nargs")
            p = click.Argument(**option_properties)

        return p


class Parameters(object):
    def __init__(self, param_list, param_list_name="unnamed"):

        self.name = param_list_name
        self.param_list = param_list
        self.scheme = None
        self.scheme_no_defaults = None

    def __repr__(self):

        return "Parameters[{}]".format(", ".join([str(p) for p in self.param_list]))

    def get_required_vars(self, required_if_not_specified=True):

        result = []

        for p in self.param_list:
            if p.scheme.get("required", required_if_not_specified):
                result.append(p)

        return result

    def get_optional_vars(self, required_if_not_specified=True):

        result = []

        for p in self.param_list:
            if not p.scheme.get("required", required_if_not_specified):
                result.append(p)

        return result

    def get_all_vars_of_type(self, param_type):
        result = {}
        for varname, scheme in self.get_validator_scheme().items():
            if scheme["type"] == param_type:
                result[varname] = scheme

        return result

    def get_all_varnames_of_type(self, param_type):
        result = []
        for varname, scheme in self.get_validator_scheme().items():
            if scheme["type"] == param_type:
                result.append(varname)

        return result

    def get_validator_scheme(self):

        if self.scheme is not None:
            return self.scheme

        scheme = {}
        for param in self.param_list:
            scheme[param.name] = param.scheme
        self.scheme = scheme
        return self.scheme

    def generate_alias_map(self):

        result = {}

        for param in self.param_list:

            aliases = param.aliases

            name = param.name

            for a in aliases:
                if a == param.name:
                    continue
                if a in result.keys():
                    raise ParametersException(self, "Duplicate alias/key: {}".format(a))
                if "/" in a:
                    a = a.split("/")[0]
                result[generate_alias(a)] = name

        return result

    def translate_args(self, args):

        alias_map = self.generate_alias_map()
        # import pp
        # pp(alias_map)
        result = {}

        for key, value in args.items():

            if value is None:
                continue

            if key in alias_map.keys():
                result[alias_map[key]] = value
            else:
                result[key] = value

        # pp(result)
        # print('------------')
        return result
        # return self.validate(result)

    def validate(self, input_dict):

        validator = FrutilsNormalizer(self.get_validator_scheme(), purge_unknown=True)
        valid = validator.validated(input_dict)
        if valid is None:
            raise ParametersException(self, validator.errors)
        return valid

    def generate_click_parameters(self, use_defaults=True):

        result = []
        for param in self.param_list:
            if param.cli_enabled:
                param = param.generate_click_parameters(use_default=use_defaults)
                if param is not None:
                    result.append(param)

        return result
