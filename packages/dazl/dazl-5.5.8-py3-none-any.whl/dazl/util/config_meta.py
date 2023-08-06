# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains the metaclasses and other utilities required by :mod:`dazl.client.config`.
"""

import logging

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Dict, Optional, Sequence

from ..model.core import Party


@dataclass(frozen=True)
class ConfigParameter:
    description: str
    param_type: 'Optional[ConfigParameter]' = None
    default_value: Any = None
    short_alias: Optional[str] = None
    deprecated_alias: Optional[str] = None
    environment_variable: Optional[str] = None


@dataclass(frozen=True)
class ConfigParameterType:
    metavar: Optional[str]
    value_ctor: Callable[[Any], Any]


class ConfigurationMetaclass(type):
    """
    Metaclass for :class:`Configuration` subclasses. Handles the magic of converting a
    :class:`ConfigParameter` from a class parameter with metadata to actually providing field
    support on subclasses.
    """
    def __new__(mcs, name, base, dct):
        slots = []
        params = OrderedDict()
        default_object = dict()

        class_def = {}

        for key, value in dct.items():
            if isinstance(value, ConfigParameter):
                slots.append(key)
                params[key] = value
                default_object[key] = value.default_value
            else:
                class_def[key] = value

        for baseclass in base:
            params.update(baseclass._parameters)  # pylint: disable=W0212
            default_object.update(baseclass._defaults)  # pylint: disable=W0212

        slots = tuple(slots)
        class_def['__slots__'] = slots
        class_def['_parameters'] = params
        class_def['_defaults'] = default_object

        return super(ConfigurationMetaclass, mcs).__new__(mcs, name, base, class_def)


class Configuration(metaclass=ConfigurationMetaclass):
    """
    Base class for a class that manages configuration parameters.
    """

    _parameters = dict()  # type: ClassVar[Dict[str, ConfigParameter]]

    @classmethod
    def add_arguments(cls, parser, action=None):
        """
        Add arguments from this configuration object to an ``argparse.ArgumentParser``.

        :param parser:
            The ``argparse.ArgumentParser`` to add arguments to.
        :param action:
            The ``argparse`` action to use instead of the default (if specified).
        """
        for key, config_param in cls._parameters.items():
            if config_param.param_type is not None:
                aliases = ['--' + key.replace('_', '-')]
                if config_param.short_alias is not None:
                    aliases.append('-' + config_param.short_alias)
                if config_param.deprecated_alias is not None:
                    aliases.append('--' + config_param.deprecated_alias)

                if config_param.param_type.value_ctor == bool:
                    parser.add_argument(
                        *aliases,
                        help=config_param.description,
                        action='store_true')
                else:
                    parser.add_argument(
                        *aliases,
                        type=config_param.param_type.value_ctor,
                        metavar=config_param.param_type.metavar,
                        help=config_param.description,
                        action=action)

    def __init__(self, **kwargs):
        for key in self._parameters:
            setattr(self, key, kwargs.get(key))

    def __getattribute__(self, key):
        """
        Return the value of the specified attribute, or the default value if unset.
        """
        params = object.__getattribute__(self, '_parameters')
        if key in params:
            return self[key]
        else:
            return object.__getattribute__(self, key)

    def __getitem__(self, key):
        if key in self._parameters:
            value = object.__getattribute__(self, key)
            if value is not None:
                return value
            else:
                defaults = object.__getattribute__(self, '_defaults')
                return defaults[key]
        else:
            raise KeyError(key)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={!r}'.format(key, object.__getattribute__(self, key))
                      for key in self._parameters))

    def __iter__(self):
        return iter(self.keys())

    def keys(self):
        """
        Return the keys of this :class:`Configuration` object.
        """
        return list(self._parameters.keys())

    def extend(self, config_dict):
        for key, value in dict(config_dict).items():
            if key in self._parameters:
                setattr(self, key, value)


def _parse_url(obj):
    return obj


def _parse_log_level(obj) -> int:
    if not obj:
        return logging.WARNING
    if isinstance(obj, str):
        obj = obj.upper()
    p = logging.getLevelName(obj)
    return p


def _parse_str(obj: Any) -> Optional[str]:
    return str(obj) if obj is not None else None


def _parse_block_offset(obj):
    return obj


def _parse_party_list(obj) -> 'Sequence[Party]':
    if isinstance(obj, str):
        return [Party(p) for p in obj.split(',')]
    else:
        return obj


BOOLEAN_TYPE = ConfigParameterType(None, bool)
COUNT_TYPE = ConfigParameterType('COUNT', int)
BLOCK_OFFSET_TYPE = ConfigParameterType('OFFSET', _parse_block_offset)
LOG_LEVEL_TYPE = ConfigParameterType('LOG_LEVEL', _parse_log_level)
SECONDS_TYPE = ConfigParameterType('SECONDS', float)
URL_TYPE = ConfigParameterType('URL', _parse_url)
PARTIES_TYPE = ConfigParameterType('PARTIES', _parse_party_list)
PORT_TYPE = ConfigParameterType('PORT', int)
STRING_TYPE = ConfigParameterType('STRING', _parse_str)
PATH_TYPE = ConfigParameterType('PATH', _parse_str)
VERIFY_SSL_TYPE = ConfigParameterType('VERIFY_SSL', _parse_str)
