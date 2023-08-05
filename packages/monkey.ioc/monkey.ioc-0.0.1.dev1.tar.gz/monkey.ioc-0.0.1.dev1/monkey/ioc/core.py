#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import glob
import json
import os
import sys

_DEFINITION_KEY = 'def'
_INSTANCE_KEY = 'inst'
_MODULE_KEY = 'module'
_CLASS_KEY = 'class'
_PARAMETERS_KEY = 'parameters'
_TYPE_KEY = 'type'
_PARAM_LABEL_KEY = 'label'
_PARAM_VALUE_KEY = 'value'
_REFERENCE_KEY = 'ref'
_PARAM_FORMAT_KEY = 'format'
_FACTORY_KEY = 'factory'
_METHOD_KEY = 'method'

_INCLUDE_KEY = 'include'

_DEFAULT_DATE_FORMAT_PATTERN = '%Y-%m-%d'
_DEFAULT_DATETIME_FORMAT_PATTERN = '%Y-%m-%dT%H:%M:%S'
_DEFAULT_TIME_FORMAT_PATTERN = '%H:%M:%S'


class Registry:

    def __init__(self):
        self.entries = {}
        self.constants = {}

    def load(self, file_path):
        with open(file_path, 'r') as file:
            entry_defs = json.load(file)
            for key, value in entry_defs.items():
                if key == _INCLUDE_KEY:
                    for file_path_pattern in value:
                        include_file_paths = glob.glob(file_path_pattern, recursive=True)
                        for include_file_path in include_file_paths:
                            self.load(include_file_path)
                else:
                    self.entries[key] = {_DEFINITION_KEY: value}

    def get(self, key, default=None):
        entry = self.entries.get(key, default)
        inst = entry.get(_INSTANCE_KEY, None)
        if inst is None:
            inst_def = entry.get(_DEFINITION_KEY, None)
            inst = self._build_inst(inst_def)
            self.entries[key][_INSTANCE_KEY] = inst
        return inst

    def _build_inst(self, inst_def):
        if _TYPE_KEY in inst_def:
            # inst_type = inst_def[_TYPE_KEY]
            inst = self._build_param(inst_def)
        else:
            params = inst_def[_PARAMETERS_KEY]
            if _FACTORY_KEY in inst_def:
                factory_inst = self.get(inst_def[_FACTORY_KEY])
                factory_method_name = inst_def[_METHOD_KEY]
            elif _CLASS_KEY in inst_def:
                module_name = inst_def[_MODULE_KEY]
                if module_name not in sys.modules:
                    __import__(module_name)
                factory_inst = sys.modules[module_name]
                # For creation by class instantiation, we use the class name as factory method name
                factory_method_name = inst_def[_CLASS_KEY]
            elif _METHOD_KEY in inst_def:
                module_name = inst_def[_MODULE_KEY]
                if module_name not in sys.modules:
                    __import__(module_name)
                factory_inst = sys.modules[module_name]
                factory_method_name = inst_def[_METHOD_KEY]
            elif _TYPE_KEY in inst_def:
                factory_inst = self
                factory_method_name = '_build_param'
                params = inst_def
            else:
                raise NotImplementedError('Requires one of supported creation method:'
                                          '\r\n\t- Class instantiation'
                                          '\r\n\t- Factory method call on object instance'
                                          '\r\n\t- Factory method call on module.'
                                          )
            inst = self._call_factory_method(factory_inst, factory_method_name, params)
        return inst

    def _call_factory_method(self, factory_inst, factory_method_name, param_defs):
        params = self._build_params(param_defs)
        factory_method = getattr(factory_inst, factory_method_name)
        inst = factory_method(*params)
        return inst

    def _build_params(self, param_defs):
        params = []
        for param_def in param_defs:
            param = self._build_param(param_def)
            params.append(param)
        return params

    def _build_param(self, param_def):
        try:
            param_type = param_def[_TYPE_KEY]
            factory_method_name = '_build_{}_param'.format(param_type)
            factory_method = getattr(self, factory_method_name)
            param = factory_method(param_def)
            return param
        except TypeError as e:
            raise e

    def _build_str_param(self, param_def) -> str:
        value = param_def[_PARAM_VALUE_KEY]
        return str(value)

    def _build_float_param(self, param_def) -> float:
        value = param_def[_PARAM_VALUE_KEY]
        return float(value)

    def _build_int_param(self, param_def) -> int:
        value = param_def[_PARAM_VALUE_KEY]
        return int(value)

    def _build_date_param(self, param_def) -> datetime.date:
        date_format_pattern = param_def.get(_PARAM_FORMAT_KEY, _DEFAULT_DATE_FORMAT_PATTERN)
        value = param_def[_PARAM_VALUE_KEY]
        return datetime.datetime.strptime(value, date_format_pattern).date()

    def _build_datetime_param(self, param_def) -> datetime.datetime:
        date_format_pattern = param_def.get(_PARAM_FORMAT_KEY, _DEFAULT_DATETIME_FORMAT_PATTERN)
        value = param_def[_PARAM_VALUE_KEY]
        return datetime.datetime.strptime(value, date_format_pattern)

    def _build_time_param(self, param_def) -> datetime.time:
        date_format_pattern = param_def.get(_PARAM_FORMAT_KEY, _DEFAULT_TIME_FORMAT_PATTERN)
        value = param_def[_PARAM_VALUE_KEY]
        return datetime.datetime.strptime(value, date_format_pattern).time()

    def _build_ref_param(self, param_def):
        key = param_def[_PARAM_VALUE_KEY]
        return self.get(key)

    def _build_list_param(self, param_def):
        param = []
        value_defs = param_def[_PARAM_VALUE_KEY]
        for value_def in value_defs:
            value = self._build_param(value_def)
            param.append(value)
        return param

    def _build_map_param(self, param_def):
        # Only accept native Python/JSON types
        return param_def[_PARAM_VALUE_KEY]

    def _build_dict_param(self, param_def):
        # Accept param definition as map values
        param_def_value = param_def[_PARAM_VALUE_KEY]
        param_dict = {}
        for key, value in param_def_value.items():
            p = self._build_param(value)
            param_dict[key] = p
        return param_dict

    def _build_envvar_param(self, param_def):
        envvar_name = param_def[_PARAM_VALUE_KEY]
        try:
            value = os.environ[envvar_name]
        except IndexError:
            value = None
        return value
