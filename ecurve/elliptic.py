class EllipticCurve(object):
   """ Elliptic curve
    Elliptic curves in short Weierstrass form :
      y^2 = x^3 + a4 x + a6
      
    - self.p (int) Finite prime field Fp. Moreover : p = 3 mod 4 
    - self.n (int) Order of the curve. n is prime
    - self.a4 (int) a4 = Hash(r4)
    - self.a6 (int) a6 = Hash(r6)
    - self.r4 (int) (random) 
    - self.r6 (int) (random)
    - self.gx (int) gx = Hash(r) such that x^3+a*x+b is a square.
    - self.gy (int)
    - self.r (int) (random)
   
    g = (gx, gy) is a point of the curve
    r4, r6 and r assure the curve is not particular
    For more information see : http://galg.acrypta.com/index.php/download
   """
   def __init__(self, p, n, a4, a6, r4, r6, gx, gy, r):
      self.p = p
      self.n = n
      self.a4 = a4
      self.a6 = a6
      self.r4 = r4
      self.r6 = r6
      self.gx = gx
      self.gy = gy
      self.r = r

   """ testPoint
    Test if a Point (x, y, z) is a point of the curve
    Input :
    - (x, y, z) (int) member of the point
    Output :
    - True is (x, y, z) is a point of the curve
    - False is (x, y, z) is not point of the curve and not a ideal
   """
   def testPoint(self, x, y, z):
      res1 = (y*y) % self.p
      res2 = (x*x*x + self.a4 * x + self.a6) % self.p
      return (res1 == res2) or z

   """ __str__
    Return a string with the curve paramaters
   """
   def __str__(self):
      return ' y^2 = x^3 + a4x + a6\n a4 = %s\n a6 = %s\n p = %s\n n = %s' % (self.a4, self.a6, self.p, self.n)

   """ __repr__
    Return a string with the curve paramaters
   """
   def __repr__(self):
      return str(self)

   """ __eq__
    Test if two curve are egal
    Input :
     - other (EllipticCurve) The curve to test
    Output :
     - True if the two curve are the same,
     - False otherwise
   """
   def __eq__(self, other):
      return (self.p, self.n, self.a4, self.a6) == (other.p, other.n, other.a4, other.a6)
   
   """ __ne__
    Test if two curve are not egal
    Input :
     - other (EllipticCurve) The curve to test
    Output :
     - True if the two curve are not the same,
     - False otherwise
   """
   def __ne__(self, other):
      return not (self == other)
      
