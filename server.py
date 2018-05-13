import socket
import threading

from connection import connect_client

TCP_PORT = 5000
BUFFER_SIZE = 1024

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    thread = threading.Thread(target = connect_client, args=[clients, BUFFER_SIZE, conn, addr] )
    thread.start()
