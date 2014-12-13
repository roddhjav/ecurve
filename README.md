# Elliptic Curves in python

DiffieHellman, Elfgamal, ECDSA & STS with elliptic curve in python

## Description

**That software provide four security primitives class ;**
* Diffie Hellman : `diffiehellman.py`
* ElGamal : `elgamal.py`
* ECDSA : `ECDSA.py`
* STS : `STS.py`

**In more there is four front-end for an immediate usage :**
* Diffie Hellman : `dh`
* ElGamal : `elgamal`
* ECDSA : `ecdsa`
* STS : `sts`

**Tools used by primitives Class and front-end :**
* `EllipticCurve` : The elliptic curve class
* `Point` ; The point class
* `ectools.py` : Mathematic function for elliptic curve
* `tools.py` : 
  - `tools` : Read curve, I/O files
  - `key` : I/O functions for the keys
  - `message` Easy to use socket functions
* `stools` : STS and DH tools for secret exchange using socket

**File system :**
* `curves/` : 
  - There is 17 256bits curves and 18 512bits curves. All front-end and class manage the two sizes of curve
  - The curve from http://galg.acrypta.com/. Therefore there are not classic curve recommend by the NIST
  - Elliptic curves under Weierstrass form
  - See `curves/README.md` for more information
* `keys/`
  - As the curve are not the classic NSA's curve. The key format containt the curve itself.
  - See `keys/README.md` for more information about keys format
* `sample/`
  - Default directory for plain text, signed and encrypted files
  - See `sample/README.md` for more information

## Requirements :

That software run with Python 3.4.2. It hasn't been tested with Python 2.7.

For AES function and the secure random generator you need the python library Crypto avaible [here](https://pypi.python.org/pypi/pycrypto)

## Usages
All the following command are showed with they full command. But some command are not mandatory as described 

### Diffie Hellman : `dh`

**Create connection with a computer and start DH protocol :**
```
dh --curve <curve.gp> --output <sharedsecret> --port <port> --host <hostname>
```
**The first computer connected have to create the server with `--server`**
```
dh --curve <curve.gp> --output <sharedsecret> --port <port> --server
```

**Get the help :**
```
dh --help
```

**Default options :**
* `<curve.gp>` : `curves/w256-001.gp`
* `<sharedsecret>` : `keys/dh.shared`
* `<port>` : `12800`
* `<localhost>` : `12800`

### Elgamal : `elgamal`

**Generate an elgamal key pair : `<key>` as private and `<key.pub>` as public key**
```
elgamal --keygen --curve <curves.gp> --output <key>
```

**Encrypt a file :**
```
elgamal --crypt --key <key.pub> --input <file> --output <file.elgamal>
```

**Decrypt a file :**
```
elgamal --decrypt -key <key> --input <file.elgamal> --output <file.decoded>
```

**Get the help :**
```
elgamal --help
```

**Default options :**
* `<curve.gp>` : `curves/w256-001.gp`
* `<key.pub>` : `keys/elgamal.pub` Public key
* `<key>` : `keys/elgamal` Private key
* `<file>` : `sample/text` Plain text file
* `<file.elgamal>` : `sample/text.elgamal` Encrypted file
* `<file.decoded>` : `sample/text.decoded` File decrypted

### ECDSA : `ecdsa`

**Generate an ECDSA key pair : `<key>` as private and `<key.pub>` as public key**
```
ecdsa --keygen --curve <curves.gp> --output <key>
```

**Sign a file :**
```
ecdsa --sign --key <key> --input <file> --output <file.signed>
```

**Verify the signature : the signed have to be named `<file.signed>`**
```
ecdsa --verif --key <key.pub> --input <file> 
```

**Get the help :**
```
ecdsa --help
```

**Default options :**
* `<curve.gp>` : `curves/w256-001.gp`
* `<key.pub>` : `keys/ecdsa.pub` Public key
* `<key>` : `keys/ecdsa` Private key
* `<file>` : `sample/text` Plain text file
* `<file.signed>` : `sample/text.signed` The signed of the file (You still need the file itsel)

### STS : `sts`

**Requirements**
* You need to generate first an ECDSA key pair with the same curve you will use for STS
* <key> is your ECDSA private key
* <key.pub> is your ECDSA public key 

**Create connection with a computer and start STS protocol :**
```
sts --curve <curve.gp> --key <key> --output <sharedsecret> --port <port> --host <hostname>
```
**The first computer connected have to create the server with `--server`**
```
sts --curve <curve.gp> --key <key> --output <sharedsecret> --port <port> --server
```

**Get the help :**
```
sts --help
```

**Default options :**
* `<curve.gp>` : `curves/w256-001.gp`
* `<key>` : `keys/ecdsa` and `keys/ecdsa.pub` We need the both private and public key
* `<sharedsecret>` : `keys/sts.shared`
* `<port>` : `12800`
* `<localhost>` : `12800`


## Security purpose

| Level | Protection                                                        | Sym | Asym  | EC  | Hash |
|:-----:|:-----------------------------------------------------------------:|:---:|:-----:|:---:|:----:|
| 1     | Attacks in ”real-time” by individuals                             | 32  |       |     |      |
| 2     | Very short-term protection                                        | 64  | 816   | 128 | 128  |
| 3     | Short-term protection against medium organizations                | 72  | 1008  | 144 | 144  |
| 4     |                                                                   | 80  | 1248  | 160 | 160  | 
| 5     | Legacy standard level                                             | 96  | 1776  | 192 | 192  |
| 6     | Medium-term protection                                            | 112 | 2432  | 224 | 224  |
| 7     | Long-term protection (minimum level recommended)                  | 128 | 3248  | 256 | 256  |
| 8     | ”Foreseeable future”, Good protection against government agencies | 256 | 15424 | 512 | 512  |


## Authors
* Alexandre PUJOL <alexandre.pujol.1@etu.univ-amu.fr>
* Maxime CHEMIN <maxime.chemin@etu.univ-amu.fr>
