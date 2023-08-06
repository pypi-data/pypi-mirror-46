# -*- coding: utf-8 -*-
import abc
import copy
import io
import logging
import os
import pprint
from collections import OrderedDict

import six
from cerberus import Validator
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from frutils import dict_merge, ensure_parent_dir
from frutils.doc import Doc
from frutils.exceptions import CnfException, CnfValidationException

log = logging.getLogger("frutils")
yaml = YAML()


class Cnf(object):
    def __init__(
        self, config_dict=None, cnf_plugins=None, interpreters=None, validator=None
    ):

        if config_dict is None:
            config_dict = {}
        if cnf_plugins is None:
            cnf_plugins = []

        self._cnf_plugins = cnf_plugins
        self._root_config = config_dict

        self._interpreters = {}

        if validator is None:
            validator = Validator

        self.validator = validator

        if interpreters:
            for interpreter_name, schema in interpreters.items():
                self.add_interpreter(name=interpreter_name, schema=schema)

    @property
    def config(self):

        return self._root_config

    @config.setter
    def config(self, config):

        self._root_config = config
        self._invalidate_interpreters()

    def merge_dict(self, overlay):
        """Overlays a dictionary over the internal config dict.

        This ignores any plugins.
        """

        dict_merge(self.config_dict, overlay, copy_dct=False)
        self._invalidate_interpreters()

    def filter_through_schema(self, schema):
        """A quick filter using an ad-hoc CnfInterpreter."""

        temp = CnfInterpreter(self, schema)
        return temp.config

    def _invalidate_interpreters(self):

        for interpreter in self._interpreters.values():
            interpreter._invalidate()

    def add_interpreter(
        self, name, schema, doc_key="doc", target_attr_key="target_key", validator=None
    ):

        if name in self._interpreters.keys():
            if self._interpreters[name].schema != schema:
                raise Exception(
                    "Can't add already existing config interpreter '{}' with different schema.".format(
                        name
                    )
                )
            return self._interpreters[name]

        if validator is None:
            validator = self.validator

        schema = copy.deepcopy(schema)
        interpreter = CnfInterpreter(
            parent_cnf=self,
            schema=schema,
            doc_key=doc_key,
            target_attr_key=target_attr_key,
            validator=validator,
        )
        self._interpreters[name] = interpreter

        return interpreter

    def get_interpreter(self, interpreter_name):

        if interpreter_name not in self._interpreters.keys():
            raise CnfException(
                msg="No interpreter with name '{}' available.".format(interpreter_name),
                cnf=self,
            )

        return self._interpreters[interpreter_name]

    def get_interpreter_names(self):

        return self._interpreters.keys()

    def get_interpreter_value(self, interpreter_name, key_name, default=None):

        return self.get_interpreter(interpreter_name).get(key_name, default)

    def get_interpreter_config(self, interpreter_name):
        return self.get_interpreter(interpreter_name).root_config

    def __repr__(self):

        result = OrderedDict()
        result["full_config"] = self.config

        interpreters = {}
        for i_name, i in self._interpreters.items():
            interpreters[i_name] = i.config

        result["interpreters"] = interpreters

        return pprint.pformat(result)

    def save_current(self, target_file, force=False, sort=True):

        if os.path.exists(target_file) and not force:
            raise Exception("File already exists: {}".format(target_file))

        conf = self.config
        if conf is None:
            conf = {}

        ensure_parent_dir(target_file)

        if sort:
            result = CommentedMap()
            for k in sorted(conf):
                result[k] = conf[k]
        else:
            result = conf

        with io.open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(result, f)

        return True


class CnfInterpreter(Cnf):
    def __init__(
        self,
        parent_cnf,
        schema,
        doc_key=None,
        target_attr_key="target_key",
        validator=None,
    ):
        super(CnfInterpreter, self).__init__(parent_cnf.config, cnf_plugins=None)
        self._parent_cnf = parent_cnf

        self._schema = schema
        self._docs = {}
        if doc_key is not None:
            for key, value in self._schema.items():
                self._docs[key] = Doc(value.pop(doc_key, None))

        self._target_attr_map = {}
        if target_attr_key is not None:
            for key, value in self._schema.items():
                if target_attr_key in value.keys():
                    self._target_attr_map[key] = value.pop(target_attr_key)

        self._tags = {}
        for key, value in self._schema.items():
            tags = value.pop("tags", [])
            self._tags[key] = tags

        self._validated = None
        if validator is None:
            validator = self._parent_cnf.validator
        self.validator = validator

    def _invalidate(self):

        self._validated = None
        self._invalidate_interpreters()

    @property
    def root_config(self):
        return self._parent_cnf.config

    @root_config.setter
    def root_config(self, value):
        raise Exception("Modification of non-root config not allowed.")

    @property
    def config(self):

        if self._validated is not None:
            return self._validated

        if self.root_config is None:
            return None

        self._validated = self._validate(self.root_config)
        return self._validated

    def overlay(self, *additional_dicts):

        if not additional_dicts:
            return self._validate(self.root_config)
        else:
            return self._validate(self.root_config, *additional_dicts)

    def _validate(self, *dicts):

        c_dict = {}

        for d in dicts:
            dict_merge(c_dict, d, copy_dct=False)

        validator = self.validator(self.schema, purge_unknown=True)

        validated = validator.validated(c_dict)
        if validated is None:
            raise CnfValidationException(self, None, validator.errors)

        if not self._target_attr_map:
            return validated

        temp = copy.deepcopy(validated)
        remove_keys = []
        for key, value in self._target_attr_map.items():
            if key in validated.keys():
                orig = validated[key]
                if isinstance(value, six.string_types):
                    value = [value]
                for v in value:
                    temp[v] = orig
                if key not in value:
                    remove_keys.append(key)

        for key in remove_keys:
            temp.pop(key)

        return temp

    def get(self, key, default=None):

        return self.config.get(key, default)

    def get_tags(self, key):

        if self._target_attr_map:
            for k, v in self._target_attr_map.items():
                if v == key:
                    key = k
                    break

        if key not in self._tags.keys():
            raise Exception("Invalid key name: {}".format(key))

        return self._tags.get(key)

    @property
    def docs(self):
        return self._docs

    def get_doc_for_key(self, key):
        doc = self._docs.get(key, None)
        if doc is None:
            for k, v in self._target_attr_map.items():
                if v == key:
                    doc = self._docs[k]
                    break

        return doc

    def get_schema_for_key(self, key):

        return self._schema.get(key, None)

    @property
    def schema(self):
        return self._schema


@six.add_metaclass(abc.ABCMeta)
class CnfPlugin(object):
    """Parent class for context plugins.

    A context plugin parses/modifies a configuration key/value pair before it forwards it to the :class:~Cnf class.
    """

    def __init__(self, **kwargs):

        pass

    @abc.abstractmethod
    def handles_keys(self):
        """Returns a list of key names this plugin handles."""

    @abc.abstractmethod
    def set_value(self, key, value, current_conf):
        """Sets a certain config value.

        Throws a :class:`~FrecklesConfigException` if invalid config key/values are specified.

        Args:
            key (str): the original key
            value: the original value
            current_config (dict): copy of current config, for read purposes

        Returns:
            dict: a dictionary that will be overlayed on top of the current config, or None
        """

        pass
