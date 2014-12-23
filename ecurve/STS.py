import math
import hashlib
import base64
from .diffiehellman import Diffiehellman
from .elliptic import EllipticCurve
from .point import Point
from .ECDSA import ECDSA
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random

class STS(Diffiehellman):
       
   """ sharedsecret
    Compute the STS shared secret, sign it and encrypt the signed
    
    Intput :
    - ecdsa_privatekey (int) ECDSA private key 
    - x (int) STS secret
    - (gx, gy) (Point, Point)

    Output :
    - gxy (Point) g^yx = (g^y)^x
    - encrypted (bytes) Signed encryped
                        such as : encrypted =  AESk(ECDSAp("gx,gy"))
    - iv (bytes) Initialisation vector for AES
   """      
   def sharedsecret(self, ecdsa_privatekey, x, gx, gy):
      gxy = x*gy
      
      # signed = ECDSA("gx,gy")
      m = str(gx.x) + str(gx.y) + str(gy.x) + str(gy.y)
      m = m.encode()
      ecdsa = ECDSA(self.curve)
      (r, s) = ecdsa.sign(ecdsa_privatekey, m)
      
      # AES(gxy.x, signed)
      signed = str(r) + "," + str(s)
      signed += ' ' * (16 - len(signed) % 16)
      
      # AES key. Must have 32 bytes length for AES256 and 
      # 16 bytes for AES128. For 256 bits EC, we need AES128.
      aes_key = bin(gxy.x)
      aes_key = hashlib.sha256(aes_key.encode()).digest()
      
      # AES encryption
      iv = Random.new().read(AES.block_size)
      cipher = AES.new(aes_key, AES.MODE_CBC, iv)
      encrypted = cipher.encrypt(signed)
      
      # Encoding
      encrypted = base64.b64encode(encrypted)
      iv = base64.b64encode(iv)
      #print("(r,s)  : " + str(r) + "," + str(s))
      #print("Ek(Sb) : " + str(encrypted))
      #print("iv     : " + str(iv))
      #print("key    : " + str(base64.b64encode(aes_key)))

      return (gxy, encrypted, iv)
      
   """ verifysecret
    Verify the STS shared secret origin
    
    Intput :
    - ecdsa_publickey (int) ECDSA public key (certificat)
    - x (int) STS secret
    - (gx, gy) (Point, Point)
    - encrypted (bytes) Signed encryped
    - iv (bytes) Initialisation vector for AES

    Output :
    - True if the STS shared secret is from the good user
    - False otherwise
   """   
   def verifysecret(self, ecdsa_publickey, x, gx, gy, encrypted, iv):
      K = x*gy
      aes_key = bin(K.x)
      aes_key = hashlib.sha256(aes_key.encode()).digest()
      
      iv = base64.b64decode(iv)
      encrypted = base64.b64decode(encrypted)
      
      cipher = AES.new(aes_key, AES.MODE_CBC, iv)
      signed = cipher.decrypt(encrypted)

      (r, s) = signed.decode().split(',')
      s = int(s)
      r = int(r)
      #print("Sb     : " + str(signed))
      #print("(r,s)  : " + str(r) + "," + str(s))
      
      m = str(gy.x) + str(gy.y) + str(gx.x) + str(gx.y)
      m = m.encode()
      ecdsa = ECDSA(self.curve)
      
      return ecdsa.verif(ecdsa_publickey, m, r, s)
      
