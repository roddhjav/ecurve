import math
import random
from elliptic import *
from point import *

# TODO : Add comment about var
class DH(object):
   def __init__(self, curve):
      self.curve = curve
      self.a = random.getrandbits(246) # See if it is a secure random
      assert self.a < self.curve.n, "Error"
      
      self.g = Point(self.curve, self.curve.gx,  self.curve.gy)
      self.ga = self.a*self.g
      
      print("a   =", self.a)
      print("g   =", self.g)
      print("g^a =", self.ga)
      
   def setkey(self, gb):
      self.gba = self.a*gb
