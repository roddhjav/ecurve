import math
import random
import hashlib
from elliptic import *
from point import *
from ectools import *

class ECDSA(object):
   """ ECDSA encryption
   - self.curve (EllipticCurve) The elliptic curve used
   - self.generator (Point) A generator of the curve
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)

   """ Generate ecdsa keys
    - publickey (Point) the public key
    - privatekey (int) the private key
   """
   def keygen(self):
      N = int(math.log(self.curve.n, 2)) - 1
      c = random.getrandbits(N)
      
      while c > (self.curve.n - 2):
         c = random.getrandbits(N)
      
      privatekey = c + 1
      publickey = privatekey*self.generator
      
      return (publickey, privatekey)
   
   """ Sign a message
    Input :
    - privatekey (int) the private key
    - m (bytes) message encoded in utf8
    Output :
    - r (int)
    - s (int)
   """
   def sign(self, privatekey, m):
      r = 1
      s = 1
      k = random.getrandbits(50)
      R = k*self.generator
      
      r = R[0] % self.curve.n      
      while s == 0:
         while r == 0:
            R = k*self.generator
            r = R[0] % self.curve.n

      kinv = modinv(k, self.curve.n)
      
      H = hashlib.sha256()
      H.update(m)
      digest = H.hexdigest()
      e = int(digest, 16)
      s = (kinv*(e + privatekey*r)) % self.curve.n
      return (r, s)
   
   """ Verify a signature
    Input :
    - publickey (Point) the public key
    - m (bytes) message encoded in utf8
    - r (int)
    - s (int)
    Output :
    - True  : The signature has been verified
    - False : The signature has not been verified
   """
   def verif(self, publickey, m, r, s):
      H = hashlib.sha256()
      H.update(m)
      
      digest = H.hexdigest()
      e = int(digest, 16)
      
      w = modinv(s, self.curve.n)
      u1 = (e*w) % self.curve.n
      u2 = (r*w) % self.curve.n
      
      R = u1*self.generator + u2*publickey
      if R.isIdeal():
         return False

      if R[0] == r:
         return True
      else:
         return False
"""
1. Use one of the routines in Appendix A.2 to generate (k, k^1),
a per-message secret number and its inverse modulo n.
Since n is prime, the output will be invalid only if there is a failure in the R

2.Compute the elliptic curve point R=kG= (xR, yR) using EC scalar
multiplication (see [Routines]), where G is the base point included in
the set of domain parameters.

3.Compute r=xR mod n.Ifr= 0, then return to Step 1.

4.Use the selected hash function to compute H=Hash(M)

5.Convert the bit string H to an integer e as described in Appendix

6.Compute s=(k^1*(e+d*r)) mod n. if s=0, return to step 1
7. return (r, s)
"""
