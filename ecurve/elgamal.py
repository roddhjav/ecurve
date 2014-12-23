import math
from Crypto.Random import random
from .elliptic import *
from .point import *

class Elgamal(object):
   """ ElGamal encryption
   - self.curve (EllipticCurve) The elliptic curve used
   - self.generator (Point) A generator of the curve
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)
   
   """ Generate elgamal keys
    - publickey (Point) the public key
    - privatekey (int) the private key
   """
   def keygen(self):
      bits = int(math.log(self.curve.n, 2))
      privatekey = random.getrandbits(bits - 1)
      publickey = privatekey*self.generator
      return (publickey, privatekey)
      
   """ Encrypt a message
    Input :
    - publickey (Point) the public key
    - m (int) message
    Output :
    - c1 (int)
    - c2 (Point)
   """
   def encrypt(self, publickey, m):
      bits = int(math.log(self.curve.n, 2))
      k = random.getrandbits(bits - 1)
      c1 = (k*publickey).x + int(m)
      c2 = k*self.generator
      return (c1, c2)
      
   """ Decrypt a message
    Input :
    - privatekey (int) the private key
    - c1 (int)
    - c2 (Point)
    output :
    - Message decrypted (int)
   """
   def decrypt(self, privatekey, c1, c2):
      return c1 - (privatekey*c2).x
      
