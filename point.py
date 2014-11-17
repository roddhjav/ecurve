def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class Point(object):
   def __init__(self, curve, x, y, z=False):
      self.curve = curve # the curve containing this point
      self.x = x
      self.y = y
      self.z = z

      if not curve.testPoint(x,y):
         raise Exception("The point %s is not on the given curve %s!" % (self, curve))


   def __str__(self):
      return "(%r, %r)" % (self.x, self.y)

   def isIdeal(self):
      return self.z

   def __repr__(self):
      return str(self)


   def __eq__(self, other):
      return (self.curve,self.x,self.y)==(other.curve,other.x,other.y)

   def __neg__(self):
      Xq=self.x
      #yq = -Yp -a1*xp -a3
      Yq= (-self.y) % self.curve.p
      return Point(self.curve,Xq,Yq, False)

   def __add__(self,Q):
      if self.curve != Q.curve:
         raise Exception("Can't add points on different curves!")
      Xp= self.x
      Yp= self.y
      Xq= Q.x
      Yq= Q.y
      print "fuck"
      if self.isIdeal():
         print "merde"
         return Q
      if Q.isIdeal():
         print "merde 2"
         return self
      if Q == -self:
         return Point(0,1,True)
      
      print ("Mais euh")
      # Careful here it is not a simple division
      # But a modular inversion
      if Xp == Xq:
         l= ((3*Xp*Xp+self.curve.a4)*modinv(2*Yp,self.curve.p))
      else:
         l = (Yp-Yq)*modinv(Xp-Xq,p)

      Xr= (l*l-Xp-Xq) % self.curve.p
      Yr= (l*Xp - Yp -l*Xr) % self.curve.p
   
      return Point(self.curve, Xr, Yr)

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

