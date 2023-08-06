# -*- coding:utf-8 -*-

import hashlib


def _gen_hash_text_func(fn):
    def _hash_text(text):
        o = getattr(hashlib, fn)
        h = o()
        _hash_text.func_name = fn
        h.update(text)
        return h.hexdigest().lower()
    return _hash_text


def _gen_hash_file_func(fn):
    def _hash_file(filename):
        o = getattr(hashlib, fn)
        h = o()
        with open(filename, 'rb') as fo:
            while True:
                ch = fo.read(1)
                if not ch:
                    break
                h.update(ch)
            _hash_file.func_name = fn
        return h.hexdigest().lower()
    return _hash_file


md5 = _gen_hash_text_func('md5')
sha1 = _gen_hash_text_func('sha1')
sha224 = _gen_hash_text_func('sha224')
sha256 = _gen_hash_text_func('sha256')
sha384 = _gen_hash_text_func('sha384')
sha512 = _gen_hash_text_func('sha512')

md5_file = _gen_hash_file_func('md5')
sha1_file = _gen_hash_file_func('sha1')
sha224_file = _gen_hash_file_func('sha224')
sha256_file = _gen_hash_file_func('sha256')
sha384_file = _gen_hash_file_func('sha384')
sha512_file = _gen_hash_file_func('sha512')
