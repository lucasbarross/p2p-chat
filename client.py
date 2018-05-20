import socket, pickle
import threading
import time

SERVER_TCP_IP = '127.0.0.1'
SERVER_TCP_PORT = 5000
BUFFER_SIZE = 1024

class Client:

    def __init__(self):
        self.users = []
        self.sockets = []
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def listen(self):
        self.listen_socket.bind(('127.0.0.1', 0))
        self.listen_socket.listen(1)
        return self.listen_socket.getsockname()
    
    def wait(self):
        print("You`re connected to ZapZiplerson.")
        while 1:
            conn, addr = self.listen_socket.accept()
            self.sockets.append(conn)
            threading.Thread(target = self.get_messages, args=[conn]).start()
        
    def get_messages(self, socket):
        try:
            while 1:
                message_received = socket.recv(BUFFER_SIZE).decode()
                print(message_received)
        except ConnectionResetError:
            print('Someone disconnected.')
    
    def confirmation_packet(self, server_socket):
        try: 
            while 1:
                time.sleep(2)
                server_socket.send('ok'.encode())
        except ConnectionResetError:
            print("Alert: server is not online anymore, by luck this is a P2P app.")
    
    def connect(self, server_socket):
        
        for user in self.users:
            conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockets.append(conn_socket)
            conn_socket.connect(user)

        for sock in self.sockets:
            threading.Thread(target = self.get_messages, args=[sock]).start()

        threading.Thread(target = self.wait).start()
        threading.Thread(target = self.confirmation_packet, args = [server_socket]).start()
        threading.Thread(target = self.send_message).start()
    
    def send_message(self):
        
        while 1:
            message = input()
            invalid_clients = []

            for index, socket in enumerate(self.sockets):
                try:
                    socket.send(message.encode())
                except:
                    print("erro")
                    invalid_clients.append(socket)
            
            for invalid in invalid_clients:
                self.sockets.pop(self.sockets.index(invalid))

    def set_users(self, users):
        self.users = users

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((SERVER_TCP_IP, SERVER_TCP_PORT))
client = Client()
info = pickle.dumps(client.listen())
server_socket.send(info)
connected_arr = server_socket.recv(BUFFER_SIZE)
connected_arr = pickle.loads(connected_arr)
client.set_users(connected_arr)
client.connect(server_socket)