import math
import random
from elliptic import *
from point import *

class DH(object):
   def __init__(self, curve):
      self.curve = curve
      self.a = random.getrandbits(246)
      print self.curve.n
      print self.a
      assert self.a < self.curve.n, "bla"
      

   #def keychange(self):

