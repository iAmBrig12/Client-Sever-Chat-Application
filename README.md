# Chat Application using Socket Programming
This project implements a chat application that enables users to exchange messages through a central chat server. The server manages a list of currently online users and facilitates the transmission of messages between clients.

## Features
- **User Registration**: Upon starting the client, users are prompted to enter a username (1-32 characters, no spaces). The client then establishes a TCP connection to the server and sends a registration message with the username.
  
- **Server Validation**: The server checks the username for validity. If the username is acceptable, the server acknowledges the registration. Otherwise, it sends an error message (e.g., if the username is already taken or in an incorrect format).

- **Broadcast Notifications**: Once registered, the server broadcasts a message to all clients when a new user joins the chatroom.

- **Messaging**: Users can send both broadcast messages and private messages to others in the chatroom. They can also receive messages from other users.

- **User Exit Notifications**: When a user leaves the chat, the server broadcasts a notification to inform other clients that the user has departed.

## Running the Server
1. Open a terminal window.
2. Navigate to the directory where `server.py` is located.
3. Start the server by running the following command:
   ```bash
   python3 server.py
## Running the Client
1. Open a terminal window.
2. Navigate to the directory where `client.py` is located.
3. Start the client by running the following command: (note the server hostname will be the hostname of the machine that server.py is running on)
   ```bash
   python3 client.py <server_hostname>
4. When prompted, enter a username (1-32 characters, no spaces).
5. Once registered, you can start sending messages to the chatroom.

### Sending Messages:
- **Broadcast Message**: Type your message and hit Enter to send it to all users in the chatroom.
- **Private Message**: Use ```@username your_message``` to send a private message to a specific user.