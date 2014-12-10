import math
import os
import hashlib
import base64
from elliptic import *
from point import *
from ECDSA import *
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random

#TODO : Make STS inherit DH
class STS(object):
   """ STS
    - self.curve (EllipticCurve) The elliptic curve used
    - self.generator (Point) A generator of the curve
   """
   def __init__(self, curve):
      self.curve = curve
      self.generator = Point(self.curve, self.curve.gx, self.curve.gy)
      
   """ keygen
    Private STS key generation
    Output :
    - x (int) Random private STS secret
   """
   def keygen(self):
      bits = int(math.log(self.curve.n, 2))
      
      return random.getrandbits(bits - 1)
      
   """ secret
    
    Intput :
    - x (int)
    Output :
    - gx (Point) 
   """
   def secret(self, x):
       return x*self.generator
       
   """ sharedsecret
    Compute the STS shared secret
    Intput :
    - ecdsa_privatekey (int) ECDSA private key 
    - x (int) STS secret
    - gy (Point)

    Output :
    - gxy (Point) g^yx = (g^y)^x
    (gy, CertB, Ek(Sb(gx, gy)))
   """      
   def sharedsecret(self, ecdsa_privatekey, x, gx, gy):
      K = x*gy
      
      # signed = ECDSA("gx,gy")
      m = str(gx.x) + str(gx.y) + str(gy.x) + str(gy.y)
      m = m.encode()
      ecdsa = ECDSA(self.curve)
      (r, s) = ecdsa.sign(ecdsa_privatekey, m)
      
      # AES(K.x, signed)
      signed = str(r) + "," + str(s)
      signed += ' ' * (16 - len(signed) % 16)
      
      # AES key. Must have 32 bits length for AES256 and 
      # 16 bits for AES128. For 256 bits EC, we need AES128.
      # TODO : Adapt AES length to the curve
      aes_key = bin(K.x)
      aes_key = hashlib.sha256(aes_key.encode()).digest()
      
      # AES encryption
      iv = Random.new().read(AES.block_size)
      cipher = AES.new(aes_key, AES.MODE_CBC, iv)
      encrypted = cipher.encrypt(signed)
      
      # Encoding
      encrypted = base64.b64encode(encrypted)
      iv = base64.b64encode(iv)
      print("(r,s)  : " + str(r) + "," + str(s))
      print("Ek(Sb) : " + str(encrypted))
      print("iv     : " + str(iv))
      print("key    : " + str(base64.b64encode(aes_key)))

      return (K, encrypted, iv)

   def verifysecret(self, ecdsa_publickey, x, gx, gy, encrypted, iv):
      K = x*gy
      aes_key = bin(K.x)
      aes_key = hashlib.sha256(aes_key.encode()).digest()
      
      iv = base64.b64decode(iv)
      encrypted = base64.b64decode(encrypted)
      
      cipher = AES.new(aes_key, AES.MODE_CBC, iv)
      signed = cipher.decrypt(encrypted)

      (r, s) = signed.decode().split(',')
      print("Sb     : " + str(signed))
      print("(r,s)  : " + str(r) + "," + str(s))
            
      m = str(gx.x) + str(gx.y) + str(gy.x) + str(gy.y)
      m = m.encode()
      ecdsa = ECDSA(self.curve)
      print(ecdsa_publickey)
      print(ecdsa_publickey.curve)
      print(self.curve)
      return ecdsa.verif(ecdsa_publickey, m, r, s)
      
