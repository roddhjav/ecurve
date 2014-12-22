""" ectools
 Some tools for elliptic curve
"""      

""" egcd
 Greatest common divisor
"""
def egcd(a, b):
   if a == 0:
      return (b, 0, 1)
   else:
      g, y, x = egcd(b % a, a)
   return (g, x - (b // a) * y, y)

""" modinv
 Modular inverse
"""
def modinv(a, m):
   g, x, y = egcd(a, m)
   if g != 1:
      raise Exception('modular inverse does not exist')
   else:
      return x % m

""" primes
 Takes a number as argument and returns the factorization of that number
 Example : 12 = [2^2,3]
"""
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
   
