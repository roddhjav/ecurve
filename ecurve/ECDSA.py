import math
import hashlib
from Crypto.Random import random
from .elliptic import EllipticCurve
from .point import Point
from .ectools import *

class ECDSA(object):
   """ ECDSA encryption
    - self.curve (EllipticCurve) The elliptic curve used
    - self.generator (Point) A generator of the curve
    - self.size (int) Elliptic curve size (256 => SHA256, 512 => SHA512)
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)
      size = len(bin(self.curve.n))
      if size >= 240 and size <= 270:
         self.size = 256
      elif size >= 500 and size <= 550:
         self.size = 512
      else:
         raise Exception('Elliptic curve size error')
         
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
      if self.size == 256:
         H = hashlib.sha256()
      else:
         H = hashlib.sha512()
      H.update(m)
      digest = H.hexdigest()
      return self._sign(privatekey, digest)
   
   """ Sign a message
    Input :
    - privatekey (int) the private key
    - digest, hexadecimal digest
    Output :
    - r (int)
    - s (int)
   """
   def _sign(self, privatekey, digest):
      r = 1
      s = 1
      bits = int(math.log(self.curve.n, 2)) - 1
      k = random.getrandbits(bits)
      R = k*self.generator
      
      r = R[0] % self.curve.n      
      while s == 0:
         while r == 0:
            R = k*self.generator
            r = R[0] % self.curve.n

      kinv = modinv(k, self.curve.n)
      
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
      if self.size == 256:
         H = hashlib.sha256()
      else:
         H = hashlib.sha512()
      H.update(m)
      digest = H.hexdigest()
      return self._verif(publickey, digest, r, s)
      
   """ Verify a signature
    Input :
    - publickey (Point) the public key
    - digest, hexadecimal digest
    - r (int)
    - s (int)
    Output :
    - True  : The signature has been verified
    - False : The signature has not been verified
   """
   def _verif(self, publickey, digest, r, s):
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
