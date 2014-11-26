import math
import random
from elliptic import *
from point import *


# TODO : Add comment about var
class ECDSA(object):
   def __init__(self, curve):

   def gen_key_pair(self):
      #need n and G to generate the random key pair
      n = self.curve.n
      G = Point(self.curve.gx, self.curve.gy)
      N = int(math.log(n))
      
      d = random.getrandbits(N)
      
      while c > (n-2):
         d = random.getrandbits(N)
      
      d = d + 1
      Q = d*G
      
      #return d and Q
      return (d,Q)
      
   def load_key_pair(self):
      #Load pregenerated keys for later tests

   def sign(self):
      

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

6.Compute s= (k^1∗(e+d∗r)) mod n. If s= 0, return to Step 1

7. return (r, s)
"""
