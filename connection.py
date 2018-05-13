def parse_address(addr):
    return addr[0] + ',' + str(addr[1])

def parse_clients(clients):
    people_connected_string = "People connected to ZapZiplerson:\n\n"
    i = 0
    for client in clients:
        people_connected_string += str(i) + ' ' + client[0] + '\n'
        i+=1
    return people_connected_string    

def already_connected_checker(c1, c2, connection):
    if c1 in connection or c2 in connection: 
        return True
    else:
        return False

def remove_client_connections(id, conn):
    if id in conn:
        return False
    else:
        return True


def listen_client(clients, connections, buffer_size, conn, addr):
    request = conn.recv(buffer_size).decode()
    print(str(conn.getpeername()) + " requesting " + request)
    if(request == 'connect'): 
        client_username = conn.recv(buffer_size).decode()
        info = (str(client_username), conn, addr)
        clients.append(info)
        client_id = len(clients)-1
        conn.send((str(client_id) + ',' + str(info[2][1])).encode())
        
        people_connected_string = parse_clients(clients)
        conn.send(people_connected_string.encode())
        want_to_connect = conn.recv(buffer_size).decode()

        if want_to_connect != 'wait':
            try:
                verification = list(filter(lambda cnn: already_connected_checker(client_id, want_to_connect, cnn), connections))
                if len(verification) == 0:
                    conn.send((parse_address(clients[int(want_to_connect)][2])).encode())
                    connections.append([client_id, want_to_connect])
                else: 
                    raise ValueError('User already connected to someone else!')
            except ValueError as err:
                conn.send(b'\x11' + str(err).encode())
            except Exception as err:
                print(err)
                conn.send(b'\x12' + "Invalid user id, please restart your connection".encode())
        
        print("Closed connection with server")
        conn.close()
    elif(request == 'disconnect'):
        client_id = int(conn.recv(buffer_size).decode())
        clients.pop(client_id)
        connections = list(filter(lambda cnn: remove_client_connections(client_id, cnn), connections))
        conn.close()
    elif(request == 'users'): 
        conn.send(parse_clients(clients).encode())
    