# -*- coding: utf-8 -*-
"""
Configuration settings for config files and defaults.

System and user level configuration files are detected and automatically
read. The configuration files are following a YAML syntax.
"""

# Created: 2019-03-15 Guy K. Kloss <guy@mysinglesource.io>
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
import sspyjose


class _Settings(object):
    """Default configuration options."""

    # ### General options.
    # Default time to live span of claims and attestations made.
    default_ttl = 365 * 24 * 3600  # 1 year in seconds.

    # ### Logging options.
    # Log level.
    log_level = logging.INFO
    # Log file name.
    log_file = '/var/log/pysinglesource/pysinglesource.log'
    # Maximal number of bytes per log.
    log_max_bytes = 2 * 1024 ** 2  # 2 MiB
    # Number of log backups for log rotation.
    log_backup_count = 5
    # Default cipher for encryption (`alg` value for JWE).
    # Current options: 'C20P' (ChaCha20/Poly1305), 'A256GCM' (AES256-GCM).
    default_enc = 'A256GCM'

    # ### Credentials.
    # OAuth client credentials.
    oauth_url = 'https://auth.mysinglesource.io/kym/login'
    oauth_consumer_key = None  # type: str
    oauth_consumer_secret = None  # type: str

    # ### API end-points.
    # DID registry REST API.
    did_registry_base_url = 'https://dev.mysinglesource.io'
    did_registry_resource_path = '/diddocuments'
    # KYM attestation REST API.
    kym_attestation_base_url = 'https://dev.mysinglesource.io'
    kym_attestation_resource_path = '/kymdevices'

    # ### KYM attestation defaults.
    # Default statements template for KYM devices.
    kym_default_statements = [
        {
            "ttl": 315360000,  # 10 years
            "metadata": {
                "kym_compliance": "device identity assurance, level 3",
                "governance": "IoT association"
            }
        }
    ]
    # Default entity/organisation on whose behalf the attestation will be made.
    kym_default_attester_obo = (
        'did:ssid:5E2J5Uqaf73CoKyD6itv4FcQvgVZ7nZR9rmmS3cCGbYNxEv7')

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

        sspyjose.Jose.DEFAULT_ENC = self.default_enc


config = _Settings('pysinglesource')
