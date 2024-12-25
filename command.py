import os
import socket
import platform
from pystyle import Colors, Colorate, Center

def banner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    x = '''
    kill chain banner here
    '''
    print(Colorate.Vertical(Colors.red_to_black, Center.XCenter(x), 1))

def connect_as_commander(host, port, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(username.encode('utf-8'))  # Send username as "commander"
    banner()
    
    while True:
        command = input("admin@KCNET;~ $ ")
        
        if command.lower() == "exit":
            break
        
        # Conditional command handling
        if command.lower() == "help":
            # Send the "help" command to the server
            client.send(command.encode('utf-8'))
            
        elif command.lower() == "list":
            # Send the "list" command to the server
            client.send(command.encode('utf-8'))

        elif command.lower().startswith("attack"):
            # Send the "attack" command to the server
            client.send(command.encode('utf-8'))
        else:
            # Invalid command
            print("Invalid command. Please try again.")
            continue
        
        # Receive and display the server's response
        response = client.recv(1024).decode('utf-8')
        print(response)
    
    client.close()

if __name__ == "__main__":
    connect_as_commander("127.0.0.1", 65432, "commander")
