SingleSource Python SDK
=======================

The high level software development kit (SDK) to participate in the
decentralised SingleSource identity eco-system in Python.


Overview
--------

High level helpers available for:

* Identity Request Service (`idrs`) - Support for generating ephemeral
  encryption key pairs (X25519 ECDH), messaging service topics and
  serialisation/deserialisation of these.
* Attestations (`attestations`) - Making (foreign) claim sets and
  making attestations on them.


Installation
------------

To install use pip:

    $ pip install pysinglesource


Or clone the repo:

    $ git clone git@bitbucket.org:mysinglesource/pysinglesource.git
    $ python setup.py install

Set up and activate for Python 3:

    virtualenv ${HOME}/.virtualenvs/pysinglesource \
               --system-site-packages --python=/usr/bin/python3
    source ${HOME}/.virtualenvs/pysinglesource/bin/activate

Install required packages:

    pip install -e .

For installing the additional development, testing or documentation
dependencies, add a qualifier with one or more of these commands:

    pip install -e .[dev]       # Development dependencies
    pip install -e .[test]      # Testing dependencies
    pip install -e .[dev,test]  # All dependencies together


Usage
-----

### Identity Request Service Handler

When using the ID Request Service to create well-formed (selective
disclosure) requests, usually also a messaging service is used in
conjunction. Due to the sensitive nature, responses usually need to be
end-to-end encrypted, as the messaging service is not under the user's
control.

For this purpose an 'ephemeral handler' is available. It will generate
an ephemeral encryption key pair as well as a suitable messaging
service topic. The ephemeral handler can be serialised and
deserialised at ease to be persisted using strings (e.g. in any used
DB system).

Notes:

- The handler is supposed to be unguessable and for single-use and a
  particular purpose on the messaging service only. After completion,
  a new handler is to be used.
- The serialised data is confidential and needs to be protected.  It
  **MUST NOT** leak out, or the communication can be retrospectively
  decrypted by anybody who has intercepted the message and this
  serialised handler.

A receiving side would continuously poll on the messaging service
(e.g. every 2 seconds) using the handler's topic, checking for a
submitted response. The message returned then would contain encrypted
content, for which the ephemeral (private) key is required to access
it. Therefore, it makes sense to store the messaging service `topic`
under an indexed field, and the serialised handler value in the same
record.

```python
from singlesource import EphemeralHandler

handler = EphemeralHandler()

# Get the messaging topic for the Identity Request Service.
topic = handler.messaging_topic
# Get the serialised handler for storage (with the topic) in a DB.
serialised_data = handler.serialise()

# After receiving a response message with encrypted content, use the
# serialised handler to re-build it.
handler = EphemeralHandler(serialised_data)
# Get the encryption JWK object for use with encrypted message data.
jwk = handler.jwk
```


Contributing
------------

TBD


Example
-------

TBD


## Licence

Copyright 2018-2019 by SingleSource Limited, Auckland, New Zealand

This work is licensed under the Apache 2.0 open source licence.
Terms and conditions apply.
