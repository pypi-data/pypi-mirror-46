#!/usr/bin/env python3
# coding: utf8
# -----------------------------------------------------------------
# zeus: crypto.py
#
# provide cryptograhic functions
#
# Copyright (C) 2016-2019, Christophe Fauchard
# -----------------------------------------------------------------
"""
Submodule: zeus.crypto

provide cryptograhic functions

Copyright (C) 2016-2019, Christophe Fauchard
"""

import os
import base64
import random
import zeus.file
import hashlib as hash


class Vigenere():

    """
    Vigenere cipher

    can handle binary datas for both key and datas
    crypt datas are base64 coded for portability

    Required Parameters: None

    Optionnal Parameters:
    - string_key: key (utf8 string)
    - base64_key: key base64 encoded
    - file_key: filename containing the key (any binary datas allowed)
    - gen_key: generate a random binary key in the file given (4096 bytes)

    The key must be set by:
    - string_key parameter
    - file_key parameter
    - ZPK environment variable to store name of key file
    """

    def __init__(self,
                 string_key=None,
                 base64_key=None,
                 key_file=None,
                 gen_key=None,
                 key_size=None):

        self.key_file = key_file

        if key_size is None:
            key_size = 4096
        self.key_size = key_size

        #
        # generate a key in the file given
        #
        if gen_key is not None:
            self.key_file = gen_key
            self.genkey(output_file=gen_key,
                        size=self.key_size)

        #
        # read key from a file
        #
        elif key_file is not None and os.path.exists(key_file):
            f = open(key_file, 'rb')
            self.base64_key = f.read()
            self.key = base64.b64decode(self.base64_key)
            f.close()

        #
        # key given as an utf8 string
        #
        elif string_key is not None:
            self.key = bytearray(string_key.encode('utf8'))
            self.base64_key = base64.b64encode(self.key).decode('utf8')

        #
        # key given as an utf8 string
        #
        elif base64_key is not None:
            self.base64_key = base64_key
            self.key = base64.b64decode(self.base64_key)

        #
        # try to read ZPK environment variable
        # (contain private key path)
        #
        elif os.environ.get("ZPK") is not None:
            f = open(os.environ.get("ZPK"), 'rb')
            self.base64_key = f.read()
            self.key = base64.b64decode(self.base64_key)
            f.close()

        #
        # else generate a default key in memory
        #
        else:
            self.genkey()

    """
    Parameters:
    - decrypted_datas: decrypted message (utf8 string)
    or filename containing datas
    (if datas are stored in a file, it can contain any binary datas)

    Optionnal parameters:
    - output_filename: file to write encrypted output base64 encoded
    """

    def encrypt(self,
                decrypted_datas,
                output_file=None):

        self.load(decrypted_datas)

        self.crypted_datas = bytearray(self.decrypted_datas)
        j = 0
        for i in range(0, len(self.decrypted_datas)):
            if j == len(self.key):
                j = 0
            self.crypted_datas[i] = (self.decrypted_datas[i] +
                                     self.key[j]) % 256
            j += 1

        self.crypted_datas = base64.b64encode(self.crypted_datas)

        if output_file is not None:
            f = open(output_file, 'wb')
            f.write(self.crypted_datas)
            f.close()

        return(self)

    """
    load data to encrypt

    Parameters:
    - decrypted_datas: decrypted message (utf8 string)
    or filename containing datas
    (if datas are stored in a file, it can contain any binary datas)

    """
    def load(self, decrypted_datas):
        if os.path.exists(decrypted_datas):
            f = open(decrypted_datas, 'rb')
            self.decrypted_datas = f.read()
            f.close()
        else:
            self.decrypted_datas = bytearray(decrypted_datas.encode("utf8"))

        return(self)

    """
    decrypting encrypted datas passed, update decrypted_datas attribute

    Parameters:
    - encrypted_datas: encrypted message (base64 encoded ascii string) or
    filename containing datas

    Optionnal parameters:
    - output_filename: file to write decrypted output

    Exceptions:
    - binascii.Error: if encrypted datas are not base64 encrypted,
    need import binascii
    """

    def decrypt(self,
                crypted_datas,
                output_file=None):

        if os.path.exists(crypted_datas):
            f = open(crypted_datas, 'rb')
            self.crypted_datas = bytearray(base64.b64decode(f.read()))
            f.close()
        else:
            self.crypted_datas = bytearray(
                base64.b64decode(crypted_datas.encode("utf8")))

        self.decrypted_datas = bytearray(self.crypted_datas)
        j = 0
        for i in range(0, len(self.crypted_datas)):
            if j == len(self.key):
                j = 0
            self.decrypted_datas[i] = (
                self.crypted_datas[i] - self.key[j]) % 256
            j += 1

        self.crypted_datas = base64.b64encode(self.crypted_datas)

        if output_file != None:
            f = open(output_file, 'wb')
            f.write(self.decrypted_datas)
            f.close()

        return(self)

    """
    generate random binary key, update the key attribute

    Optional parameters:
    - size: size of the key, default 4096 bytes
    - output_file: file to write the keys
    """

    def genkey(self,
               size=4096,
               output_file=None):
        self.key_size = size
        self.key = bytearray(self.key_size)


        for i in range(0, self.key_size):
            self.key[i] = random.getrandbits(8)

        self.base64_key = base64.b64encode(self.key)

        if output_file is not None:
            if os.path.exists(output_file):
                raise zeus.exception.PrivateKeyOverwrite(output_file)
            f = open(output_file, 'wb')
            f.write(self.get_base64_key())
            f.close()

        return(self)

    def get_key(self):
        return (self.key)

    def get_base64_key(self):
        return (self.base64_key)

    def get_crypted_datas(self):
        return (self.crypted_datas)

    def get_decrypted_datas(self):
        return (self.decrypted_datas)

    def get_decrypted_datas_size(self):
        return (len(self.decrypted_datas))

    def get_key_size(self):
        return(self.key_size)

    def get_crypted_datas_base64(self):
        return (self.crypted_datas.decode("ascii"))

    def get_decrypted_datas_utf8(self):
        return (self.decrypted_datas.decode("utf8"))

    """
    print encrypted datas base64 coded
    """

    def __str__(self):
        if hasattr(self, 'crypted_datas'):
            return (self.get_crypted_datas_base64())
        else:
            return ("No crypted datas in buffer...")


class Vernam(Vigenere):
    """
    Vernam cipher inherit from Vigenere class

    Vigenere variant mathematically safe

    nead following prerequists:
    - oneshot key (one key for one message)
    - key length must be greater or equal than message length

    Security is dependant of key storage only
    """

    def __init__(self, key_file=None):
        if key_file is not None:
            super().__init__(key_file=key_file)
        else:
            super().__init__()

    def encrypt(self,
                decrypted_datas,
                output_file=None):
        super().load(decrypted_datas)
        super().genkey(size=self.get_decrypted_datas_size(), output_file=self.key_file)
        super().encrypt(decrypted_datas, output_file=output_file)


class Hash():
    """

    MD5 of file or buffer

    Parameters:
        - input_data: file path or buffer content

    Attributes:
        - digest: sha256 digest of datas provided

    """
    def __init__(self, input_data):

        sha = hash.sha256()

        if os.path.exists(input_data):
            BLOCKSIZE = 65536

            with open(input_data, 'rb') as fd:
                file_buffer = fd.read(BLOCKSIZE)
                while len(file_buffer) > 0:
                    sha.update(file_buffer)
                    file_buffer = fd.read(BLOCKSIZE)

        else:
            sha.update(input_data.encode("utf8"))

        self.digest = sha.hexdigest()

    def get_digest(self):
        return(self.digest)
