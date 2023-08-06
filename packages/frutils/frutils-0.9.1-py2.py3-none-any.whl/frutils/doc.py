# -*- coding: utf-8 -*-

"""Generic configuration class."""

import logging
from collections import Mapping

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from six import string_types

from frutils import readable_yaml

log = logging.getLogger("frutils")

yaml = YAML(typ="safe")


class Doc(object):
    @classmethod
    def to_list_item_format(self, msg, first_char_lowercase=True):

        if first_char_lowercase:
            msg = msg[0].lower() + msg[1:]

        if msg.endswith("."):
            msg = msg[0:-1]

        if msg.startswith("[") and msg.endswith("]"):
            msg = msg[1:-1]

        return msg

    def __init__(
        self,
        doc_dict,
        short_help_key="short_help",
        help_key="help",
        long_help_key="long_help",
        further_reading_key="further_reading",
        examples_key="examples",
    ):

        if not doc_dict:
            doc_dict = {}

        self.short_help_key = short_help_key
        self.help_key = help_key
        self.long_help_key = long_help_key
        self.further_reading_key = further_reading_key
        self.examples_key = examples_key

        if isinstance(doc_dict, string_types):

            if "\n" in doc_dict:
                short_help = doc_dict.split("\n")[0]
                help = doc_dict
                temp = {"short_help": short_help, "help": help}
            else:
                short_help = doc_dict
                temp = {"short_help": short_help}
            self.doc_dict = temp

        elif isinstance(doc_dict, Mapping):
            self.doc_dict = {}
            self.doc_dict["short_help"] = doc_dict.get(short_help_key, None)
            self.doc_dict["help"] = doc_dict.get(self.help_key, None)
            self.doc_dict["long_help"] = doc_dict.get(self.long_help_key, None)
            self.doc_dict["further_reading"] = doc_dict.get(self.further_reading_key)
            self.doc_dict["examples"] = doc_dict.get(self.examples_key, None)

    def get_short_help(self, default="n/a", list_item_format=False, use_help=True):

        result = self.doc_dict.get("short_help", None)
        if result is None:
            if use_help:
                help = self.get_help(default=default)
            else:
                help = None
            if not help:
                return default
            first_line = help.split("\n")[0]
            result = first_line

        if list_item_format:
            result = Doc.to_list_item_format(result)

        if result:
            result = result.strip()
        return result

    def get_help(self, default="n/a", use_short_help=True):

        result = self.doc_dict.get("help", None)
        if not result and not use_short_help:
            result = default
        elif result is None:
            if "short_help" in self.doc_dict.keys():
                result = self.get_short_help(default=default, use_help=False)
            else:
                result = default

        if result:
            result = result.strip()

        return result

    def get_long_help(self):

        if "long_help" in self.doc_dict and self.doc_dict["long_help"]:
            return self.doc_dict["long_help"]
        else:
            return None

    def matches_apropos(self, apropos, only_short_help=True):
        """Checks whether this documentations text matches all of the apropos matchers."""

        if not apropos:
            return False

        if isinstance(apropos, string_types):
            apropos = [apropos]

        match = True
        for a in apropos:
            if only_short_help:
                if a.lower() not in self.get_short_help().lower():
                    match = False
                    break

            else:
                if (a.lower() not in self.get_short_help().lower()) and (
                    a.lower() not in self.get_help().lower()
                ):
                    match = False
                    break
        return match

    def get_notes(self):

        return self.doc_dict.get("notes", [])

    def get_examples(self):

        return self.doc_dict.get("examples", [])

    def get_further_reading(self):

        return self.doc_dict.get("further_reading", {})

    def exploded_dict(self):

        result = CommentedMap()
        if self.doc_dict["short_help"]:
            result["short_help"] = self.get_short_help(
                "n/a", list_item_format=False, use_help=False
            )
        if self.doc_dict["help"]:
            result["help"] = self.get_help("n/a", use_short_help=False)
        if self.get_long_help():
            result["long_help"] = self.get_long_help()
        if self.get_further_reading():
            result["further_reading"] = self.get_further_reading()
        if self.get_examples():
            result["examples"] = self.get_examples()
        if self.get_notes():
            result["notes"] = self.get_notes()

        return result

    def __str__(self):

        return readable_yaml(self.doc_dict)

    def __repr__(self):

        return readable_yaml(self.doc_dict)
