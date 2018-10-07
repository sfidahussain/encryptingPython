
# Import socket module 
import socket, ssl              

# Message to send from client
MESSAGE = "Hello"    
  
# Define the port on which you want to connect 
port = 9500          
host = '127.0.0.1'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'   
host_name = 'Sanaa Fidahussain' 

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)  

# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

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