#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from secure_dict import SecureDict, InvalidData


rsa1 = RSA.generate(1024)
priv_rsa = rsa1
pub_rsa = rsa1.publickey()

rsa2 = RSA.generate(1024)
priv_rsa2 = rsa2
pub_rsa2 = rsa2.publickey()


def test_set_and_get():
    sd = SecureDict(priv_rsa, pub_rsa)
    sd['foo'] = 'bar'
    assert sd.export()['foo'] != 'bar'
    assert sd['foo'] == 'bar'


def test_set_and_get_fail():
    sd = SecureDict(priv_rsa, pub_rsa2)
    sd['foo'] = 'bar'
    assert sd.export()['foo'] != 'bar'
    try:
        sd['foo'] != 'bar'
    except InvalidData:
        pass


def test_set():
    sd = SecureDict(None, pub_rsa)
    sd['foo'] = 'bar'
    assert sd.export()['foo'] != 'bar'
    try:
        sd['foo'] == 'bar'
    except AttributeError:
        pass


def test_load_existing():
    sd = SecureDict(None, pub_rsa)
    sd['foo'] = 'bar'
    data = sd.export()

    assert data['foo'] != 'bar'

    sd2 = SecureDict(priv_rsa, None, data)
    assert sd2['foo'] == 'bar'


def test_load_existing_fail():
    sd = SecureDict(None, pub_rsa)
    sd['foo'] = 'bar'
    data = sd.export()

    assert data['foo'] != 'bar'

    sd2 = SecureDict(priv_rsa2, None, data)
    try:
        sd2['foo'] != 'bar'
    except InvalidData:
        pass


def test_multi_types():
    data = {
        "a": 1,
        "b": ("a", 5),
        "c": None,
        "d": {"foo": "bar"},
        "e": 192.1223411231,
    }
    sd = SecureDict(priv_rsa, pub_rsa)
    sd.update(data)
    for k, v in data.items():
        assert v != sd.export()[k]
        assert v == sd[k]


def test_update():
    data = {
        "foo": "bar",
        "a": "b",
        "c": "d",
    }
    sd = SecureDict(priv_rsa, pub_rsa)
    sd.update(data)
    for k, v in data.items():
        assert v != sd.export()[k]
        assert v == sd[k]
