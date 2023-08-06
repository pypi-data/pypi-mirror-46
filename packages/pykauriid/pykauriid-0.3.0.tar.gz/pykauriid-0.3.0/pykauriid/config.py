# -*- coding: utf-8 -*-
"""
Configuration settings for config files and defaults.

System and user level configuration files are detected and automatically
read. The configuration files are following a YAML syntax.
"""

# Created: 2018-10-05 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

import logging
import os
import yaml

import appdirs


class _Settings(object):
    """Default configuration options."""

    # ### General options.
    # Default time to live span of claims and attestations made.
    default_ttl = 365 * 24 * 3600  # 1 year in seconds.
    # Default time to live span for selective disclosure requests.
    default_request_ttl = 600  # 10 minutes in seconds.

    # ### Logging options.
    # Log level.
    log_level = logging.INFO
    # Log file name.
    log_file = '/var/log/pykauriid/pykauriid.log'
    # Maximal number of bytes per log.
    log_max_bytes = 2 * 1024 ** 2  # 2 MiB
    # Number of log backups for log rotation.
    log_backup_count = 5
    # Default cipher for encryption (`alg` value for JWE).
    # Current options: 'C20P' (ChaCha20/Poly1305), 'A256GCM' (AES256-GCM).
    default_enc = 'A256GCM'
    # Default cipher for signing (`alg` value for JWS).
    # Current options: 'Ed25519' only.
    default_sig = 'Ed25519'

    def __init__(self, appname: str):
        """
        Initialise the configuration.

        Defaults are overridden with system and/or user configurations.
        """
        config_paths = [appdirs.user_config_dir(appname),
                        appdirs.site_config_dir(appname)]

        for config_path in config_paths:
            if os.path.exists(config_path):
                file_config = yaml.load(open(config_path))
                for key, value in file_config.items():
                    setattr(self, key, value)


config = _Settings('pykauriid')
