
# import the socket library 
import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl   
  
listen_addr = '127.0.0.1'
# reserve a port on your computer in our 
# case it is 9500 but it can be anything 
port = 9500   
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

# next create a socket object 
s = socket.socket()          
print("Socket successfully created")              
  
# Next bind to the port 
s.bind(('', port))         
print("socket binded to %s" %(port))
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening")           
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
    print('Waiting for client')
    # Establish connection with client. 
    c, addr = s.accept()      
    print('Got connection from', addr)
    print("Client connected: {}:{}".format(addr[0], addr[1])) 
    conn = context.wrap_socket(c, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert()))    

    data = conn.recv(1024).decode()
    if (data == 'Hello'): 
        conn.send('Hi'.encode())
    else:
        conn.send('Goodbye'.encode())
    # Close the connection with the client 
    print("Closing connection")
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()