import math
import random
from elliptic import *
from point import *

#Add exchange over network
#Check if random function is truly random
# TODO : Add comment about var
class DH(object):
   def __init__(self, curve):
      self.curve = curve
      
      bits = int(math.log(curve.n,2))

      self.a = random.getrandbits(bits-1) # See if it is a secure random
      
      assert self.a < self.curve.n, "Error"
      
      self.g = Point(self.curve, self.curve.gx,  self.curve.gy)
      self.ga = self.a*self.g
      
      print("a   =", self.a)
      print("g   =", self.g)
      print("g^a =", self.ga)
      
   def setkey(self, gb):
      self.gba = self.a*gb
