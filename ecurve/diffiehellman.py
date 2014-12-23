import math
from Crypto.Random import random
from .elliptic import EllipticCurve
from .point import Point

class Diffiehellman(object):
   """ Diffie Hellman
    - self.curve (EllipticCurve) The elliptic curve used
    - self.generator (Point) A generator of the curve
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)

   """ secret
   Diffie Hellman's secret
    Output :
    - x (int) Random private DH secret
   """
   def secret(self):
      bits = int(math.log(self.curve.n, 2))
      return random.getrandbits(bits - 1)
      
   """ gx
    Compute g^x (ie : x*g in EC)
    Intput :
    - x (int)
    Output :
    - gx (Point) 
   """
   def gx(self, x):
      return x*self.generator
       
   """ sharedsecret
    Compute the DH shared secret
    Intput :
    - x (int)
    - gy (Point)
    Output :
    - gxy (Point) g^yx = (g^y)^x
   """
   def sharedsecret(self, x, gy):
      return x*gy
      
