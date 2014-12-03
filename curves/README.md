# Elliptic curves under Weierstrass form of prime order n over a finite prime field F_p

size(p) : about 256 bits
y^2 = x^3 + a4 x + a6
Number of points n: a prime number

a4 and a6 are built from two random numbers r4 and r6 by the two following equations:
```
a4 = hextodec(sha512.hex("dec(r14)"))  modulo p
a6 = hextodec(sha512.hex("dec(r16)"))  modulo p
```

We give also a generator (gx,gy) of the group of the elliptic curve
This generator is random and 
```
gx = hextodec(sha512.hex("dec(r)"))  modulo p
```

(we draw a random r, compute gx by the previous formula, test if z = x^3 + a4 x + a6
is a square, if yes, we compute gy, if no, we draw an another r)

source : http://galg.acrypta.com/
