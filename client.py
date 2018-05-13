import socket
import threading
import atexit

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
        self.listen()
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.connected = False
        self.username = username

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
            print("Who you connected to is not online.")
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

def exit_handler(client_id, server_socket):
    server_socket.connect((SERVER_TCP_IP, SERVER_TCP_PORT))
    server_socket.send('disconnect'.encode())
    server_socket.send(client_id)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((SERVER_TCP_IP, SERVER_TCP_PORT))
### ASKING USERNAME AND SHOWING LISTS OF USERS ONLINE.
name = input("Welcome to ZIPZAPLERSON! Your username, sir: ")

server_socket.send('connect'.encode())
server_socket.send(name.encode())

my_info = server_socket.recv(BUFFER_SIZE).decode().split(',')
my_port = int(my_info[1])
my_id = my_info[0].encode()

users_online = server_socket.recv(BUFFER_SIZE).decode()
print(users_online)

choice = ''

while (choice != 'c' and choice != 'w'): 
    choice = input("Do you want to connect to someone or wait a connection? (c/w) ")

    if choice == 'c':
        user_chosen = input("Type the number of who you want to connect to: ")
        server_socket.send(user_chosen.encode())
        address = server_socket.recv(BUFFER_SIZE)
        if address[0:1] == b'\x11' or address[0:1] == b'\x12':
            # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # server_socket.connect((SERVER_TCP_IP, SERVER_TCP_PORT))
            # server_socket.send("users".encode())
            # users_online = server_socket.recv(BUFFER_SIZE).decode()
            # print(users_online)
            print(address.decode())
            choice = ''
        else:
            address = address.decode().split(',')
            Opener(name, (address[0], int(address[1]))).run()
    elif choice == 'w':
        print("Waiting...")
        server_socket.send('wait'.encode())
        Listener(name, my_port).run()
    else:
        print("Invalid command")

atexit.register(exit_handler, client_id=my_id, server_socket=server_socket)