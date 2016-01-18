#!/usr/bin/env python3
import pickle
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


class InvalidData(Exception):
    pass


class SecureDict(dict):
    def __init__(self, private_key=None, public_key=None, data=None,
                 serializer=pickle, AES_bytes=32):
        """
        Create a dictionary-like object with RSA+AES encryption of it's data
        (NOTE: keys are in plaintext, data is serialized using the provided
        serializer).  In order to fill the object with data, a `public_key`
        must be provided.  In order to read from the object, a `private_key`
        must be provided.
        """
        self.private_key = PKCS1_OAEP.new(private_key)
        self.public_key = PKCS1_OAEP.new(public_key)
        self.serializer = serializer

        self.AES_bytes = AES_bytes

        data = data or {}
        try:
            self.session = self.private_key.decrypt(data['__session'])
        except KeyError:
            self.session = get_random_bytes(AES_bytes)
            data['__session'] = self.public_key.encrypt(self.session)
        super().__init__(data)

    def _aes(self, iv):
        return AES.new(self.session, AES.MODE_CFB, iv)

    def decryptvalue(self, value_secured):
        iv = value_secured[:16]
        data = value_secured[16:]
        aes = self._aes(iv)
        serialized = aes.decrypt(data)
        serialized = serialized[:-serialized[-1]]
        try:
            return self.serializer.loads(serialized)
        except Exception:
            raise InvalidData

    def encryptvalue(self, value):
        iv = get_random_bytes(16)
        serialized = self.serializer.dumps(value)
        length = 16 - (len(serialized) % 16)
        padding = bytes([length])*length
        aes = self._aes(iv)
        data = aes.encrypt(serialized + padding)
        return iv + data

    def __getitem__(self, key):
        value_secured = super().__getitem__(key)
        return self.decryptvalue(value_secured)

    def __setitem__(self, key, value):
        value_secured = self.encryptvalue(value)
        return super().__setitem__(key, value_secured)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self.__setitem__(k, v)

    def export(self):
        return super().copy()
