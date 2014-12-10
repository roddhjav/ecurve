#
# Elliptic Curves in python
# Version 1.0
# Year 2014
# Author Alexandre PUJOL <alexandre.pujol.1@etu.univ-amu.fr>
# Author Maxime CHEMIN <maxime.chemin@etu.univ-amu.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License.
#

import base64
from elliptic import *
from point import *

# TODO : Add exception error during read & write
# TODO : Add buffer when reading and writing a file

""" tools
 Some tools
"""
class tools(object):

   """ loadCurve
   
   """
   @staticmethod
   def loadCurve(path):
      data = {}
      f = open(path, "r")
      lines = f.readlines()
      
      for line in lines:
         (var, val) = line.split('=')
         data[var] = int(val)
      
      curve = EllipticCurve(  data["p"],
                              data["n"],
                              data["a4"],
                              data["a6"],
                              data["r4"],
                              data["r6"],
                              data["gx"],
                              data["gy"],
                              data["r"])
      f.close()
      return curve
      
   """ readFile
   
   """
   @staticmethod
   def readFile(path):
      f = open(path, "r", encoding='utf-8')
      filecontent = f.read()
      f.close()
      return filecontent

   """ writeFile
   
   """ 
   @staticmethod
   def writeFile(path, content):
      f = open(path, "w")
      f.write(content)
      f.close()


""" Key

"""      
class key(object):

   """ writeKey
    Write ELGAMAL, ECDSA or DIFFIEHELLMAN public and private key in a file
    Input :
     - path (string) key path (a public key will have .pub)
     - algo (string) algo type : ELGAMAL or ECDSA or DiffieHellman
     - curve (EllipticCurve) The elliptic curve used
     - key (int or Point) The key
   """
   @staticmethod
   def writeKey(path, algo, curve, key):
      f = open(path, "w")
      
      if algo is not 'ELGAMAL' and algo is not 'ECDSA' and algo is not 'DIFFIEHELLMAN':
         raise Exception('Writing key : Unrecognized algorithm')
      
      if isinstance(key, Point):
         if algo is 'DIFFIEHELLMAN':
            keytype = 'SHAREDSECRET'
         else:
            keytype= 'PUBLIC'
      elif isinstance(key, int) or isinstance(key, long):
         keytype= 'PRIVATE'
      else:
         raise Exception('Writing key : Key type error')
      
      #f.write( str(base64.b64encode( str(curve.p).encode('ascii'))) )
      
      f.write("-----BEGIN " + algo + " " + keytype + " KEY-----\n")
      f.write("p=" + str(curve.p) + "\n")
      f.write("n=" + str(curve.n) + "\n")
      f.write("a4=" + str(curve.a4) + "\n")
      f.write("a6=" + str(curve.a6) + "\n")
      f.write("r4=" + str(curve.r4) + "\n")
      f.write("r6=" + str(curve.r6) + "\n")
      f.write("gx=" + str(curve.gx) + "\n")
      f.write("gy=" + str(curve.gy) + "\n")
      f.write("r=" + str(curve.r) + "\n")
      
      if isinstance(key, Point):
         f.write("Kx="+str(key.x)+"\n")
         f.write("Ky="+str(key.y)+"\n")
      elif isinstance(key, int) or isinstance(key, long):
         f.write("K="+str(key)+"\n")
      
      f.write("-----END " + algo + " " + keytype + " KEY-----\n")
      f.close()


   """ readKey
    Read ELGAMAL, ECDSA or DIFFIEHELLMAN public and private key from a file
    Input :
     - path (string) key path
    Output :
     - curve (EllipticCurve) The elliptic curve used
     - key (int or Point) The key
   """
   @staticmethod
   def readKey(path):
      data = {}
      f = open(path, "r")
      lines = f.readlines()
      algo = lines[0].split(' ')[1]    # algo = ELGAMAL or ECDSA or DH
      keytype = lines[0].split(' ')[2] # keytype = PUBLIC or PRIVATE
      lines = lines[1:len(lines)-1]
      
      for line in lines:
            (var, val) = line.split('=')
            data[var] = int(val) 
      
      curve = EllipticCurve(  data["p"],
                              data["n"],
                              data["a4"],
                              data["a6"],
                              data["r4"],
                              data["r6"],
                              data["gx"],
                              data["gy"],
                              data["r"])
      
      if algo != 'ELGAMAL' and algo != 'ECDSA' and algo != 'DIFFIEHELLMAN':
         raise Exception('Reading key : Unrecognized algorithm')

      if keytype == 'PUBLIC' or keytype == 'SHAREDSECRET':
         key = Point(curve, data["Kx"], data["Ky"])
      elif keytype == 'PRIVATE':
         key = data["K"]
      else:
         raise Exception('Reading key : Key type error')
         
      f.close()
      return (curve, key)
      
