#
# elgamal - Elgamal with elliptic curve.
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
   def readFile(path):
      f = open(path, "r")
      filecontent = f.read()
      f.close()
      return filecontent

   """ writeFile
   
   """ 
   def writeFile(path, content):
      f = open(path, "w")
      f.write(content)
      f.close()


""" Key

"""      
class key(object):

   """ writeKey
   ELGAMAL, ECDSA
   """
   def writeKey(path, algo, curve, key):
      f = open(path, "w")
      
      if algo is 'ELGAMAL':
         if isinstance(key, Point):
            keytype= 'PUBLIC'
         elif isinstance(key, int):
            keytype= 'PRIVATE'
         else:
            raise Exception('Writing key : Key type error')
      
         #f.write( str(base64.b64encode( str(curve.p).encode('ascii'))) )

         f.write("-----BEGIN " + algo + " " + keytype + " KEY-----\n")
         f.write("p="+str(curve.p)+"\n")
         f.write("n="+str(curve.n)+"\n")
         f.write("a4="+str(curve.a4)+"\n")
         f.write("a6="+str(curve.a6)+"\n")
         f.write("r4="+str(curve.r4)+"\n")
         f.write("r6="+str(curve.r6)+"\n")
         f.write("gx="+str(curve.gx)+"\n")
         f.write("gy="+str(curve.gy)+"\n")
         f.write("r="+str(curve.r)+"\n")
         
         if isinstance(key, Point):
            f.write("Kx="+str(key.x)+"\n")
            f.write("Ky="+str(key.y)+"\n")
         elif isinstance(key, int):
            f.write("K="+str(key)+"\n")
         else:
            raise Exception('Writing key : Key type error')
         
         f.write("-----END " + algo + " " + keytype + " KEY-----\n")
      elif algo is 'ECDSA':
         keytype = 'PRIVATE'
         f.write("-----BEGIN " + algo + " " + keytype + " KEY-----\n")
         f.write("-----END " + algo + " " + keytype + " KEY-----\n")
      else:
         raise Exception('Writing key : Unrecognized algorithm')
         
      f.close()

   """ readKey
   
   """
   def readKey(path):
      data = {}
      f = open(path, "r")
      lines = f.readlines()
      algo = lines[0].split(' ')[1]
      keytype = lines[0].split(' ')[2]
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
      
      if algo == 'ELGAMAL':
         if keytype == 'PUBLIC':
            key = Point(curve, data["Kx"], data["Ky"])
         elif keytype == 'PRIVATE':
            key = data["K"]
         else:
            raise Exception('Reading key : Key type error')
      elif algo == 'ECDSA':
         print('TODO')
      else:
         raise Exception('Reading key : Unrecognized algorithm')
         
      f.close()
      return (curve, key)
      
