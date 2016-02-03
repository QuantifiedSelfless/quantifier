from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from secretsharing import HexToHexSecretSharer


def create_keypair(passphrase=None, length=4096):
    rsa1 = RSA.generate(length)
    private_key = rsa1
    public_key = rsa1.publickey()
    private_exp = private_key.exportKey('PEM', passphrase=passphrase)
    public_exp = public_key.exportKey('PEM')
    return public_exp, private_exp


def generate_passphrase(length=32):
    pass_raw = get_random_bytes(length//2)
    return pass_raw.hex()


def split_passphrase(passphrase, share_threshold=2, num_shares=6):
    return HexToHexSecretSharer.split_secret(passphrase, share_threshold, num_shares)


def recover_passphrase(shares):
    return HexToHexSecretSharer.recover_secret(shares)
