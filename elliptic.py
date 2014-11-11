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
      


class Point(object):
   def __init__(self, curve, x, y):
      self.curve = curve # the curve containing this point
      self.x = x
      self.y = y

      if not curve.testPoint(x,y):
         raise Exception("The point %s is not on the given curve %s!" % (self, curve))


   def __str__(self):
      return "(%r, %r)" % (self.x, self.y)


   def __repr__(self):
      return str(self)


   def __eq__(self, other):
      return (self.curve,self.x,self.y)==(other.curve,other.x,other.y)

   def __neg__(self):
      Xq=self.x
      #yq = xp -a1*xp -a3
      Yq=self.x +self.y % self.curve.p
      return Point(self.curve,Xq,Yq)

   def add_distinct_points(self, Q):
      if self.curve != Q.curve:
         raise Exception("Can't add points on different curves!")
      if isinstance(Q, Ideal):
         return self
      
      Xp, Yp, Xq, Yq = self.x, self.y, Q.x, Q.y

      X =Xp+Xq
      l = (Yp+Yq/X)% self.curve.p

      Xr = (l*l +l + X) % self.curve.p
      Yr = ((l+1)*Xr + l*Xp + Yp) % self.curve.p
      return Point(self.curve, Xr, Yr)

   def double(self):
      Xp = self.x
      Yp = self.y

      l = (Xp + Yp/Xp) % self.curve.p
      Xr = (l*l+l) % self.curve.p
      Yr = (Xp*Xp + l*Xr + Xr) % self.curve.p
      print "compute 2P\n"
      return Point(self.curve,Xr,Yr)

   def __add__(self,Q):

      if self == Q:
         return self.double()
      else:
         return self.add_distinct_points(Q)

   def __mul__(self, n):
      if not isinstance(n, int):
         raise Exception("Can't scale a point by something which isn't an int!")

      if n < 0:
         return -self * -n

      if n == 0:
         return Ideal(self.curve)

      Q = self
      R = self if n & 1 == 1 else Ideal(self.curve)

      i = 2
      while i <= n:
         Q += Q
         if n & i == i:
             R += Q
         i = i << 1
      return R


   def __rmul__(self, n):
      return self * n

   def __list__(self):
      return [self.x, self.y]

   def __eq__(self, other):
      return self.x==other.x and self.y == other.y

      return self.x, self.y == other.x, other.y

   def __ne__(self, other):
      return not self == other

   def __getitem__(self, index):
      return [self.x, self.y][index]


class Ideal(Point):
   def __init__(self, curve):
      self.curve = curve

   def __neg__(self):
      return self

   def __str__(self):
      return "Ideal"

   def __add__(self, Q):
      if self.curve != Q.curve:
         raise Exception("Can't add points on different curves!")
      return Q

   def __mul__(self, n):
      if not isinstance(n, int):
         raise Exception("Can't scale a point by something which isn't an int!")
      else:
         return self

   def __eq__(self, other):
      return type(other) is Ideal

