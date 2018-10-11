# import the socket library 
import socket, ssl, pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP
from Crypto.Hash import SHA
from Crypto import Random

from ca import generateCertAndKeys 
  
listen_addr = '127.0.0.1'
# reserve a port on your computer 
port = 9500   
# server_cert = 'server.crt'
encrypt_str = "encrypted_message="
sessionCipherKey_str = "sessionCipherKey="

filename, publicKey, private, certificate = generateCertAndKeys()
#Generate private and public keys
# random_generator = Random.new().read
# private_key = RSA.generate(1024, random_generator)
# public_key = private_key.publickey()

pem = private.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

privKey = RSA.importKey(pem)

sessionCipherKey = PKCS1_OAEP.new(privKey)  

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

# a forever loop until we interrupt it or  
# an error occurs 
while True: 
    # Wait until data is received
    data = c.recv(1024)
    data = data.replace("\r\n", '') #remove new line character

    if(data == "Initiated"):
        c.send(filename.encode())
        print("Sending client server certificate to authenticate")
    elif(sessionCipherKey_str in data):
        data = data.replace(sessionCipherKey_str, '')
        # sessionCipherKey = PKCS1_v1_5.new(privateKey)
        print("Session cipher key recieved: " + str(sessionCipherKey))
        # The server will decrypt the 'session cipher key' using its private key
        # privateKey.decrypt(sessionCipherKey)
        c.send("Acknowledgment".encode())
        print("Sending acknowledgment that sessionCipherKey recieved")
    elif(encrypt_str in data): #Reveive encrypted message and decrypt it
        data = data.replace(encrypt_str, '')
        print("Received: Encrypted message = " + str(data))
        # encrypted = eval(data)
        decrypted = sessionCipherKey.decrypt(data)
        c.send("Server: OK".encode())
        print("Decrypted message = " + decrypted)

    else:
        break

# Close the connection with the client 
print("Closing connection")
c.send("Server stopped".encode())
c.close()