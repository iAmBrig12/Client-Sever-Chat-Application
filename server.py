import socket
import select

# server constants
HOST = '0.0.0.0'	# open ip for testing
PORT = 12345		# arbitrary non-privelaged port

# manage connected clients and their usernames 
clients = {} 		# client_socket -> username


# start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")
    sockets_list = [server_socket]

    while True:
        # use select to handle multiple sockets
        read_sockets, _, _ = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            # new connection
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")

                # request and store username
                username = client_socket.recv(64).decode().strip()

                if username in clients.values():
                    client_socket.send("ERR 0: username taken".encode())
                    client_socket.close()
                elif len(username) > 32:
                    client_socket.send("ERR 1: username too long".encode())
                    client_socket.close()
                elif ' ' in username:
                    client_socket.send("ERR 2: username contains spaces".encode())
                    client_socket.close()
                else:
                    sockets_list.append(client_socket)
                    clients[client_socket] = username
                    print(f"Username {username} registered")

                    # ack registration
                    client_socket.send(f"\nACK Welcome {username}!\n{len(clients)} user(s) currently in chat: {list(clients.values())}\n\nEnter any message to broadcast to the entire chat\nEnter @username your_message to send a private message to username\nEnter EXIT to exit chat\n""".encode())

                    # broadcast new user
                    broadcast(f"SERVER: {username} has joined the chat!\n{len(clients)} user(s) currently in chat: {list(clients.values())}", client_socket)

            # existing connection with message
            else:
                try:
                    message = notified_socket.recv(1024).decode().strip()

                    if message:                             # handle the message
                        username = clients[notified_socket]
                        print(f"Message from {username}: {message}")

                        if message.startswith("PMSG"):      # private message
                            _, target_user, private_message = message.split(maxsplit=2)
                            send_private_message(notified_socket, target_user, private_message)
                    
                        elif message.startswith("MESG"):    # broadcast message
                            broadcast(f"{username}: {message[5:].strip()}", notified_socket)
                    
                        elif message.startswith("EXIT"):    # client disconnect
                            disconnect_client(notified_socket)
                            sockets_list.remove(notified_socket)

                    else:                                   # client disconnected without messaging
                        disconnect_client(notified_socket)
                        sockets_list.remove(notified_socket)

                except Exception as e:
                    print(f"Error: {e}")
                    if notified_socket in clients:
                        disconnect_client(notified_socket)


# function to broadcast a message to all clients except the sender
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_socket]


# function to send a private message to a specified user
def send_private_message(sender_socket, target_user, message):
    send_username = clients[sender_socket]
    for client_socket, username in clients.items():
        if username == target_user:
            try:
                client_socket.send(f"{send_username} (private): {message}".encode())
                return
            except:
                client_socket.close()
                del clients[client_socket]
        
    sender_socket.send("ERR 3: Unkown user".encode())


# function to disconnect a client
def disconnect_client(client_socket):
    username = clients[client_socket]
    print(f"User {username} disconnected")
    broadcast(f"SERVER: {username} has left the chat!")
    client_socket.close()
    del clients[client_socket]
    broadcast(f"{len(clients)} user(s) currently in chat: {list(clients.values())}")


if __name__ == "__main__":
    start_server()

