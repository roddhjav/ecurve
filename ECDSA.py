import math
import random
import hashlib
from elliptic import *
from point import *
from ec_utils import *


# TODO : Add comment about var
class ECDSA(object):
   def __init__(self, curve,d=None,Q=None):
      self.d = d
      self.Q = Q
      self.curve = curve

   def gen_key_pair(self):
      #need n and G to generate the random key pair
      n = self.curve.n
      G = Point(self.curve,self.curve.gx, self.curve.gy)
      N = int(math.log(n))
      
      c = random.getrandbits(N)
      
      while c > (n-2):
         c = random.getrandbits(N)
      
      d = c + 1
      Q = d*G
      
      #return d and Q
      return (d,Q)
      
   def load_key_pair(self,path):
      #Load pregenerated keys for later tests
      data = {}
      
      f = open(path,"r")
      
      lines = f.readlines()
      
      for line in lines:
         (var,val) = line.split('=')
         data[var]=int(val) 
      
      self.curve = EllipticCurve(data["p"],
                                 data["n"], 
                                 data["a4"],
                                 data["a6"],
                                 data["r4"],
                                 data["r6"],
                                 data["gx"],
                                 data["gy"],
                                 data["r"])
      self.d = data["d"]
      self.Q = Point(self.curve,int(data["Qx"]),int(data["Qy"]))
      
      f.close()

#Idea use function in Ellipticcurve to get necessary arguments in the right format
   def save_key_pair(self,path):
      f = open(path,"w")
      
      f.write("n="+str(self.curve.n)+"\n")
      f.write("p="+str(self.curve.p)+"\n")
      f.write("a4="+str(self.curve.a4)+"\n")
      f.write("a6="+str(self.curve.a6)+"\n")
      f.write("r4="+str(self.curve.r4)+"\n")
      f.write("r6="+str(self.curve.r6)+"\n")
      f.write("a4="+str(self.curve.a4)+"\n")
      f.write("r="+str(self.curve.r)+"\n")
      f.write("gx="+str(self.curve.gx)+"\n")
      f.write("gy="+str(self.curve.gy)+"\n")
      f.write("d="+str(self.d)+"\n")
      f.write("Qx="+str(self.Q[0])+"\n")
      f.write("Qy="+str(self.Q[1])+"\n")
      
      f.close()

   def set_key(self,d,Q):
      self.d = d
      self.Q = Q

   def sign(self, m):
      
      r=1
      s=1 
      Q = self.Q
      n = self.curve.n
      d = self.d
      k = random.getrandbits(50)
      G = Point(self.curve.gx,self.curve.gy)
      
      R =  k*G
      
      r = R[0] % n
      
      while s == 0:
         while r == 0:
            G = Point(self.curve.gx,self.curve.gy)
            R =  k*G
            r = R[0] % n

         kinv = modinv(k,n)
      
         H = hashlib.sha256()
         H.update(m)
      
         digest = H.hexdigest()
         e = int(digest,16)
      
         s = (kinv*(e+d*r)) % n
      
      return (r,s)
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
