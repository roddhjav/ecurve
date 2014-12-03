import math
import random
from elliptic import *
from point import *

class Elgamal(object):
   """ ElGamal encryption
   - curve EllipticCurve
   - generator Point
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)
      
   def keygen(self):
      bits = int(math.log(self.curve.n, 2))
      privatekey = random.getrandbits(bits - 1)
      publickey = privatekey*self.generator
      return (publickey, privatekey)
      
   def crypt(self, publickey, m):
      bits = int(math.log(self.curve.n, 2))
      k = random.getrandbits(bits - 1)
      c1 = (k*publickey).x + int(m)
      c2 = k*self.generator
      return (c1, c2)
      
   def decrypt(self, privatekey, c1, c2):
      return c1 - (privatekey*c2).x
