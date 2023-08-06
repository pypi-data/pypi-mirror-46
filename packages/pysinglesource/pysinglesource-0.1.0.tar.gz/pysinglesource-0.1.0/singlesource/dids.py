# -*- coding: utf-8 -*-
"""DID handling support."""

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

import base64
import json
import nacl.hash
from typing import Optional, Iterable, Dict

import base58
import nacl.encoding
import nacl.utils

from singlesource import utils
from singlesource.config import config  # noqa: F401 # @UnusedImport


# To load the default configuration.
_IDENTIFIER_FORMAT = '{}:ssid:{}'
_IMID_SIZE = 32
_ADDRESS_TYPE = b'*'  # 42: CENNZnet address type.
_ADDRESS_TYPE_IMID = b'?'  # 63: Last unreserved of Substrate.
_PREFIX = b'SS58PRE'
_CHECKSUM_SIZE = 2
_DIGEST_LENGTH = 64
_DID_DOC_SKELETON = {
    '@context': 'https://w3id.org/did/v1',
    'id': None,
    'publicKey': [],
    'authentication': []
}


def generate_id(identifier: Optional[str] = None,
                public_key: Optional[bytes] = None,
                id_type: str = 'did') -> str:
    """
    Generate a (decentralised) identifier from a unique identifier.

    :param identifier: The specific identifier to use, usually a blockchain
        address (e.g. an encoded public key).
    :param public_key: The public key to use for generating an identifier.
    :param id_type: Identifier type, defaulting to a DID (decentralised
        identifier).
    :return: Identifier representation usable in the decentralised environment.
    """
    if id_type not in ('did', 'imid'):
        raise ValueError('Identifier type unknow/unsupported: {}'
                         .format(id_type))
    if not identifier:
        if id_type == 'did':
            identifier = _get_address_from_pub_key(public_key)
        elif id_type == 'imid':
            imid_raw = nacl.utils.random(_IMID_SIZE)
            identifier = _get_address_from_pub_key(imid_raw, id_type=id_type)
    return _IDENTIFIER_FORMAT.format(id_type, identifier)


def _get_address_from_pub_key(pub_key: bytes, id_type: str = 'did') -> str:
    """
    Generate an address (blockchain address) from the public key.

    TODO: This needs potential fixing, as the checksum doesn't pan out.

    :param pub_key: Public key or identifier bytes to use for generation.
    :param id_type: Identifier type, defaulting to a DID (decentralised
        identifier).
    :return: Identifier representation usable in the decentralised environment.
    """
    address_type = _ADDRESS_TYPE if id_type == 'did' else _ADDRESS_TYPE_IMID
    payload = address_type + pub_key
    checksum = nacl.hash.blake2b(_PREFIX + payload, digest_size=_DIGEST_LENGTH,
                                 encoder=nacl.encoding.RawEncoder)
    complete = payload + checksum[:_CHECKSUM_SIZE]
    return base58.b58encode(complete).decode('utf-8')


def make_did_document(did: str, public_keys: Iterable[Dict]) -> str:
    """
    Generate a DID document from a DID and public keys.

    This is to suffice the needs of the `api_register_did_document()` function
    in this module.

    :param did: Decentralised identifier.
    :param public_keys: Iterable containing the public keys in order of
        listing in the DID document (for anchors, starting to count from 1).
        `key_type` and `public_key` must be present for each key. Keys
        containing `authentication_type` will be registered as authentication
        keys with their given type.
    :return: DID document as a JSON string.
    """
    did_document = _DID_DOC_SKELETON.copy()
    did_document['id'] = did
    for i, pub_key in enumerate(public_keys):
        index = i + 1  # We're starting to count from 1 in the DID document.
        key_id = '{}#key{}'.format(did, index)
        key_record = {
            'id': key_id,
            'type': pub_key['key_type'],
            'controller': did,
            'publicKeyBase64': base64.b64encode(pub_key['public_key']).decode()
        }
        did_document['publicKey'].append(key_record)
        if pub_key.get('authentication_type'):
            auth_record = {
                'type': pub_key['authentication_type'],
                'publicKey': key_id
            }
            did_document['authentication'].append(auth_record)
    return json.dumps(did_document)


def api_register_did_document(did: str, did_document: str):
    """
    Register a DID document with the DID registry.

    This is an interim (centralised) solution using a centralised DID registry
    implemented via a REST API.

    :param did: Decentralised identifier.
    :param did_document: DID document to register.
    """
    resource = '{}/{}'.format(config.did_registry_resource_path, did)
    response = utils.request_api(base_url=config.did_registry_base_url,
                                 resource=resource, body=did_document,
                                 method='PUT')
    if response.status_code != 204:
        raise RuntimeError('Error registering the DID with the registry: {} {}'
                           .format(response.status_code, response.content))
