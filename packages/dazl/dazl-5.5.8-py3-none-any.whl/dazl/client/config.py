# Copyright (c) 2019 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
This module contains configuration parameters used by the rest of the library.
"""

import warnings
from typing import Optional

from .. import LOG
from ..model.core import ConfigurationError
from ..util.config_meta import Configuration, ConfigParameter, \
    COUNT_TYPE, LOG_LEVEL_TYPE, PARTIES_TYPE, PATH_TYPE, PORT_TYPE, SECONDS_TYPE, STRING_TYPE, \
    URL_TYPE, VERIFY_SSL_TYPE


# If this environment variable is set, is used in place of a configuration file if none is supplied
# on the command-line.
DAZL_CONFIG_ENV = 'DAZL_CONFIG'


class LedgerPartyConfiguration(Configuration):
    """
    Configuration for a specific party's client.
    """

    url = ConfigParameter(
        'URL where the Ledger API is hosted',
        param_type=URL_TYPE,
        short_alias='u',
        environment_variable='DAML_LEDGER_URL',
        deprecated_alias='participant_url')

    admin_url = ConfigParameter(
        'URL where administrative functions are exposed',
        param_type=URL_TYPE,
        environment_variable='DAML_LEDGER_ADMIN_URL',
        default_value=None)

    ca_file = ConfigParameter(
        'server certificate authority file',
        param_type=PATH_TYPE,
        default_value=None)

    cert_file = ConfigParameter(
        'client certificate file',
        param_type=PATH_TYPE)

    cert_key_file = ConfigParameter(
        'client certificate and key file',
        param_type=PATH_TYPE)

    verify_ssl = ConfigParameter(
        'level of verification to use for SSL',
        param_type=VERIFY_SSL_TYPE)

    poll_interval = ConfigParameter(
        'polling interval for receiving new events',
        param_type=SECONDS_TYPE,
        default_value=0.1)

    connect_timeout = ConfigParameter(
        'number of seconds before giving up on a connection',
        param_type=SECONDS_TYPE,
        default_value=120)

    application_name = ConfigParameter(
        'The name that this application uses to identify itself to the ledger.',
        param_type=STRING_TYPE,
        default_value='DAZL-Client')

    max_event_block_size = ConfigParameter(
        'Maximum number of blocks to read in a single call.',
        param_type=COUNT_TYPE,
        default_value=100)

    max_command_batch_size = ConfigParameter(
        'Maximum number of commands to batch up in a single transaction',
        param_type=COUNT_TYPE,
        default_value=100)

    max_command_batch_timeout = ConfigParameter(
        'Maximum number of seconds to wait before sending out a command',
        param_type=SECONDS_TYPE,
        default_value=0.25)

    party_groups = ConfigParameter(
        'comma-separated list of broadcast parties',
        param_type=PARTIES_TYPE)


class LedgerConfiguration(Configuration):
    """
    Configuration for the entire client library and all connected parties.
    """

    log_level = ConfigParameter(
        'logging level for events for this party',
        param_type=LOG_LEVEL_TYPE,
        environment_variable='DAZL_LOG_LEVEL',
        short_alias='l')

    max_connection_count = ConfigParameter(
        'Number of concurrent HTTP connections to have outstanding.',
        param_type=COUNT_TYPE,
        default_value=20),

    quiet_timeout = ConfigParameter(
        'Number of seconds to wait after the client "thinks" it\'s done to hang around for',
        param_type=SECONDS_TYPE,
        default_value=1)

    idle_timeout = ConfigParameter(
        'Maximum number of seconds of idle activity before automatically closing the client',
        param_type=SECONDS_TYPE,
        default_value=120)

    max_consequence_depth = ConfigParameter(
        'The maximum number of times to wait for all parties to arrive at the same offset' +
        'before failing with an error',
        param_type=COUNT_TYPE,
        default_value=50)

    server_host = ConfigParameter(
        'Server listening host. Used for OAuth web application flow callbacks.',
        param_type=STRING_TYPE)

    server_port = ConfigParameter(
        'Server listening port. Used for OAuth web application flow callbacks.',
        param_type=PORT_TYPE)

    oauth_client_id = ConfigParameter(
        'OAuth client ID',
        param_type=STRING_TYPE)

    oauth_client_secret = ConfigParameter(
        'OAuth client secret (implies web application flow or backend application flow)',
        param_type=STRING_TYPE)

    oauth_token = ConfigParameter(
        'OAuth token',
        param_type=STRING_TYPE)

    oauth_refresh_token = ConfigParameter(
        'OAuth refresh token',
        param_type=STRING_TYPE)

    oauth_id_token = ConfigParameter(
        'OpenID token (JWT formatted)',
        param_type=STRING_TYPE)

    oauth_token_uri = ConfigParameter(
        'OAuth token URL',
        param_type=STRING_TYPE)

    oauth_redirect_uri = ConfigParameter(
        'OAuth redirect URI (implies web application flow)',
        param_type=STRING_TYPE)

    oauth_auth_url = ConfigParameter(
        'OAuth auth URL (implies mobile application flow)',
        param_type=STRING_TYPE)

    oauth_legacy_username = ConfigParameter(
        'OAuth username (implies legacy application flow)',
        param_type=STRING_TYPE)

    oauth_legacy_password = ConfigParameter(
        'OAuth password (implies legacy application flow)',
        param_type=STRING_TYPE)

    nodes = ConfigParameter(
        'a list of node configurations')

    participant_defaults = ConfigParameter(
        'default values for otherwise unspecified nodes')

    def __init__(self, nodes=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = [LedgerNodeConfiguration(**node_kwargs) for node_kwargs in nodes]


class LedgerNodeConfiguration(LedgerPartyConfiguration):
    """
    Configuration for a participant node.
    """

    parties = ConfigParameter(
        'comma-separated list of parties serviced by a participant node',
        param_type=PARTIES_TYPE,
        short_alias='p',
        environment_variable='DAML_LEDGER_PARTY')


def configure_parser(arg_parser, config_file_support=False):
    """
    Add standard options to an arg parser (later to be extracted out by ``get_config``).
    """
    if config_file_support:
        from os import environ
        default_config = environ.get(DAZL_CONFIG_ENV)
        group = arg_parser.add_argument_group('Configuration Settings')
        group.add_argument('--config', help='path to a YAML config file', default=default_config)

    group = arg_parser.add_argument_group('Overall Settings')
    LedgerConfiguration.add_arguments(group)

    group = arg_parser.add_argument_group('Per-Party Settings')
    LedgerNodeConfiguration.add_arguments(group, action='append')

    return arg_parser


def parse_kwargs(*config, **kwargs) -> LedgerConfiguration:
    """
    Create a :class:`LedgerClientManager` for the configuration settings.

    :param config:
        Instances of :class:`LedgerConfiguration`` objects to merge together.
    :param kwargs:
        Configuration options that are accepted either at the global level or at the party level.
    :return:
        An instance of :class:`LedgerClientManager`.
    """
    configurations = list(config)
    if kwargs:
        ledger_config_kwargs = {}
        for key, param in LedgerConfiguration._parameters.items():
            if param.deprecated_alias in kwargs:
                warnings.warn(f'The {param.deprecated_alias} option is deprecated. '
                              f'Please use {key} instead.', DeprecationWarning)
                ledger_config_kwargs[key] = param.param_type.value_ctor(kwargs.pop(param.deprecated_alias))
            elif key in kwargs:
                ledger_config_kwargs[key] = param.param_type.value_ctor(kwargs.pop(key))

        node_config_kwargs = {}
        for key, param in LedgerNodeConfiguration._parameters.items():
            if param.deprecated_alias in kwargs:
                warnings.warn(f'The {param.deprecated_alias} option is deprecated. '
                              f'Please use {key} instead.', DeprecationWarning)
                node_config_kwargs[key] = param.param_type.value_ctor(kwargs.pop(param.deprecated_alias))
            elif key in kwargs:
                node_config_kwargs[key] = param.param_type.value_ctor(kwargs.pop(key))

        if kwargs:
            raise ValueError(f'unknown kwargs: {list(kwargs.keys())}')

        ledger_config = LedgerConfiguration(**ledger_config_kwargs)
        ledger_config.nodes.append(LedgerNodeConfiguration(**node_config_kwargs))

        configurations.append(ledger_config)

    return merge_configurations(*configurations)


def fetch_config(path_or_url: Optional[str]) -> Optional[str]:
    """
    Attempts to fetch a config file from what looks like either a path or a URL.

    :param path_or_url: A file path or a URL.
    :return: The body of the config file.
    """
    if not path_or_url:
        return None

    from urllib.parse import urlparse
    from urllib.request import urlopen, URLError, HTTPError

    u = urlparse(path_or_url)
    if not u.scheme or u.scheme == 'file':
        try:
            with open(u.path, 'r') as buf:
                config_str = buf.read()
        except FileNotFoundError:
            raise ConfigurationError([f'Config file not found: {u.path}'])
    else:
        try:
            with urlopen(path_or_url) as buf:
                config_str = buf.read().decode('utf8')
        except HTTPError as error:
            raise ConfigurationError([f'HTTP {error.code}: {path_or_url}'])
        except URLError as error:
            if isinstance(error.args[0], ConnectionRefusedError):
                raise ConfigurationError([f'HTTP unreachable: {path_or_url}'])
            else:
                raise ConfigurationError([error.args[0]])

    return config_str


def get_config(args, config_file_support=False):
    """
    Convert an ``argparse.Namespace`` to :class:`LedgerConfiguration`.
    """
    configs = []
    if config_file_support and args.config:
        from .config_yaml import parse_yaml_config_file, parse_yaml_config_url
        from urllib.parse import urlparse
        p = urlparse(args.config)
        if not p.scheme or p.scheme == 'file':
            configs.append(parse_yaml_config_file(p.path))
        else:
            configs.append(parse_yaml_config_url(args.config))
    configs.append(_get_config(args))
    return merge_configurations(*configs)


def validate_config(config: LedgerConfiguration) -> LedgerConfiguration:
    parties_missing_urls = set()
    failures = set()

    LOG.debug('Configuration: %s', config)

    if config.nodes:
        for node in config.nodes:
            if node.url:
                if not node.parties:
                    failures.add(f'A participant URL has no listed parties: {node.url}')
            elif node.parties:
                parties_missing_urls.update(node.parties)
            else:
                failures.add(f'A node configuration is missing a URL and a party list')

        if parties_missing_urls:
            failures.add(f'No URL specified for these parties: {sorted(parties_missing_urls)}')
    else:
        failures.add('At least one party and a URL must be specified')

    if failures:
        raise ConfigurationError(failures)

    return config


def _get_config(args):
    ledger_config = dict()
    node_configs = dict()

    for var in LedgerConfiguration._parameters:  #pylint: disable=W0212
        if hasattr(args, var):
            value = getattr(args, var)
            if value is not None:
                ledger_config[var] = getattr(args, var)

    # for party-specific configuration, expect a list for each provided value, and the positions
    # in the list line up to form a node configuration
    for var in LedgerNodeConfiguration._parameters:  #pylint: disable=W0212
        if hasattr(args, var):
            value = getattr(args, var)
            if value is not None:
                node_configs[var] = value

    nodes = []
    if node_configs:
        for idx in range(max(map(len, node_configs.values()))):
            current_node = dict()
            for key, values in node_configs.items():
                current_node[key] = values[idx]
            nodes.append(current_node)

    ledger_config['nodes'] = nodes
    return LedgerConfiguration(**ledger_config)


def merge_configurations(*configurations):
    config_class = type(configurations[0])
    config_params = dict()

    nodes = []
    for config in configurations:
        for key in config.keys():
            if key == 'nodes':
                nodes.extend(config['nodes'])
                config_params['nodes'] = nodes
            else:
                value = object.__getattribute__(config, key)
                if value is not None:
                    config_params[key] = value
    config_obj = config_class(**config_params)
    if nodes:
        config_obj.nodes.extend(nodes)
    return config_obj
