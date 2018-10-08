# Import socket module 
import socket, ssl    
from Crypto.PublicKey import RSA
from ca import validateCert 
  
# Define the port on which you want to connect 
port = 9500          
host = '127.0.0.1'
server_cert = 'server.crt'  
host_name = 'Sanaa Fidahussain' 

# Returns a new context with secure default setting
context = validateCert(server_cert)

# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

# Wrap an existing Python socket sock and return an instance of SSLContext
# The returned SSL socket is tied to the context, its settings and certificates. 
conn = context.wrap_socket(s, server_side=False, server_hostname=host_name)

# connect to the server on local computer 
conn.connect((host, port))
# print("SSL established. Peer: {}".format(conn.getpeercert()))
print("SSL established.")

#Tell server that connection is OK
conn.send("Client: OK".encode())

#Receive public key string from server
serverPublicKeyString = conn.recv(1024).decode()
print('Received public key from server.')

#Remove extra characters
serverPublicKeyString = serverPublicKeyString.replace("public_key=", '')
print('Replacing string with {}'.format(serverPublicKeyString))

#Convert string to key
serverPublicKey = RSA.importKey(serverPublicKeyString)

#Encrypt message and send to server
message = "This is my secret message."
encrypted = serverPublicKey.encrypt(message, 32)

print('Sending encrypted message: {}'.format(str(encrypted)))
conn.send("encrypted_message=".encode()+str(encrypted).encode())

#Server's response
response = conn.recv(1024).decode()
if(response == "Server: OK"):
    print("Server decrypted message successfully")

#Tell server to finish connection
conn.send("Quit".encode())
#Quit server response
print(conn.recv(1024).decode()) 
conn.close()