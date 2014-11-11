class EllipticCurve(object):

   # w256-009
   # y^2 = x^3 + a4 x + a6

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


   def testPoint(self, x, y):
      res1=(y*y)% self.p
      res2=(x*x*x + self.a4 * x + self.a6) % self.p
      return res1 == res2


   def __str__(self):
      return 'y^2 = x^3 + %sx + %s \np = %s\nn = %s' % (self.a4, self.a6, self.p, self.n)


   def __repr__(self):
      return str(self)


   def __eq__(self, other):
      return (self.p, self.n, self.a4, self.a6) == (other.p, other.n, other.a4, other.a6)
      


