# -*- coding:utf-8 -*-


from authlib.jose import JsonWebSignature


def serialize_compact(plaintext, key, kid):
    jws = JsonWebSignature(algorithms=['RS256'])
    protected = {'alg': 'RS256', 'kid': kid}
    payload = plaintext
    return jws.serialize_compact(protected, payload, key)


def deserialize_compact(ciphertext, key):
    jws = JsonWebSignature()
    return jws.deserialize_compact(ciphertext, key)
