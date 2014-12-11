import socket
from point import Point
from tools import message

class stools(object):

   """ secret_exchange
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
         print(" Sending secret to client")
         message.send(socket, gx_bytes)
      
         print(" Getting client's secret")
         gy_bytes = message.get(socket)
      else:
         print(" Getting server's secret")
         gy_bytes = message.get(socket)
         
         print(" Sending secret to server")
         message.send(socket, gx_bytes)
      
      gy_str = gy_bytes.decode()
      (gy_str_x, gy_str_y) = gy_str.split(',')
      gy = Point(gx.curve, int(gy_str_x), int(gy_str_y))
      return gy
      
   """ sharedsecret_exchange

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
         print("  - Public key certificate")
         certificat_bytes_new = message.get(socket)
         
         print("  - Signature encrypted")
         encrypted_new = message.get(socket)
         iv_new = message.get(socket)
      else:
         print(" Getting from the server :")
         print("  - Public key certificate")
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
