#!/usr/bin/env python
# encoding: utf-8
import binascii
import sha3
from ecdsa import SigningKey, SECP256k1
from web3 import Web3


def generate_address_and_private_key():
    private = SigningKey.generate(curve=SECP256k1)
    public = private.get_verifying_key()

    keccak = sha3.keccak_256()
    keccak.update(public.to_string())

    address = Web3.toChecksumAddress('0x{}'.format(keccak.hexdigest()[24:]))
    private_key = binascii.hexlify(private.to_string()).decode()

    return address, private_key
