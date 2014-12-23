import socket
from .elliptic import EllipticCurve
from .point import Point
from .tools import message

""" stools
 STS and DH tools for secret exchange using socket
"""
class stools(object):

   """ curve_exchange
    Test if the server and the client are using the same curve
    Warning :  Only the minimal nomber of parameter for a curve is sended.
               Therefore the comparaison is etablished with p, n, a4 and a6
    Input : 
    - curve (EllipticCurve)
    Ouput :
    - True if server and client are on the same curve
    - False otherwise
   """
   def curve_exchange(socket, curve):
      curve_bytes = (str(curve.p) + "," + str(curve.n) + "," +
                     str(curve.a4) + "," + str(curve.a6)).encode()
      
      print(" Sending curve to the client")
      message.send(socket, curve_bytes)
      
      print(" Getting server's curve")
      curve_bytes_client = message.get(socket)
      
      curve_str = curve_bytes_client.decode()
      curve_str = curve_str.split(',')
      curve_client = EllipticCurve( int(curve_str[0]), int(curve_str[1]), 
                                    int(curve_str[2]), int(curve_str[3]), 
                                    curve.r4, curve.r6, curve.gx, curve.gy,
                                    curve.r)
      
      return (curve == curve_client)
      
      
   """ secret_exchange
    For DH and STS
    Input :
    - server (bool)
    - socket (socket)
    - gx (Point)
    Output :
    - gy (Point)
   """   
   def secret_exchange(server, socket, gx):
      gx_bytes = (str(gx.x) + "," + str(gx.y)).encode()
      
      if server is True:
         print(" Sending secret to client : g^x")
         message.send(socket, gx_bytes)
         
         print(" Getting client's secret : g^y")
         gy_bytes = message.get(socket)
      else:
         print(" Getting server's secret : g^y")
         gy_bytes = message.get(socket)
         
         print(" Sending secret to server : g^x")
         message.send(socket, gx_bytes)
         
      gy_str = gy_bytes.decode()
      (gy_str_x, gy_str_y) = gy_str.split(',')
      gy = Point(gx.curve, int(gy_str_x), int(gy_str_y))
      return gy
      
   """ sharedsecret_exchange
    For STS protocol only
    Input :
    - server (bool)
    - socket (socket)
    - ecdsa_publickey (Point) (certificat)
    - encrypted (bytes)
    - iv (bytes)
    Ouptut :
    - certificat_new (Point) (certificat)
    - encrypted_new (bytes)
    - iv_new (bytes)
   """
   def sharedsecret_exchange(server, socket, ecdsa_publickey, encrypted, iv):
      certificat_bytes = (str(ecdsa_publickey.x)+","+str(ecdsa_publickey.y)).encode()
      if server is True:
         print(" Sending to the client :")
         print("  - Public ecdsa key certificate")
         message.send(socket, certificat_bytes)
         print("  - Signature encrypted")
         message.send(socket, encrypted)
         message.send(socket, iv)
         
         print(" Getting from the client :")
         print("  - Public ecdsa key certificate")
         certificat_bytes_new = message.get(socket)
         
         print("  - Signature encrypted")
         encrypted_new = message.get(socket)
         iv_new = message.get(socket)
      else:
         print(" Getting from the server :")
         print("  - Public ecdsa key certificate")
         certificat_bytes_new = message.get(socket)
         print("  - Signature encrypted")
         encrypted_new = message.get(socket)
         iv_new = message.get(socket)
         
         print(" Sending to the server :")
         print("  - Public ecdsa key certificate")
         message.send(socket, certificat_bytes)
         
         print("  - Signature encrypted")
         message.send(socket, encrypted)
         message.send(socket, iv)
      
      certificat_str = certificat_bytes_new.decode()
      (certificat_str_x, certificat_str_y) = certificat_str.split(',')
      certificat_new = Point(ecdsa_publickey.curve, int(certificat_str_x), int(certificat_str_y))
      return (certificat_new, encrypted_new, iv_new)
      
