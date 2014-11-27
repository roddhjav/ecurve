#!/usr/bin/env python

from elliptic import *
from point import *
from diffiehellman import *
import socket
import threading


class DHThread(threading.Thread):
   def __init__(self,curve, IP, port):
      self.curve = curve
      threading.Thread.__init__(self)
      self.IP = IP
      self.port = port
   
   def run(self):
      dh = DH(self.curve,"jacques")
      dh.exchange_key(self.IP,self.port)
      print dh.name+" sent\n"

p=8884933102832021670310856601112383279507496491807071433260928721853918699951
n=8884933102832021670310856601112383279454437918059397120004264665392731659049
a4=2481513316835306518496091950488867366805208929993787063131352719741796616329
a6=4387305958586347890529260320831286139799795892409507048422786783411496715073
r4=5473953786136330929505372885864126123958065998198197694258492204115618878079
r6=5831273952509092555776116225688691072512584265972424782073602066621365105518
gx=7638166354848741333090176068286311479365713946232310129943505521094105356372
gy=762687367051975977761089912701686274060655281117983501949286086861823169994
r=8094458595770206542003150089514239385761983350496862878239630488323200271273

IP = "localhost"
port = 10000

curve = EllipticCurve(p, n, a4, a6, r4, r6, gx, gy, r)
Alice = DHThread(curve,IP,port)
Bob = DHThread(curve,IP,port)

nb_clients=0

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP,port))
serversocket.listen(1)
connections = []
messages = []

Alice.start()
Bob.start()

while nb_clients<2:
   connection, address = serversocket.accept()
   buf = connection.recv(1024)
   connections.append(connection)
   messages.append(buf)
   nb_clients = nb_clients+1

connections[1].send(messages[0])
connections[0].send(messages[1])

Alice.join()
Bob.join()


#assert AliceDH.gba == BobDH.gba, "Error AliceDH.gba != BobDH.gba"

