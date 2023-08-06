# -*- coding: utf-8 -*-
"""Identity Request Service support."""

# Created: 2019-03-14 Guy K. Kloss <guy@mysinglesource.io>
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

import nacl.hash

import base58
import nacl.encoding
from sspyjose.jwk import Jwk

from singlesource.config import config  # noqa: F401 # @UnusedImport


# To load the default configuration.
_TOPIC_BYTES = 16


class EphemeralHandler:
    """
    Handler for ephemeral (single-use) communication.

    This handler is intended to be used with the ID Request Service and/or
    SingleSource messaging service.

    It provides a single-use encryption key pair for the user to receive
    confidential information with in returning messages. Additionally it
    provides a 'topic' that can be used with the SingleSource messaging
    service. This topic acts as a 'single-use post box', and is intended to
    be unguessable.
    """

    _ephemeral_jwk = None  # type: nacl.public.PrivateKey
    """Ephemeral X25519 key pair for public key content encryption."""

    def __init__(self, recovery_data: str = None):
        """
        Construct the ephemeral communication handler.

        An ephemeral handler can be de-serialised with the `recovery_data`
        parameter. This string representation can be stored elsewhere (e.g. a
        database). However, this serialised data is confidential and needs to
        be protected. It MUST NOT leak out, or the communication can be
        retrospectively decrypted by anybody who has intercepted the message
        and is in possession of this serialised recovery data.

        Note: The handler is supposed to be unguessable and for single-use
              and a particular purpose on the messaging service only. After
              completion, a new handler is to be used.

        :param recovery_data: Optional serialisation data that allows an
            ephemeral handler to be deserialised.
        """
        if recovery_data:
            self._deserialise(recovery_data)
        else:
            self._ephemeral_jwk = Jwk.get_instance(crv='X25519', generate=True)

    @property
    def messaging_topic(self) -> str:
        """
        Messaging service topic related to the ephemeral (public) key.

        Note: The topic is supposed to be unguessable and single-use for a
              particular purpose on the messaging service only.

        :return: Topic identifier.
        """
        pk_bytes = self._ephemeral_jwk.x
        hashed_pk = nacl.hash.sha256(bytes(pk_bytes),
                                     encoder=nacl.encoding.RawEncoder)
        return base58.b58encode(hashed_pk[:_TOPIC_BYTES]).decode('utf-8')

    def serialise(self) -> str:
        """
        Serialise the object to a bytes array.

        This allows an {EphemeralHandler} to be re-created after
        deserialisation.

        Note: The serialised data is confidential and needs to be protected.
              It MUST NOT leak out, or the communication can be retrospectively
              decrypted by anybody who has intercepted the message and this
              serialised handler.

        :return: Serialised content that allows the handler to be deserialised.
        """
        return base58.b58encode_check(self._ephemeral_jwk.d).decode('utf-8')

    def _deserialise(self, recovery_data: str):
        """
        Deserialise the state of an {EphemeralHandler} into this object.

        :param recovery_data: Serialised data to recover the state from.
        :raises: {ValueError} on checksum mismatch of `recovery_data`.
        """
        self._ephemeral_jwk = Jwk.get_instance(crv='X25519')
        private_key = base58.b58decode_check(recovery_data)
        self._ephemeral_jwk.d = private_key

    @property
    def private_key(self) -> bytes:
        """
        Bytes of the ephemeral private key.

        :return: Key bytes.
        """
        return self._ephemeral_jwk.d

    @property
    def public_key(self) -> bytes:
        """
        Bytes of the ephemeral public key.

        :return: Key bytes.
        """
        return self._ephemeral_jwk.x

    @property
    def jwk(self) -> Jwk:
        """
        JWK object of the ephemeral public key.

        :return: JWK.
        """
        return self._ephemeral_jwk
