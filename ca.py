
# Import socket module 
import socket, ssl              

# Accepts cert and returns public key associated with certificate 
# or null if certificate isn't recognized

def validateCert(server_cert):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.verify_mode = True
    context.load_verify_locations(server_cert)
    return context