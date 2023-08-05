[![Build Status](https://travis-ci.com/acapitanelli/jewels.svg?branch=master)](https://travis-ci.com/acapitanelli/jewels)

## Jewels

A simple utility for encrypting/decrypting text files. It can be used for securely using applicative credentials.

Jewels provides:
- a Command Line tool for user-driven key generation and data encryption
- a Jewels Class for application-driven file decryption

Encryption is performed using AES256 in EAX Mode.

### Installation

> \> pip install jewels

### Usage

Generate a key file to safely store on server:

> \> jewels-cli keygen /etc/mykey

Encrypt a text file:

> \> jewels-cli encrypt plaintext [--dest dest-dir] /etc/mykey

Encrypt recursively all text files into a folder:

> \> jewels-cli encrypt -r src-dir [--dest dest-dir] /etc/mykey

Inside your code, access data from an encrypted file:

```
from jewels import Jewels

jewel = Jewels('/etc/mykey')

data = jewel.decrypt('filename')
```

