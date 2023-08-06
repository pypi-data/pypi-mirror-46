#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line (CLI) client for SingleSource operations.
"""

# Created: 2019-05-08 Guy K. Kloss <guy@mysinglesource.io>
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

import argparse
import logging

from sspyjose import Jose

from singlesource.config import config
from singlesource.scripts import (dids,
                                  attestations)


logger = logging.getLogger(__name__)

# Configure to use AES256-GCM as a default cipher for encryption.
# Current options: 'C20P' (ChaCha20/Poly1305), 'A256GCM' (AES256-GCM).
Jose.DEFAULT_ENC = config.default_enc


def _console():
    """
    Entry point for console execution.
    """
    # Set up logger.
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s\t%(name)s\t%(asctime)s %(message)s')

    # Create the top-level parser.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-commands')

    # Create the parser for the "claims" command.
    parser_dids = subparsers.add_parser(
        'dids', help='DID- or identifier-related operations')
    parser_dids.set_defaults(func=dids.main)
    parser_dids.add_argument(
        '--operation', type=str,
        help='Operation to perform, one of:'
             ' `generate`, `makedoc`, `register`, `resolve`.')
    parser_dids.add_argument(
        '--type', dest='id_type', type=str, default='did',
        help="Identifier type, one of: `did` (default), `imid`.")
    parser_dids.add_argument(
        '--address', type=str, default=None,
        help='Public address of identity (e.g. blockchain address).')
    parser_dids.add_argument(
        '--did', type=str, default=None,
        help='DID or public identifier of identity.')
    parser_dids.add_argument(
        '--did-doc', dest='did_document', type=str, default=None,
        help='File name for the DID document.')
    parser_dids.add_argument(
        '--pub-sig-key', dest='pub_sig_key', type=str, default=None,
        help='Base64 encoded public signing key (Ed25519).')

    # Create the parser for the "claims" command.
    parser_attestations = subparsers.add_parser(
        'attestations', help='Attestation-related operations')
    parser_attestations.set_defaults(func=attestations.main)
    parser_attestations.add_argument(
        '--operation', type=str,
        help='Operation to perform, one of:'
             ' `attest`, `xxx`.')
    parser_attestations.add_argument(
        '--subject', type=str, default=None,
        help="DID or public identifier of subject's identity.")
    parser_attestations.add_argument(
        '--attester-obo', dest='attester_obo', type=str, default=None,
        help='DID of the verifying party requesting the attestation'
             ' (default: from configuration).')
    parser_attestations.add_argument(
        '--statements', type=argparse.FileType('rt'), default=None,
        help='Attestation statements to use (default: from configuration).')
    parser_attestations.add_argument(
        '--claims', type=argparse.FileType('rt'), default=None,
        help='File for the claims.')
    parser_attestations.add_argument(
        '--attestation', type=str, default=None,
        help='File for the attestations.')

    # Now let's do the work.
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    _console()
