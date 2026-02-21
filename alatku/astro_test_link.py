import socket
import json

def connect_to_arch():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Menghubungkan ke port 1337 di Codespace yang sudah di-tunnel ke Arch Linux
        s.connect(("localhost", 1337))
        
        # Kirim Secret Key
        s.send(b"teemo")
        auth_res = s.recv(1024).decode()
        print(f"Auth Status: {auth_res}")
        
        if "ESTABLISHED" in auth_res:
            # Minta Telemetri
            s.send(b"telemetry")
            data = s.recv(4096).decode()
            print("
[ASTRO-LINK TELEMETRY DATA]")
            print(json.dumps(json.loads(data), indent=4))
        
        s.close()
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    connect_to_arch()
