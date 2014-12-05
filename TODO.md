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
    - http://stackoverflow.com/questions/16334433/python-read-binary-file-into-buffer-as-integer-then-slice
    - http://www.java2s.com/Tutorial/Python/0240__File/Readbytesintoabuffer.htm
* Read and write the file like binary file and not like text file
* Use os.urandom(n) instead of random.getrandombits(n) because the second is not suitable for cryptographic purposes
* Enable the user to choose security level (see below)

    | Level | Sym | Asym  | EC  | Hash |
    |:-----:|:---:|:-----:|:---:|:----:|
    | 5     | 96  | 1776  | 192 | 192  |
    | 6     | 112 | 2432  | 224 | 224  |
    | 7     | 128 | 3248  | 256 | 256  |
    | 8     | 256 | 15424 | 512 | 512  |
   
* In The README.md add comment about security purpose (security level and curves origin)