"""Bloqly API"""

__version__ = '0.4'

import hashlib

import nacl.signing
from nacl.encoding import Base64Encoder, Base16Encoder


def sign_transaction(private_key, space, tag, nonce, timestamp, value, memo=''):
    signing_key = nacl.signing.SigningKey(private_key, encoder=Base64Encoder)

    data = \
        space.encode('utf-8') + \
        tag.encode('utf-8') + \
        nonce.to_bytes(8, 'big', signed=False) + \
        timestamp.to_bytes(8, 'big', signed=False) + \
        memo.encode('utf-8') + \
        value.encode('utf-8')

    m = hashlib.sha256()
    m.update(data)
    tx_hash = m.digest()

    signed_message = signing_key.sign(tx_hash, encoder=Base64Encoder)

    signature = signed_message.signature.decode('utf-8')

    verify_key = signing_key.verify_key

    public_key = Base64Encoder.encode(bytes(verify_key))

    signed_transaction = {
        'space': space,
        'tag': tag,
        'nonce': nonce,
        'timestamp': timestamp,
        'memo': memo,
        'value': value,
        'hash': Base16Encoder.encode(tx_hash).decode('utf-8'),
        'signature': signature,
        'public_key': public_key.decode('utf-8')
    }

    return signed_transaction


def encode_transaction(signed_transaction):
    tx_json = str(signed_transaction).replace('\'', '"').encode('utf-8')

    tx_bytes = bytes(tx_json)

    encoded_transaction = Base64Encoder.encode(tx_bytes).decode('utf-8')

    return encoded_transaction
