# -*- coding: utf-8 -*-

"""Commandline-line related utility methods that are used across the frkl-suite (https://frkl.io) of tools.

To use this module, the 'Click' and 'cursor' packages need to be available.
"""
import inspect
import logging
import subprocess  # nosec
import sys
from collections import OrderedDict
from pydoc import locate

import click
import cursor
from plumbum import local
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from six import string_types

from .defaults import *  # noqa
from .frutils import (
    add_key_to_dict,
    dict_merge,
    parse_host_string,
    parse_ssh_config_string,
    readable,
)
from .parameters import Parameter, Parameters, create_default_arg

log = logging.getLogger("frutils")


class CursorOff(object):
    """A context-manager wrapper to hide the cursor on long(-ish) running computations for a cli-app."""

    def __enter__(self):
        """Hide cursor."""
        cursor.hide()

    def __exit__(self, *args):
        """Show cursor again."""
        cursor.show()


class HostType(click.ParamType):

    name = "host_type"

    def convert(self, value, param, ctx):

        try:
            details = parse_host_string(value)
            return details
        except (Exception):
            self.fail("%s is not a valid host string" % value, param, ctx)


class HostTypePlus(HostType):

    name = "host_type_plus"

    def list_hosts(self):
        try:
            status_out = (
                subprocess.check_output(  # nosec
                    ["vagrant", "status", "--machine-readable"]
                )
                .decode("utf-8")
                .rstrip()
            )
        except (Exception):
            return None

        hosts = {}
        for line in status_out.split("\n"):
            tokens = line.split(",")
            # timestamp = tokens[0]
            hostname = tokens[1]
            data_type = tokens[2]
            data = tokens[3:]
            if data_type == "state":
                if data[0] == "running":
                    hosts[hostname] = True
                else:
                    hosts[hostname] = False

        return hosts

    def convert(self, value, param, ctx):

        if value == "vagrant" or value.startswith("vagrant:"):

            return self.process_vagrant(value)

        elif "find-pi" in value:

            return self.process_find_pi(value)

        else:
            return super(HostTypePlus, self).convert(value, param, ctx)

    def process_find_pi(self, value):

        if value == "find-pi":
            host = "default"
            user = "pi"
        else:
            if "@" in value:
                user, host = value.split("@")
            else:
                click.echo(
                    "Can't parse Raspberry pi host-value, '{}', please use '<user>@find-pi".format(
                        value
                    )
                )
                sys.exit(1)

        log.debug("Raspberry Pi user: '{}', host alias: '{}'".format(user, host))

        nmap_available = check_local_executable("arp")

        if not nmap_available:

            click.echo(
                "\n'arp' is not installed on this machine, can't discover Rasperry Pis on this network. Either install it manually, or use the 'pkg-arp-installed' frecklecutable:\n\nfrecklecute pkg-arp-installed\n"
            )
            sys.exit(1)

        arp = local["arp"]
        awk = local["awk"]

        chain = arp["-n"] | awk["/b8:27:eb/ {print $1}"]

        result = chain()

        addresses = result.strip().split("\n")

        if len(addresses) == 0:
            click.echo(
                "No Raspberry Pi found in this network, you'll have to specify the ip address manually..."
            )
            sys.exit()
        if len(addresses) > 1:
            click.echo("\nMore than one IP addresses for Raspbery pi's found:")
            for a in addresses:
                click.echo("  - {}".format(a))
            click.echo()
            click.echo("Using first one: {}".format(addresses[0]))
        else:
            click.echo(
                "\nFound exactly one IP belonging to a Raspberry Pi: {}".format(
                    addresses[0]
                )
            )

        address = addresses[0]

        host_details = {"host": address, "user": user, "connection_type": "ssh"}

        return host_details

    def process_vagrant(self, value):

        if value == "vagrant":
            host = "default"
        else:
            host = value.split(":")[1]

        hosts = self.list_hosts()

        if hosts is None:
            self.fail("Not in a Vagrant folder, or Vagrant not installed.")
            return

        if host not in hosts.keys():
            self.fail(
                "No Vagrant host '{}' available. Are you in the right folder?".format(
                    host
                )
            )
            return

        if not hosts[host]:
            self.fail("Vagrant host '{}' not running.".format(host))

        config = subprocess.check_output(["vagrant", "ssh-config", host]).decode(
            "utf-8"
        )  # nosec
        host_details = parse_ssh_config_string(config)
        host_details["connection_type"] = "ssh"
        host_details["is_vagrant"] = True
        return host_details


def output_item(item_name, item, format, pager):
    """Print a 'title'-'item' formatted text."""
    click.secho("{}:".format(item_name), bold=True)
    click.echo("")
    output(item, output_type=format, pager=pager)
    click.echo("")


def output(
    python_object,
    output_type="raw",
    pager=False,
    safe=False,
    indent=0,
    nl=True,
    ignore_aliases=False,
    sort_keys=False,
):
    """Print a Python object in a certain format."""
    output_string = readable(
        python_object,
        out=output_type,
        safe=safe,
        indent=indent,
        ignore_aliases=ignore_aliases,
        sort_keys=sort_keys,
    )

    if pager:
        click.echo_via_pager(output_string)
    else:
        click.echo(output_string, nl=nl)


def create_flag_var(help_string, flag_names):
    """Create a dict to be used with lucify to create a flag option for a cli interface.

    Args:
      help_string (str): the user-facing explanation what this flag does
      flag_names (list): the cli option/flag names (e.g. ["--help", "-h"])

    Returns:
      dict: configuration to create a flag option

    """
    flag_dict = {
        "type": bool,
        "required": False,
        "default": False,
        "doc": {"help": help_string},
        "click": {"option": {"is_flag": True, "param_decls": flag_names}},
    }

    return flag_dict


def create_output_type_var():
    """Create a dict to be used with lucify to create an option to specify the output format for a command in a cli interface."""
    return {
        "type": str,
        "required": False,
        "doc": {"help": "the output type"},
        "click": {
            "option": {
                "param_decls": ["--format", "-f"],
                "type": click.Choice(["yaml", "json", "raw"]),
            }
        },
    }


def create_pager_var():
    """Create a dict to be used with lucify to create an option to use a pager in a cli interface command."""
    return {
        "type": bool,
        "required": False,
        "default": False,
        "doc": {"help": "whether to use a pager for display"},
        "click": {
            "option": {"param_decls": ["--pager", "-p"], "type": bool, "is_flag": True}
        },
    }


# cli util methods
def clean_user_input(user_input, vars_desc):
    """Clean up and re-map user input according to the description used to create the cli options/arguments.

    Args:
        user_input (dict): the dictionary with the arg-name/value mapping.
        vars_desc (dict): the dictionary used to create the cli options/arguments (with luci/lucify)

    Returns:
        dict: the final user input key/values

    """
    result = OrderedDict()
    for key in vars_desc.keys():

        if user_input.get(key, None) is not None:
            add_key_to_dict(result, key, user_input[key])

    return result


def convert_args_to_dict(args):
    """Ensure the input to create cli options is a dictionary.

    If that is not the case, the input list or string will be converted to a (properly formatted) dict.

    Args:
        args (list, str, dict): the input to create the cli options

    Returns:
         OrderedDict: the formatted dict

    """
    if isinstance(args, string_types):
        args = [args]

    result = OrderedDict()

    for arg in args:

        if isinstance(arg, (dict, OrderedDict, CommentedMap)):
            dict_merge(result, arg, copy_dct=False)
        elif isinstance(arg, string_types):
            arg_dict = {arg: create_default_arg(arg)}
            dict_merge(result, arg_dict, copy_dct=False)
        else:
            raise Exception("Can't parse arg(s): {}".format(str(args)))

    return result


def create_parameter(arg_name=None, arg_details=None, type_map=None):
    """Creates a :class:`~Parameter` object.

    Args:
        arg_name (str): the parameter name
        arg_details (dict): the parameter details

    Returns:
        Parameter: the parameter object
    """
    if arg_name is not None:
        return Parameter(arg_name, arg_details, type_map=type_map)
    else:
        raise Exception("No arg_name provided")


def create_parameters(args, default_enabled=True, default_vars=None, type_map=None):
    """Parses an list/string/dictionary and returns an expanded dict of arguments.

    Args:
        args: the argument(s)
        default_enabled (bool): whether to enable/disable options by default (not implemented yet)
        default_vars (dict): (extra) default vars
        type_map (dict): type mapping of click to cerberus types

    Returns:
        list: a list of options/arguments
    """

    if default_vars is None:
        default_vars = {}

    default_vars["omit"] = OMIT_VALUE

    parameters = []
    parameters_optional = []

    if isinstance(args, (dict, CommentedMap, OrderedDict)):

        for name, details in args.items():

            parameter = create_parameter(name, details, type_map=type_map)
            default = default_vars.get(name, None)
            if default:  # TODO: check whether that should instead test for None
                parameter.set_default(default)
            if parameter.scheme.get("required", True):
                parameters.append(parameter)
            else:
                parameters_optional.append(parameter)

    elif isinstance(args, string_types):
        parameter = create_parameter(args, None, type_map=type_map)
        default = default_vars.get(args, None)
        if default:  # TODO: check whether that should instead test for None
            parameter.set_default(default)
        if parameter.scheme.get("required", True):
            parameters.append(parameter)
        else:
            parameters_optional.append(parameter)
    elif isinstance(args, (list, tuple, CommentedSeq)):
        for arg in args:
            if isinstance(arg, string_types):
                parameter = create_parameter(arg, None, type_map=type_map)
                default = default_vars.get(arg, None)
                if default:  # TODO: check whether that should instead test for None
                    parameter.set_default(default)
                if parameter.scheme.get("required", True):
                    parameters.append(parameter)
                else:
                    parameters_optional.append(parameter)
            elif isinstance(arg, (dict, OrderedDict, CommentedMap)):
                for key, value in arg.items():
                    parameter = create_parameter(key, value, type_map=type_map)
                    default = default_vars.get(key, None)
                    if default:  # TODO: check whether that should instead test for None
                        parameter.set_default(default)
                    parameters.append(parameter)
                    if parameter.scheme.get("required", True):
                        parameters.append(parameter)
                    else:
                        parameters_optional.append(parameter)

            else:
                raise Exception("Invalid type for argument: {}".format(arg))
    else:
        raise Exception("Invalid type for argument: {}".format(args))

    result = Parameters(parameters + parameters_optional)

    return result


def parse_to_click_args_list(args, default_enabled=True):
    """Parse a dictionary and create a list of options/arguments the 'click' library can use to render a command-line interface.

    Args:
        args (dict): the input dictionary
        default_enabled (bool): whether to enable/disable options by default

    Returns:
        list: a list of :class:~click.Option and :class:~click.Argument objects

    """
    options_list = []

    if not isinstance(args, (dict, OrderedDict, CommentedMap)):
        args = convert_args_to_dict(args)

    for opt_name, details in args.items():

        if KEY_PARAM_ENABLED_NAME in details.keys():
            cli_enabled = details[KEY_PARAM_ENABLED_NAME]
        else:
            cli_enabled = default_enabled

        if not cli_enabled:
            log.debug("Argument '{}' not enabled for cli. Ignoring.".format(opt_name))
            continue

        # meta = details.get(KEY_META_GROUP, {})
        doc = details.get(KEY_DOC_GROUP, {})
        cli = details.get(KEY_CLI_GROUP, {})

        # arg_type = details.get(KEY_TYPE_NAME, KEY_TYPE_DEFAULT)
        required = details.get(KEY_REQUIRED_NAME, KEY_REQUIRED_DEFAULT)
        default = details.get(KEY_DEFAULT_VALUE_NAME, None)
        help_string = doc.get(KEY_HELP_NAME, None)

        alias = details.get(KEY_ALIAS_NAME, opt_name.replace(".", "_"))
        cli_option = cli.get(KEY_CLI_CLICK_OPTIONS_NAME, None)
        cli_argument = cli.get(KEY_CLI_CLICK_ARGUMENT_NAME, None)

        if cli_option and cli_argument:
            raise Exception(
                "Both '{}' and '{}' specified for argument '{}'. This is not possible, please remove one key.".format(
                    KEY_CLI_CLICK_OPTIONS_NAME, KEY_CLI_CLICK_ARGUMENT_NAME, opt_name
                )
            )

        param_is_option = True
        if cli_option:
            cli_parameters = cli_option
        elif cli_argument:
            cli_parameters = cli_argument
            param_is_option = False
        else:
            cli_parameters = {}

        default_parameters = {KEY_REQUIRED_NAME: required, KEY_HELP_NAME: help_string}
        if param_is_option:
            default_parameters[KEY_CLI_CLICK_PARAM_NAME] = ["--{}".format(alias)]
        else:
            default_parameters[KEY_CLI_CLICK_PARAM_NAME] = [alias]
        default_parameters[KEY_DEFAULT_VALUE_NAME] = default

        # pprint.pprint(default_parameters)
        # pprint.pprint(cli_parameters)
        # print("--------")
        param_details = dict_merge(default_parameters, cli_parameters, copy_dct=True)

        opt_type = param_details.get("type", None)
        if isinstance(opt_type, (list, tuple, CommentedSeq)):
            log.debug(
                "Found list in 'click.*.type' value, converting to click.Choice: {}".format(
                    opt_type
                )
            )
            opt_type = click.Choice(opt_type)
            param_details["type"] = opt_type
        elif isinstance(opt_type, string_types):
            opt_type_converted = locate(opt_type)
            if not opt_type_converted:
                raise Exception("No type found for: {}".format(opt_type))

            if inspect.isclass(opt_type_converted):

                if issubclass(opt_type_converted, click.ParamType):
                    param_details["type"] = opt_type_converted()
                else:
                    param_details["type"] = opt_type_converted

        if param_is_option:
            option_names = param_details.pop(KEY_CLI_CLICK_PARAM_NAME)
            o = click.Option(option_names, **param_details)
        else:
            param_details.pop(KEY_HELP_NAME)
            o = click.Argument(**param_details)

        # hope this doesn't interfere with anything internal in click
        o.name = opt_name

        options_list.append(o)

    return options_list


def check_local_executable(executable_name, msg_if_missing=None, exit_if_missing=False):
    """
    Checks whether an executable is available on the local machine.

    """

    try:
        local[executable_name]
        return True
    except (Exception) as e:
        log.debug("failed to load 'sshpass': {}".format(e))
        if msg_if_missing:
            click.echo(msg_if_missing)

        if exit_if_missing is True or (isinstance(exit, int) and exit_if_missing > 0):
            if exit_if_missing is True:
                sys.exit(1)
            else:
                sys.exit(exit_if_missing)
        return False


def output_to_terminal(line, nl=True, no_output=False):

    if no_output:
        return

    click.echo(line.encode("utf-8"), nl=nl)
