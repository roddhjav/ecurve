# Elliptic Curves in python

## Usage
The program provide 4 softwares with similar command line usage

### Diffie Hellman


Get the help
```
dh -h
```

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
Option like keygen, crypt and decrypt are mandatory. The other option are not mandatory, the default path are : 
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
Option like keygen, sign and verif are mandatory. The other option are not mandatory, the default path are : 
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
