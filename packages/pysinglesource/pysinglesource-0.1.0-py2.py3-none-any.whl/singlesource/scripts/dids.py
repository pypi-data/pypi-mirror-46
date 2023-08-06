# -*- coding: utf-8 -*-
"""
Module providing an entry point to DID/identifier operations via a CLI.
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
import base64
import logging
from typing import Optional

from singlesource.dids import (generate_id,
                               make_did_document,
                               api_register_did_document)


logger = logging.getLogger(__name__)


def generate_did(identifier: Optional[str] = None,
                 pub_key: Optional[bytes] = None,
                 id_type: str = 'did'):
    """
    Generate a (decentralised) identifier from a unique identifier.

    :param identifier: The specific identifier to use, usually a blockchain
        address (e.g. an encoded public key).
    :param pub_key: Base64 encoded public signing key. Currently only supported
        for Ed25519 keys.
    :param id_type: Identifier type, defaulting to a DID (decentralised
        identifier).
    """
    if identifier:
        print(generate_id(identifier=identifier, id_type=id_type))
    elif pub_key:
        print(generate_id(public_key=base64.b64decode(pub_key),
                          id_type=id_type))
    else:
        raise ValueError('Either an identifier or a public key is required'
                         ' to generate a DID.')


def generate_did_document_from_signing_key(did: str, pub_key: str,
                                           did_doc_file: str):
    """
    Generate a DID document from a public (Ed25519) signing key.

    :param did: Decentralised identifier.
    :param pub_key: Base64 encoded public signing key. Currently only supported
        for Ed25519 keys.
    :param did_doc_file: File to write the DID document to.
    """
    public_keys = [
        {'key_type': 'Ed25519VerificationKey2018',
         'public_key': base64.b64decode(pub_key),
         'authentication_type': 'Ed25519SignatureAuthentication2018'}
    ]
    with open(did_doc_file, 'wt') as fd:
        fd.write(make_did_document(did, public_keys))


def register_did_document_api(did: str, did_doc_file: str):
    """
    Register a DID document with the DID registry (API).

    This is an interim (centralised) solution using a centralised DID registry
    implemented via a REST API.

    :param did: Decentralised identifier.
    :param did_doc_file: File containing the DID document for registration.
    """
    with open(did_doc_file, 'rt') as fd:
        api_register_did_document(did, fd.read())


def main(args: argparse.Namespace):
    """
    Delegate to the right functions from given (command line) arguments.

    :param args: Command line arguments provided:

        - args.id_type - type: str
        - args.address - type: str
        - args.did - type: str
        - args.pub_sig_key - type: str
        - args.did_document - type: str
    """
    if args.operation == 'generate':
        if args.address:
            generate_did(identifier=args.address, id_type=args.id_type)
        elif args.pub_sig_key:
            generate_did(pub_key=args.pub_sig_key, id_type=args.id_type)
        else:
            raise ValueError('Either an identifier or a public key is required'
                             ' to generate a DID.')
    elif args.operation == 'makedoc':
        generate_did_document_from_signing_key(args.did, args.pub_sig_key,
                                               args.did_document)
    elif args.operation == 'register':
        register_did_document_api(args.did, args.did_document)
    elif args.operation == 'resolve':
        raise NotImplementedError('DID operation not implemented, yet: {}'
                                  .format(args.operation))
    else:
        raise ValueError('Unsupported operation "{}" for DIDs.'
                         .format(args.operation))

    logger.info('Operation "{}" finished.'.format(args.operation))
