# Import socket module 
import socket, ssl    
from ca import *

# Message to send from client
MESSAGE = "Hello"    
  
# Define the port on which you want to connect 
port = 9500          
host = '127.0.0.1'
server_cert = 'server.crt'  
host_name = 'Sanaa Fidahussain' 

# Returns a new context with secure default setting
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.verify_mode = True
context.load_verify_locations(server_cert)

# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

# Wrap an existing Python socket sock and return an instance of SSLContext
# The returned SSL socket is tied to the context, its settings and certificates. 
conn = context.wrap_socket(s, server_side=False, server_hostname=host_name)

# connect to the server on local computer 
conn.connect((host, port))
print("SSL established. Peer: {}".format(conn.getpeercert()))

print("Sending: 'Hello, world!")
conn.send(MESSAGE.encode())

# receive data from the server 
data = conn.recv(1024).decode()
print('Server sent: ', data)

print("Closing connection")
conn.close()