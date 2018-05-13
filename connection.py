import json

def parseAddress(addr):
    return addr[0] + ',' + str(addr[1])

def connect_client(clients, buffer_size, conn, addr): 
    client_username = conn.recv(buffer_size).decode()
    info = (str(client_username), conn, addr)
    clients.append(info)
    conn.send(str(info[2][1]).encode())
        
    people_connected_string = "People connected to ZapZiplerson:\n\n"
    i = 0
    for client in clients:
        people_connected_string += str(i) + ' ' + client[0] + '\n'
        i+=1
        
    conn.send(people_connected_string.encode())
    want_to_connect = conn.recv(buffer_size).decode()

    if want_to_connect != 'w':
        try:
            conn.send((parseAddress(clients[int(want_to_connect)][2])).encode())
        except:
            conn.send("Invalid user id, please restart your connection".encode())
    
    print("Closed connection with server")
    conn.close()