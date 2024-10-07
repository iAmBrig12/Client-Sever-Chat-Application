import socket
import select
import sys

# client constants
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    # start client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # get username and send to server
    username = input("\nUsername must be 1-32 characters and cannot include spaces\nEnter your username:\n")
    client_socket.send(username.encode())

    # loop that manages tcp connection until connections is closed
    while True:
        sockets_list = [sys.stdin, client_socket]

        # use select to wait for input either from user or from server
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            
            if notified_socket == client_socket:            # message from the server
                message = client_socket.recv(1024).decode()
                if not message:
                    print("Connection closed by the server.")
                    sys.exit()
                else:
                    print(message)
            
            else:                                           # user input
                message = sys.stdin.readline().strip()
                if message.lower() == "exit":               # exit chat
                    client_socket.send(f"EXIT {username}".encode())
                    client_socket.close()
                    sys.exit()
                elif message.startswith("@"):               # private message
                    if len(message.split()) < 2:            # incorrect message syntax
                        print("private message syntax: @username message")
                    else:                                   # send PMSG
                        target_user, private_message = message[1:].split(maxsplit=1)
                        client_socket.send(f"PMSG {target_user} {private_message}".encode())
                else:                                       # broadcast message
                    client_socket.send(f"MESG {message}".encode())

if __name__ == "__main__":
    start_client()
