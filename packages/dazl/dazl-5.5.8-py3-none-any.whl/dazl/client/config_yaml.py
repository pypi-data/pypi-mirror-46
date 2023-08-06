# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains functions for assisting in parsing the YAML version of the configuration file.
This module requires the ``yaml`` module to be available.
"""

from ..model.core import ConfigurationError
from .config import LedgerConfiguration, LedgerNodeConfiguration


def parse_yaml_config(buf, yaml_load=None) -> LedgerConfiguration:
    """
    Attempt to parse the specified buffer as a YAML configuration file. Return a
    :class:`LedgerPartyConfiguration` object from the config file.
    """

    if yaml_load is None:
        try:
            import yaml
        except ImportError:
            raise ConfigurationError(['Loading YAML config requires a dependency to the `PyYAML` module'])
        yaml_load = yaml.load

    config = yaml_load(buf)
    return parse_yaml_config_dict(config)


def parse_yaml_config_file(path: str) -> LedgerConfiguration:
    """
    Attempt to parse a file at the specified path as a YAML configuration file.
    """
    with open(path, 'r') as buf:
        return parse_yaml_config(buf)


def parse_yaml_config_url(url: str) -> LedgerConfiguration:
    """
    Attempt to parse a file at the specified path as a YAML configuration file.
    """
    import urllib.request
    with urllib.request.urlopen(url) as buf:
        return parse_yaml_config(buf)


def parse_yaml_config_dict(yaml_dict: dict) -> LedgerConfiguration:
    """
    Parse a config object in YAML format.
    """

    config = LedgerConfiguration()

    for topology in yaml_dict.values():
        participant_nodes = topology.get('participants')
        for _, value in participant_nodes.items():
            node_config = LedgerNodeConfiguration()
            node_config.parties = value.get('names', '').split(',')
            node_config.url = _parse_url(value['server'])
            config.nodes.append(node_config)

    return config


def _parse_url(url_dict):
    from urllib.parse import urlunparse

    if url_dict is None:
        return None

    if isinstance(url_dict, str):
        return url_dict

    protocol = url_dict.get('scheme', 'http')
    netloc = url_dict.get('host')
    port = url_dict.get('port')
    path = url_dict.get('context_path', '')
    version = url_dict.get('version', '')

    if netloc is not None and port is not None:
        netloc = '{}:{}'.format(netloc, port)

    path = path.rstrip('/')
    if not path.startswith('/'):
        path = '/' + path

    # TODO: The only reason this is required is because we have inconsistent convention in our URLs.
    # Take the version string (if present) and lop it off the back part of the URL.
    version = version.rstrip('/')
    if not version.startswith('/'):
        version = '/' + version
    if path and version:
        if path.endswith(version):
            path = path[0:-len(version)]

    url_tuple = (protocol, netloc, path, '', '', '')
    return urlunparse(url_tuple)
