# Import socket module
from socket import *
import os

# Programming Assignment 2
# Bradley Manzo
# Dayton Harvey

serverPort = 6789
proxyPort = 8888

# TCP Welcoming Socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# create TCP socket on client to use for connecting to remote server.  
clientSocket = socket(AF_INET, SOCK_STREAM)

# Bind Server socket to listen for clients
serverSocket.bind(('', proxyPort))
serverSocket.listen(1) #numer of allowed clients = 1

# Server should be up and running and listening to the incoming connections
while True:
		print('Ready to serve...')
		
		# Set up a new connection from the client
		connectionSocket, addr = serverSocket.accept()
		try:
			message =  connectionSocket.recv(4096).decode()
			filename = message.split()[1]
			print(filename[1:])
			
			# Look for file in cache
			if os.path.exists(filename[1:]):
						# Open file and send data to client
						f = open(filename[1:], 'rb')
						cached_data = f.read()
						connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
						connectionSocket.send(cached_data)
						print('file ' + filename[1:] + ' in cache')
						f.close()
						connectionSocket.close()
			else:
						print('file ' + filename[1:] + ' not in cache')
						# Initiates socket with main server to recieve file
						clientSocket.connect(('localhost', serverPort))
						# Sends GET to main server
						clientSocket.send(b'GET /'+ filename[1:].encode() + b' HTTP/1.1\r\n\r\n')
						# Receives first chunk with header information
						server_response = clientSocket.recv(4096).decode()
						# separates header from first chunk of info, (must decoded)
						header = server_response.split('\r\n\r\n')[0]
						# rest of data from first chunk, (has to stay encoded)
						data = "\r\n\r\n".join(server_response.split("\r\n\r\n")[1:])
						# 200 OK if on main server
						if header == 'HTTP/1.1 200 OK':
								# send 200 OK to client along with encoded data from first chunk
								connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
								connectionSocket.send(data.encode())
								# open file in cache to write to
								f = open(filename[1:],'wb')
								# write first chunk of data encoded
								f.write(data.encode())
								# While data is being received, write to file and send to client
								while server_response:
									server_response = clientSocket.recv(4096)
									f.write(server_response)
									connectionSocket.send(server_response)
						else:
								# otherwise just send the response from the main server
								connectionSocket.send(server_response.encode())
						clientSocket.close()
						server_response = ''

			message = ''
			server_response = ''
		except IOError:
			# If file is unable to be opened, 404 is sent to client
			connectionSocket.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')
			connectionSocket.close()

serverSocket.close()