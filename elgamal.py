import math
import random
from elliptic import *
from point import *

class Elgamal(object):
   """ ElGamal encryption
   - curve EllipticCurve
   - generator Point
   - privatekey int
   - publickey Point
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx,  self.curve.gy)
      
   def genkey(self):
      bits = int(math.log(self.curve.n, 2))
      self.privatekey = random.getrandbits(bits - 1)
      self.publickey = self.privatekey*self.generator   
   
      print("privatekey =", self.privatekey)
      print("publickey  =", self.publickey)
      
   def encryp(self, publickey, m):
      bits = int(math.log(self.curve.n, 2))
      k = random.getrandbits(bits - 1)
      """
      c1 = k*self.generator
      
      sharedsecret = k*publickey
      c2 = m*sharedsecret
      
      """
      c1 = (k*publickey).x + m
      c2 = k*self.generator
      
      return (c1, c2)
      
   def decryp(self, privatekey, c1, c2):
      return c1 - (privatekey*c2).x
