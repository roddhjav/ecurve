# TODO

## Elliptic curve componant

* Diffie - Hellman
* ElGamal
* ECDSA
   - Add File signature
   - https://www.nsa.gov/ia/_files/ecdsa.pdf
* STS 
   - https://notendur.hi.is/pgg/Handbook%20of%20Applied%20Cryptography.pdf pages 519 to 520
   - http://en.wikipedia.org/wiki/Station-to-Station_protocol
   - Create our own certification authority
* We should maybe switch from using variables directly to using getters instead of self.curve.n use self.curve.getOrder()

## Global feature

* Create buffer to read, write and encode the data
* Read and write the file like binary file and not like text file
* Use os.urandom(n) instead of random.getrandombits(n) because the second is not suitable for cryptographic purposes
* Enable the user to choose security level (see below)

| level  |sym  |asym   |ec  |hash  |
|:-----: |:---:|:----: |:--:|:----:|
|5       |96   | 1776  |192 |192   |
|6       |112  | 2432  |224 |224   |
|7       |128  | 3248  |256 |256   |
|8       |256  | 15424 |512 |512   |
