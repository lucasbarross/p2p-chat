def parse_address(addr):
    return addr[0] + ',' + str(addr[1])

def parse_clients(clients):
    people_connected_string = "People connected to ZapZiplerson:\n\n"
    i = 0
    for client_id, info in clients.items():
        people_connected_string += str(i) + ' ' + info[1] + '\n'
        i+=1
    return people_connected_string    

def already_connected_checker(c1, connection):
    if c1 in connection: 
        return True
    else:
        return False

def remove_client_connections(id, conn):
    if id in conn:
        return False 
    else:
        return True

def remove_client(id, client): 
    if(client[0] == id):
        return False
    else:
        return True

def listen_client(clients, buffer_size, conn, addr, socket):
        while 1:
            request = conn.recv(buffer_size).decode()

            if request == 'connect': 
                client_username = conn.recv(buffer_size).decode()
                client_id = len(clients)+1
                conn.send((str(client_id)).encode())
                port = conn.recv(buffer_size).decode()
                info = (client_id, str(client_username), conn, (addr[0], port))
                clients[client_id] = info
                print(str(info[1]) + ' connected')
                while 1:
                    try: 
                        socket.timeout(3)
                        confirmation = conn.recv(buffer_size).decode()
                    except:
                        if client_id in clients:
                            del clients[client_id]
                        break
                break

            elif request == 'connect_to':
                try:
                    listener = int(conn.recv(buffer_size).decode())
                    keys_list = list(clients.keys())
                    if listener < len(keys_list) and listener >= 0:
                        listener = clients[keys_list[listener]]
                        conn.send((parse_address(listener[3])).encode())
                        del clients[listener[0]]
                        break
                    else: 
                        raise ValueError()
                except ValueError as err:
                    conn.send(b'\x11' + 'This user is not available!'.encode())
                except Exception as err:
                    conn.send(b'\x12' + "Invalid user id".encode())
            elif request == 'users': 
                conn.send(parse_clients(clients).encode())  
        