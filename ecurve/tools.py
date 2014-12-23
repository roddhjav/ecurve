import struct
from .elliptic import EllipticCurve
from .point import Point

""" tools
 Read curve, I/O files
"""
class tools(object):

   """ loadCurve
    Read a curve's file in .gp format (see curves/README.md)
    Input :
    - path (String) Path of the curve's file
    Output :
    - curve (EllipticCurve)
   """
   @staticmethod
   def loadCurve(path):
      with open(path, "r") as file:
         data = {}
         lines = file.readlines()
         for line in lines:
            (var, val) = line.split('=')
            data[var] = int(val)
         
         curve = EllipticCurve(  data["p"], data["n"], data["a4"], data["a6"],
                                 data["r4"], data["r6"], data["gx"], data["gy"],
                                 data["r"])
         file.close()
      return curve
      
   """ readFile
    Read a plain text file
    Input :
    - path (String) Path of the file
    Output :
    - filecontent (String)
   """
   @staticmethod
   def readFile(path):
      f = open(path, "r", encoding='utf-8')
      filecontent = f.read()
      f.close()
      return filecontent

   """ writeFile
    Write a plain text file
    Input : 
    - path (String) Path of the file
    - content (String)
   """ 
   @staticmethod
   def writeFile(path, content):
      f = open(path, "w")
      f.write(content)
      f.close()



""" Key
 I/O functions for the keys
"""      
class key(object):

   """ writeKey
    Write ELGAMAL, ECDSA or DIFFIEHELLMAN public and private key in a file
    Input :
     - path (string) key path (a public key will have .pub)
     - algo (string) algo type : ELGAMAL or ECDSA or DIFFIEHELLMAN
     - curve (EllipticCurve) The elliptic curve used
     - key (int or Point) The key
   """
   @staticmethod
   def writeKey(path, algo, curve, key):
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
      
      with open(path, "w") as file:
         file.write("-----BEGIN " + algo + " " + keytype + " KEY-----\n")
         file.write("p=" + str(curve.p) + "\n")
         file.write("n=" + str(curve.n) + "\n")
         file.write("a4=" + str(curve.a4) + "\n")
         file.write("a6=" + str(curve.a6) + "\n")
         file.write("r4=" + str(curve.r4) + "\n")
         file.write("r6=" + str(curve.r6) + "\n")
         file.write("gx=" + str(curve.gx) + "\n")
         file.write("gy=" + str(curve.gy) + "\n")
         file.write("r=" + str(curve.r) + "\n")
         if isinstance(key, Point):
            file.write("Kx=" + str(key.x) + "\n")
            file.write("Ky=" + str(key.y) + "\n")
         elif isinstance(key, int) or isinstance(key, long):
            file.write("K=" + str(key) + "\n")
         file.write("-----END " + algo + " " + keytype + " KEY-----\n")
         file.close()
      
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
      with open(path, "r") as file:
         data = {}
         lines = file.readlines()
         algo = lines[0].split(' ')[1]    # algo = ELGAMAL or ECDSA or DH
         keytype = lines[0].split(' ')[2] # keytype = PUBLIC or PRIVATE
         lines = lines[1:len(lines)-1]
         for line in lines:
               (var, val) = line.split('=')
               data[var] = int(val) 
         
         curve = EllipticCurve(  data["p"], data["n"], data["a4"], data["a6"],
                                 data["r4"], data["r6"], data["gx"], data["gy"],
                                 data["r"])
         
         if algo != 'ELGAMAL' and algo != 'ECDSA' and algo != 'DIFFIEHELLMAN':
            raise Exception('Reading key : Unrecognized algorithm')
         if keytype == 'PUBLIC' or keytype == 'SHAREDSECRET':
            key = Point(curve, data["Kx"], data["Ky"])
         elif keytype == 'PRIVATE':
            key = data["K"]
         else:
            raise Exception('Reading key : Key type error')
         file.close()
      return (curve, key)

"""
 Easy to use socket functions
""" 
class message(object):

   """ send
    Send a message throught a socket
    Input :
    - socket (Socket)
    - msg (bytes)
   """
   @staticmethod 
   def send(socket, msg):
      length = struct.pack('!I', len(msg))
      socket.send(length + msg)
      
   """ get
    Get a message from a socket
    Input :
    - socket (Socket)
    Output :
    - msg (bytes)
   """
   @staticmethod
   def get(socket):
      l = socket.recv(4)
      l_buff = struct.unpack('!I', l)[0]
      msg = socket.recv(l_buff)
      return msg
   
