import os
import platform
import socket
import subprocess
import json
import time
import threading

# CONFIGURATION
BRIDGE_PORT = 1337
SECRET_KEY = "teemo" # Simple validation

def get_system_telemetry():
    try:
        data = {
            "status": "ONLINE",
            "os": platform.system(),
            "distro": platform.linux_distribution() if hasattr(platform, 'linux_distribution') else "Arch Linux",
            "kernel": platform.release(),
            "hostname": socket.gethostname(),
            "cpu_load": os.getloadavg(),
            "uptime": subprocess.check_output("uptime -p", shell=True).decode().strip(),
            "battery": "N/A"
        }
        # Try to get battery info if laptop
        if os.path.exists("/sys/class/power_supply/BAT0"):
            cap = open("/sys/class/power_supply/BAT0/capacity").read().strip()
            stat = open("/sys/class/power_supply/BAT0/status").read().strip()
            data["battery"] = f"{cap}% ({stat})"
        return data
    except Exception as e:
        return {"error": str(e)}

def handle_client(client_socket):
    try:
        # Simple Auth
        auth = client_socket.recv(1024).decode().strip()
        if auth != SECRET_KEY:
            client_socket.send(b"ACCESS DENIED")
            client_socket.close()
            return

        client_socket.send(b"ASTRO-BRIDGE-ESTABLISHED")
        
        while True:
            command = client_socket.recv(4096).decode().strip()
            if not command: break
            
            if command == "telemetry":
                response = json.dumps(get_system_telemetry())
            elif command.startswith("exec "):
                cmd = command[5:]
                try:
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                    response = output.decode()
                except subprocess.CalledProcessError as e:
                    response = e.output.decode()
            elif command == "exit":
                break
            else:
                response = "UNKNOWN_COMMAND"
            
            client_socket.send(response.encode() if response else b"CMD_EXECUTED_NO_OUTPUT")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_bridge():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", BRIDGE_PORT))
    server.listen(5)
    print(f"[*] ASTRO-Bridge Active on port {BRIDGE_PORT}")
    print("[*] Waiting for ASTRO connection...")
    
    while True:
        client, addr = server.accept()
        print(f"[+] Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_bridge()
