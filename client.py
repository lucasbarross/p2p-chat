import socket
import threading
import atexit

from actions import connect, disconnect, choose_user, ask_users

SERVER_TCP_IP = '127.0.0.1'
SERVER_TCP_PORT = 5000
BUFFER_SIZE = 1024
class Listener(): 

    def __init__(self, username, port, id, server_socket):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = server_socket
        self.username = username
        self.port = port
        self.id = id

    def listen(self):
        self.socket.bind(('127.0.0.1', self.port))
        self.socket.listen()

    def run(self):
        self.listen()
        input_thread = None
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
                input_thread.flag(False)
                print("Who you connected to is not online anymore.")
                disconnect(self.id, self.server_socket)
                break
class Opener(): 

    def __init__(self, username, address, id, server_socket):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = server_socket
        self.address = address
        self.connected = False
        self.username = username
        self.id = id

    def run(self):
        input_thread = InputReader(self.username, True, self.socket)
        try:
            self.socket.connect(self.address)
            self.connected = True
            input_thread.start()
            while 1:
                message_received = self.socket.recv(BUFFER_SIZE).decode()
                print(message_received)
        except socket.error:
            disconnect(self.id, self.server_socket)
            input_thread.flag(False)
            print("Who you connected to is not online anymore.")

class InputReader(threading.Thread):

    def __init__(self, username, connected, connection):
        super().__init__()
        self.connected = connected
        self.connection = connection
        self.username = username
    
    def flag(self, bool):
        self.connected = bool

    def run(self):
        while 1:
            message = input()
            if self.connected:
                prefix = self.username + ": "
                self.connection.send((prefix + message).encode())
            else:
                break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((SERVER_TCP_IP, SERVER_TCP_PORT))
### ASKING USERNAME AND SHOWING LISTS OF USERS ONLINE.

my_info = connect(server_socket)
name, id, port = my_info

ask_users(server_socket)
choice = ''

while (choice != 'c' and choice != 'w'): 
    choice = input("Do you want to connect to someone or wait a connection? (c/w) ")

    if choice == 'c':
        address = choose_user(server_socket)
        if address[0:1] == b'\x11' or address[0:1] == b'\x12':
            ask_users(server_socket)
            print(address.decode())
            choice = ''
        else:
            address = address.decode().split(',')
            Opener(name, (address[0], int(address[1])), id, server_socket).run()
    elif choice == 'w':
        print("Waiting...")
        Listener(name, port, id, server_socket).run()
    else:
        print("Invalid command")

    