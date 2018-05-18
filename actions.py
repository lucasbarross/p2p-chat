def choose_user(client_id, server_socket, buffer_size = 1024):
    user_chosen = input("Type the number of who you want to connect to: ")
    server_socket.send('connect_to'.encode())
    server_socket.send(user_chosen.encode())
    address = server_socket.recv(buffer_size)
    return address

def ask_users(server_socket, buffer_size = 1024):
    server_socket.send('users'.encode())
    users_online = server_socket.recv(buffer_size).decode()
    print(users_online)

def connect(server_socket, name, buffer_size = 1024):
    server_socket.send('connect'.encode())
    server_socket.send(name.encode())
    info = server_socket.recv(buffer_size).decode().split(',')
    port = int(info[1])
    id = info[0]
    return {id: id, port: port}