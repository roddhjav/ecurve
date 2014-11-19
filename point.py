import math

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

#takes a number as argument and returns the factorization of that number
#for example 12 = [2^2,3]
def primes(n):
   primfac = []
   multiple = False
   d = 2
   while d*d <=n:
      dpow = 0
      while(n%d) == 0:
         dpow = dpow + 1
         multiple = True
         n /= d
      
      if multiple:
         primfac.append(d)
         primfac.append(dpow)
         multiple=False
      d +=1
   
   if n>1:
      primfac.append(n)
      primfac.append(1)
   
   return primfac

class Point(object):
   def __init__(self, curve, x, y, z=False):
      self.curve = curve # the curve containing this point
      self.x = x
      self.y = y
      #Boolean
      #Indicates if point is infinite
      self.z = z

      if not curve.testPoint(x,y,z):
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
      if self.isIdeal():
         return Q
      if Q.isIdeal():
         return self
      if Q == -self:
         return Point(self.curve,0,1,True)
      
      # Careful here it is not a simple division
      # But a modular inversion
      if Xp == Xq:
         l= ((3*Xp*Xp+self.curve.a4)*modinv(2*Yp,self.curve.p))
      else:
         l = (Yp-Yq)*modinv((Xp-Xq)%self.curve.p,self.curve.p)

      Xr= (l*l-Xp-Xq) % self.curve.p
      Yr= (l*Xp - Yp -l*Xr) % self.curve.p
   
      return Point(self.curve, Xr, Yr)

   def __mul__(self, n):
      if not isinstance(n, int):
         raise Exception("Can't scale a point by something which isn't an int!")

      if n == 0:
         return Point(self.curve,0,1,True)

      if n == 1:
         return self
      
      Q = Point(self.curve,0,1,True)
      i = 1 << (int(math.log(n,2)))
      while i > 0:
         Q = Q + Q
         if n & i == i:
            Q = Q + self
         i = i >> 1
      return Q

   def order(self):
      
      m = self.curve.n
      factors = primes(m)
      
      r = len(factors)/2
      
      for i in range(0,r):
         pi = factors[2*i]
         ei = factors[2*i+1]
         m = m/(pi^ei)
         Q = m*P
         
         while not Q.isIdeal:
            Q = pi*Q
            m = m*pi
         
      return m

   def __rmul__(self, n):
      return self * n

   def __list__(self):
      return [self.x, self.y]

   def __eq__(self, other):
      return self.x == other.x and self.y == other.y

   def __ne__(self, other):
      return not self == other

   def __getitem__(self, index):
      return [self.x, self.y][index]

