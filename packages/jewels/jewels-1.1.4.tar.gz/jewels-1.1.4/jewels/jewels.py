#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from os import walk, path, listdir
import base64

class Jewels:

    NUM_BYTES = 32
    ALLOWED_FILES = ('.json', '.txt', '.yaml', '.yml')

    def __init__(self, keyfile):
        self.key = self.load_key(keyfile)


    def decrypt(self, encrypted_file):

        key = self.key

        with open(encrypted_file, 'r') as f:
            # 24 bytes instead of 16 for base64 padding
            nonce, tag, ciphertext = [ base64.standard_b64decode(f.read(el).encode('utf-8')) for el in (24, 24, -1) ]

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        return data.decode('utf-8')


    def encrypt(self, source_file, dest_file):

        key = self.key

        cipher = AES.new(key, AES.MODE_EAX)

        try:

            with open(source_file, 'r', encoding='utf-8') as f:
                byte_data = f.read().encode()

            ciphertext, tag = cipher.encrypt_and_digest(byte_data)

            with open(dest_file, 'w') as f:
                for el in (cipher.nonce, tag, ciphertext):
                    f.write(base64.standard_b64encode(el).decode('utf-8'))

        except Exception as err:
            print('Impossible to encrypt {0}: {1}'.format(source_file, str(err)))

        else:
            print('Encrypted "{0}".'.format(source_file))

        return


    def encrypt_all(self, src, dest_dir):

        for dirpath, _, files in walk(src, topdown=True, followlinks=False):

            for filename in files:

                source_file = path.join(dirpath, filename)

                if source_file.endswith(Jewels.ALLOWED_FILES):

                    dest_file = path.join(dest_dir, filename.split('.')[0])
                    self.encrypt(source_file, dest_file)

        return


    def load_key(self, keyfile):

        try:
            with open(keyfile, 'r', encoding='utf-8') as f:
                key = base64.standard_b64decode(f.read().encode('utf-8'))

        except Exception as err:
            print('Impossible to read key file: {0}'.format(str(err)))

        return key


    @staticmethod
    def generate_key(key_file):

        # generate key bytes
        key = get_random_bytes(Jewels.NUM_BYTES)

        # base64 encoding
        key = base64.standard_b64encode(key).decode('utf-8')

        try:
            with open(key_file, 'w') as f:
                f.write(key)
                print('Key saved in "{0}". Please put this file in a safe folder.'.format(key_file))

        except Exception as err:
            print('Impossible to save key file: {0}'.format(str(err)))

        return
