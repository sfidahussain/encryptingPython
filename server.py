# import the socket library 
import socket, ssl   
from Crypto.PublicKey import RSA
from Crypto import Random
  
listen_addr = '127.0.0.1'
# reserve a port on your computer 
port = 9500   
server_cert = 'server.crt'
# server key associated with certificate
server_key = 'server.key'
encrypt_str = "encrypted_message="

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)

# next create a socket object 
s = socket.socket()          
print("Socket successfully created")              
  
# Next bind to the port 
s.bind(('', port))         
print("socket binded to %s" %(port))
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening")           
  
print('Waiting for client')
# Establish connection with client. 
c, addr = s.accept()      
print("Client connected: {}:{}".format(addr[0], addr[1])) 
conn = context.wrap_socket(c, server_side=True)
print("SSL established.")    

# a forever loop until we interrupt it or  
# an error occurs 
while True: 
    # Wait until data is received
    data = conn.recv(1024).decode()
    data = data.replace("\r\n", '') #remove new line character

    if(data == "Client: OK"):
        conn.send("public_key=".encode() + public_key.exportKey().encode())
        print("Public key sent to client.")

    elif(encrypt_str in data): #Reveive encrypted message and decrypt it.
        data = data.replace(encrypt_str, '')
        print("Received: Encrypted message = " + str(data))
        encrypted = eval(data)
        decrypted = private_key.decrypt(encrypted)
        conn.send("Server: OK".encode())
        print("Decrypted message = " + decrypted)

    elif(data == "Quit"): 
        break

# Close the connection with the client 
print("Closing connection")
conn.send("Server stopped".encode())
conn.close()