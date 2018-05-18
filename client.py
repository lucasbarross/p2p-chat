import socket
import threading
import atexit
import time

from datetime import datetime
from actions import connect, choose_user, ask_users

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
        self.connected = False

    def listen(self):
        self.socket.bind(('127.0.0.1', self.port))
        self.socket.listen()

    def send_confirmation_packet(self):
        while not self.connected:
            time.sleep(2)
            if not self.connected:
                self.server_socket.send("Ok!".encode())

    def run(self):
        self.listen()
        input_thread = None
        #next_time = datetime.now() + 2000
        try:
            while 1:
                threading.Thread(target = self.send_confirmation_packet).start()
                connection, addr = self.socket.accept()
                self.connected = True
                self.server_socket.close()
                print("Hey, someone connected with you!")
                input_thread = InputReader(self.username, True, connection)
                input_thread.start()
                while 1: 
                    message_received = connection.recv(BUFFER_SIZE).decode()
                    print(message_received)
        except:
            input_thread.flag(False)
            print("Who you connected to is not online anymore.")
                
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
            self.server_socket.close()
            input_thread.start()
            while 1:
                message_received = self.socket.recv(BUFFER_SIZE).decode()
                print(message_received)
        except socket.error:
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

name = input("Welcome to ZapZiplerson! Your username, sir: ")
ask_users(server_socket)
choice = ''

while (choice != 'c' and choice != 'w'): 
    choice = input("Do you want to connect to someone, wait a connection or refresh online users list? (c/w/r) ")

    if choice == 'c':
        address = choose_user(id, server_socket)
        if address[0:1] == b'\x11' or address[0:1] == b'\x12':
            ask_users(server_socket)
            print(address.decode())
            choice = ''
        else:
            address = address.decode().split(',')
            Opener(name, (address[0], int(address[1])), id, server_socket).run()
    elif choice == 'w':
        my_info = connect(server_socket, name)
        id, port = my_info
        print("Waiting...")
        Listener(name, port, id, server_socket).run()
    elif choice == 'r':
        ask_users(server_socket)
    else:
        print("Invalid command")

    