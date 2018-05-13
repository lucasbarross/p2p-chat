import socket
import json
import threading

SERVER_TCP_IP = '127.0.0.1'
SERVER_TCP_PORT = 5000
BUFFER_SIZE = 1024

class Listener(): 

    def __init__(self, username, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.username = username

    def listen(self):
        self.socket.bind(('127.0.0.1', self.port))
        self.socket.listen()

    def run(self):
        while 1:
            try: 
                connection, addr = self.socket.accept()
                print("Hey, someone connected with you!")
                input_thread = InputReader(self.username, True, connection)
                input_thread.start()
                while 1: 
                    message_received = connection.recv(BUFFER_SIZE).decode()
                    print(message_received)
            except:
                print("Who you connected to is not online anymore.")

class Opener(): 

    def __init__(self, username, address):
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = username

    def run(self):
        try:
            self.socket.connect(self.address)
            self.connected = True
            input_thread = InputReader(self.username, True, self.socket)
            input_thread.start()
            while 1:
                message_received = self.socket.recv(BUFFER_SIZE).decode()
                print(message_received)
        except:
            print("Who you connected to is not online anymore.")
            input_thread.connected = False


class InputReader(threading.Thread):

    def __init__(self, username, connected, connection):
        super().__init__()
        self.connected = connected
        self.connection = connection
        self.username = username

    def run(self):
        while self.connected:
            message = input()
            prefix = self.username + ": "
            self.connection.send((prefix + message).encode())

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.connect((SERVER_TCP_IP, SERVER_TCP_PORT))

### ASKING USERNAME AND SHOWING LISTS OF USERS ONLINE.
name = input("Welcome to ZIPZAPLERSON! Your username, sir: ")
socket_server.send(name.encode())

my_port = int(socket_server.recv(BUFFER_SIZE).decode())

users_online = socket_server.recv(BUFFER_SIZE).decode()
print(users_online)

choice = ''

while (choice != 'c' and choice != 'w'): 
    choice = input("Do you want to connect to someone or wait a connection? (c/w) ")
    if choice == 'c':
        print("here")
        user_chosen = input("Type the number of who you want to connect to: ")
        socket_server.send(user_chosen.encode())
        address = socket_server.recv(BUFFER_SIZE).decode().split(',')
        Opener(name, (address[0], int(address[1]))).run()
    elif choice == 'w':
        print("Waiting...")
        socket_server.send('no'.encode())
        listen_client = Listener(name, my_port)
        listen_client.listen()
        listen_client.run()
    else:
        print("Invalid command")