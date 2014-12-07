# Elliptic Curves in python

## Description

That software provide four security primitives class ;
* Diffie Hellman : `diffiehellman.py`
* ElGamal : `elgamal.py`
* ECDSA : `ECDSA.py`
* STS : `STS.py`

In more there is 4 front-end for an immediate usage :
* Diffie Hellman : `dh`
* ElGamal : `elgamal`
* ECDSA : `ecdsa`
* STS : `sts`

## Usages

### Diffie Hellman


Generate Diffie Hellman key
```
dh --keygen -c <elliptic_curve> -o <key_path>
```

Create connection with a computer and share DH's secret.

```
dh --share --key <key_path> --output <dh_shared_secret_path> --port <port> --host <hostname>
```
**WARNING** The first computer connected must create the server with `--server`
```
dh --share --key <key_path> --output <dh_shared_secret_path> --port <port> --host <hostname> --server
```

Get the help :
```
dh -h
```

**WARNING** 
Options like `--keygen` and `--share` are mandatory. The other option are not mandatory, the default path are : 
* Curve : `curves/w256-001.gp`
* Private secret : `keys/dh`
* Shared secret : `keys/dh.shared`
* Hostname : `localhost`
* Port : `12800`

### Elgamal

Generate an elgamal key pair
```
elgamal --keygen -c <elliptic_curve> -o <keys_path>
```

Crypt a file
```
elgamal --crypt -k <public_key> -i <file> -o <file_encrypted>
```

Decrypt a file
```
elgamal --decrypt -k <private_key> -i <file_encrypted> -o <file>
```

Get the help
```
elgamal -h
```

**WARNING** 
Options like `--keygen`, `--crypt` and `--decrypt` are mandatory. The other option are not mandatory, the default path are : 
* Curve : `curves/w256-001.gp`
* Public key : `keys/elgamal.pub`
* Private key : `keys/elgamal`
* File : `sample/text`
* File encrypted : `sample/text.elgamal`
* Decrypted file : `sample/text.decoded`

### ECDSA

Generate an elgamal key pair
```
ecdsa --keygen -c <elliptic_curve> -o <keys_path>
```

Sign a file
```
ecdsa --sign -k <private_key> -i <file> -o <file_signed>
```

Verify the signature
```
ecdsa --verif -k <public_key> -i <file_signed>
```

Get the help
```
ecdsa -h
```

**WARNING** 
Options like `--keygen`, `--sign` and `--verif` are mandatory. The other option are not mandatory, the default path are : 
* Curve : `curves/w256-001.gp`
* Public key : `keys/ecdsa.pub`
* Private key : `keys/ecdsa`
* File : `sample/text`
* File encrypted : `sample/text.ecdsa`

### STS


Get the help
```
sts -h
```

## Authors
* Alexandre PUJOL <alexandre.pujol.1@etu.univ-amu.fr>
* Maxime CHEMIN <maxime.chemin@etu.univ-amu.fr>
