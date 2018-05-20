import socket, pickle
import threading

BUFFER_SIZE = 1024
TCP_PORT = 5000
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

def listen_client(conn, addr):
    info = pickle.loads(conn.recv(BUFFER_SIZE))
    connected_arr = pickle.dumps(clients)
    conn.send(connected_arr)
    clients.append(info)
    try: 
        while 1:
            conn.settimeout(3)
            confirmation = conn.recv(BUFFER_SIZE)
    except Exception as err:
        clients.pop(clients.index(info))

print('Im listening on port ' + str(TCP_PORT))

while 1:
    conn, addr = s.accept()
    thread = threading.Thread(target = listen_client, args=[conn, addr] )
    thread.start()

