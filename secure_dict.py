#!/usr/bin/env python3
"""
http://pycryptodome.readthedocs.org/en/latest/src/examples.html
"""
import pickle


class InvalidData(Exception):
    pass


class SecureDict(dict):
    def __init__(self, private_key=None, public_key=None, data=None,
                 serializer=pickle):
        self.private_key = private_key
        self.public_key = public_key
        self.serializer = serializer
            self.
        super().__init__(data or {})

    def decryptvalue(self, value_secured):
        serialized = self.private_key.decrypt(value_secured)
        try:
            return self.serializer.loads(serialized)
        except Exception:
            raise InvalidData

    def encryptvalue(self, value):
        serialized = self.serializer.dumps(value)
        return self.public_key.encrypt(serialized, None)

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
