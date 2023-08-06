# -*- coding: utf-8 -*-

"""Default values for both frutils and the frkl-suite of tools (if appropriate)."""

import os

JINJA_DELIMITER_PROFILES = {
    "default": {
        "block_start_string": "{%",
        "block_end_string": "%}",
        "variable_start_string": "{{",
        "variable_end_string": "}}",
    },
    # "luci": {
    #     "block_start_string": "{%::",
    #     "block_end_string": "::%}",
    #     "variable_start_string": "{{::",
    #     "variable_end_string": "::}}",
    # },
    "freckles": {
        "block_start_string": "{%::",
        "block_end_string": "::%}",
        "variable_start_string": "{{::",
        "variable_end_string": "::}}",
    },
    "shell": {
        "block_start_string": "#%::",
        "block_end_string": "#::%",
        "variable_start_string": "#{{::",
        "variable_end_string": "::}}#",
    },
    "documentation": {
        "block_start_string": "{{%=",
        "block_end_string": "=%}}",
        "variable_start_string": "{{==",
        "variable_end_string": "==}}",
    },
    "tempting": {
        "block_start_string": "{%::",
        "block_end_string": "::%}",
        "variable_start_string": "{{::",
        "variable_end_string": "::}}",
    },
}

DEFAULT_BLOCK_START_STRING = "{%"
DEFAULT_BLOCK_END_STRING = "%}"
DEFAULT_VARIABLE_START_STRING = "{{"
DEFAULT_VARIABLE_END_STRING = "}}"
DEFAULT_LOCAL_ENV_VARS_KEY = "LOCAL_ENV"

# KEY_LUCI_NAME = "__lucify__"
# KEY_DICTLET_LUCIFIER_NAME = "__default_lucifier__"

KEY_META_GROUP = "meta"
KEY_DOC_GROUP = "doc"
KEY_CLI_GROUP = "click"
KEY_VARS_GROUP = "vars"
KEY_ARGS_GROUP = "args"
# KEY_LUCIFIERS_GROUP = "lucifiers"

KEY_INCLUDE_DEFAULT_VARS_NAME = "include_default_vars"

KEY_TYPE_NAME = "type"
KEY_TYPE_DEFAULT = "string"
KEY_ALIAS_NAME = "alias"
KEY_REQUIRED_NAME = "required"
KEY_REQUIRED_DEFAULT = False
KEY_DEFAULT_VALUE_NAME = "default"

KEY_HELP_NAME = "help"
KEY_SHORT_HELP_NAME = "short_help"
KEY_EPILOG_NAME = "epilog"
KEY_PARAMETER_TYPE = "param_type"
KEY_OPTION_TYPE = "option"
KEY_ARGUMENT_TYPE = "argument"

KEY_PARAM_ENABLED_NAME = "cli_enabled"
KEY_CLI_CLICK_OPTIONS_NAME = "option"
KEY_CLI_CLICK_ARGUMENT_NAME = "argument"
KEY_CLI_CLICK_PARAM_NAME = "param_decls"

URL_PLACEHOLDER = -9876

SUPPORTED_OUTPUT_FORMATS = ["raw", "yaml", "json"]

# abbreviations used by the UrlAbbrevProcessor class
DEFAULT_URL_ABBREVIATIONS_FILE = {
    "gh": [
        "https://raw.githubusercontent.com",
        "/",
        URL_PLACEHOLDER,
        "/",
        URL_PLACEHOLDER,
        "/",
        "{{ branch }}",
        "/",
    ],
    "bb": [
        "https://bitbucket.org",
        "/",
        URL_PLACEHOLDER,
        "/",
        URL_PLACEHOLDER,
        "/",
        "src",
        "/",
        "{{ branch }}",
        "/",
    ],
    "gl": [
        "https://gitlab.com",
        "/",
        URL_PLACEHOLDER,
        "/",
        URL_PLACEHOLDER,
        "/",
        "raw",
        "/",
        "{{ branch }}",
        "/",
    ],
}

DEFAULT_URL_ABBREVIATIONS_REPO = {
    "gh": ["https://github.com/", URL_PLACEHOLDER, "/", URL_PLACEHOLDER, ".git"],
    "bb": ["https://bitbucket.org/", URL_PLACEHOLDER, "/", URL_PLACEHOLDER, ".git"],
    "gl": ["https://gitlab.com/", URL_PLACEHOLDER, "/", URL_PLACEHOLDER, ".git"],
}


DEFAULT_EXCLUDE_DIRS = [".git", ".tox", ".cache"]

DEFAULT_DOWNLOAD_CACHE_BASE = os.path.expanduser("~/.local/share/frkl/download_cache")
OMIT_VALUE = "_______OMIT_VALUE________"
