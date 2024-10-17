# Import socket module
from socket import *

# Programming Assignment 2
# Bradley Manzo
# Dayton Harvey

serverPort = 6789

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Fill in start

serverSocket.bind(('', serverPort))
serverSocket.listen(1)  #numer of allowed clients = 1

# Fill in end 

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()          #Fill in end
    
    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message =  connectionSocket.recv(4096).decode()         #Fill in end
        filename = message.split()[1]
        print(filename[1:])
        f = open(filename[1:],'rb')
        # Store the entire contenet of the requested file in a temporary buffer
        outputdata = f.read()         #Fill in end

        # Send the HTTP response header line to the connection socket
	# Fill in start
	
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')

        # Fill in end
 
	# Send the content of the requested file to the connection socket

        connectionSocket.send(outputdata)

        print('file ' + filename[1:] + ' found!')

        message = ''
        # Close the client connection socket
        
        connectionSocket.close()
        
    except IOError:
        # Send HTTP response message for file not found
	# Fill in start
        connectionSocket.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

        print('file ' + filename[1:] + ' not found :( ')

        # Fill in end
	
	# Close the client connection socket
	# Fill in start
        connectionSocket.close()
	# Fill in end

serverSocket.close()