# Import socket module 
import socket, ssl, pickle  
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA

from ca import validateCert 
  
# Define the port on which you want to connect 
port = 9500          
host = '127.0.0.1'

# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

# connect to the server on local computer 
s.connect((host, port))

# Initiate contact with server
print('Initiating contact with server')
s.send("Initiated".encode())

#Receive cert from server
serverCert = s.recv(1024).decode()
print('Received {} from server.'.format(serverCert))

# Send cert file to CA for validation
key = validateCert(serverCert)
print('Key given back from CA: {}'.format(str(key)))

if(key != "Goodbye"):
    #Encrypt key to session cipher key USING public key
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    pubKey = RSA.importKey(pem)
    sessionCipherKey = PKCS1_OAEP.new(pubKey)

    print('Sending cipher key: {}'.format(str(sessionCipherKey)))
    # Send encrypted session key
    # data = pickle.dumps(sessionCipherKey)
    s.send("sessionCipherKey=" + str(sessionCipherKey))
    # Should recieve acknowledgment if server is using session cipher key
    acknowledgment = s.recv(1024).decode()

    #Encrypt message and send to server
    message = b'This is my secret message.'
    h = SHA.new(message)
    encrypted = sessionCipherKey.encrypt(message)

    print('Sending encrypted message: {}'.format(str(encrypted)))
    # print('Sending decrypted message: {}'.format(str(decrypted)))

    # encryptedData = pickle.dumps(encrypted)
    s.send("encrypted_message=" + encrypted)

    #Server's response
    response = s.recv(1024).decode()
    if(response == "Server: OK"):
        print("Server decrypted message successfully")
    #Tell server to finish connection
    s.send("Quit".encode())

else:
    # Will send 'Goodbye' since certificate is not valid
    s.send(str(key).encode())

#Quit server response
print(s.recv(1024).decode()) 
s.close()