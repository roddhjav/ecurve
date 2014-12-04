import math
from ectools import *

class Point(object):
   """ Point
    A Point is a point of an elliptic curve
    - curve (EllipticCurve) the curve containing this point
    - x (int) 
    - y (int)
    - z (boolean) Indicates if point is infinite 
   """
   def __init__(self, curve, x, y, z = False):
      self.curve = curve
      self.x = x
      self.y = y
      self.z = z

      if not curve.testPoint(x, y , z):
         raise Exception("The point %s is not on the given curve %s!" % (self, curve))

   """ __str__
    Return a string with the point paramaters
   """
   def __str__(self):
      return "(%r, %r)" % (self.x, self.y)
      
   """ isIdeal
    Test if the point is infinite
    Output :
    - True if the point is infinite (z == true)
    - False otherwise
   """
   def isIdeal(self):
      return self.z
      
   """ __repr__
    Return a string with the point paramaters
   """
   def __repr__(self):
      return str(self)

   """ __eq__
    Test if two Points are egal
    Input :
     - other (Point) The point to test
    Output :
     - True if the two points are the same,
     - False otherwise
   """
   def __eq__(self, other):
      return (self.curve, self.x, self.y) == (other.curve, other.x, other.y)
      
   """ __neg__
    Return the negation of the point
    Output :
    -self (Point) 
   """
   def __neg__(self):
      Xq= self.x
      Yq= (-self.y) % self.curve.p
      return Point(self.curve, Xq, Yq, False)
      
   """ __add__
    Add two Points
    Input :
    - Q (Point)
    Output :
     self + Q (Point)
   """   
   def __add__(self, Q):
      if self.curve != Q.curve:
         raise Exception("Can't add points on different curves!")
         
      if self.isIdeal():
         return Q
         
      if Q.isIdeal():
         return self
         
      if Q == -self:
         return Point(self.curve, 0, 1, True)
         
      Xp = self.x
      Yp = self.y
      Xq = Q.x
      Yq = Q.y

      # Careful here it is not a simple division,
      # but a modular inversion
      if Xp == Xq:
         l= ((3*Xp*Xp + self.curve.a4)*modinv(2*Yp, self.curve.p))
      else:
         l = (Yp - Yq)*modinv((Xp - Xq)%self.curve.p, self.curve.p)

      Xr= (l*l - Xp - Xq) % self.curve.p
      Yr= (l*Xp - Yp - l*Xr) % self.curve.p
   
      return Point(self.curve, Xr, Yr)
      
   """ __mul__
    Multiply a Point with an int
    Input :
    - n (int)
    Output :
    - Q (Point) Q = n*self
   """   
   def __mul__(self, n):
      if not isinstance(n, int) and not isinstance(n, long):
         raise Exception("Can't scale a point by something which isn't an int!")

      if n == 0:
         return Point(self.curve, 0, 1, True)

      if n == 1:
         return self
      
      Q = Point(self.curve, 0, 1, True)
      i = 1 << (int(math.log(n, 2)))
      while i > 0:
         Q = Q + Q
         if n & i == i:
            Q = Q + self
         i = i >> 1
      return Q
   
   """ order
    Compute the order of the curve
    Output :
    - m (int) order of the curve
   """ 
   def order(self):
      m = self.curve.n
      factors = primes(m)
      
      r = len(factors)/2
      for i in range(0,r):
         pi = factors[2*i]
         ei = factors[2*i + 1]
         m = m/(pi^ei)
         Q = m*P
         
         while not Q.isIdeal:
            Q = pi*Q
            m = m*pi
         
      return m

   """ __rmul__
    Multiply a Point with an int
    Input :
    - n (int)
    Output :
    - Q = n*self (Point)
   """   
   def __rmul__(self, n):
      return self * n

   """ __list__
    
   """
   def __list__(self):
      return [self.x, self.y]

   """ __ne__
    
   """      
   def __ne__(self, other):
      return not self == other

   """ __getitem__
    
   """
   def __getitem__(self, index):
      return [self.x, self.y][index]

