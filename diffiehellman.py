import math
import random
from elliptic import *
from point import *

#Add exchange over network
#Check if random function is truly random
# TODO : Add comment about var
class DH(object):
   def __init__(self, curve, name):
      self.curve = curve
      self.name = name
      bits = int(math.log(curve.n,2))

      self.a = random.getrandbits(bits-1) # See if it is a secure random
      
      assert self.a < self.curve.n, "Error"
      
      self.g = Point(self.curve, self.curve.gx,  self.curve.gy)
      self.ga = self.a*self.g
      
      print("a   =", self.a)
      print("g   =", self.g)
      print("g^a =", self.ga)
      
   def setkey(self, gb):
      self.gba = self.a*gb
   
   def proxy_key(self,IP,port):
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serversocket.bind((IP,port))
      serversocket.listen(1)
      
      connection, address = serversocket.accept()
      buf = connection.recv(256)
      
      if len(buf) > 0:
         print buf
#need a server that acts as and interface between the two clients
#most likely that server will be implemented in the test programm
   def exchange_key(self,IP,port):
      clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      clientsocket.connect((IP,port))
      clientsocket.send(name+":"+self.ga)
      reply = s.recv(1024)
   
