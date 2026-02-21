import socket
import ssl
import sys

def emulate_handshake(target_ip, target_port, sni_host):
    print(f"[*] Emulating Handshake to {target_ip}:{target_port} with SNI: {sni_host}")
    
    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    try:
        sock.connect((target_ip, target_port))
        
        # Wrap the socket with SSL
        context = ssl.create_default_context()
        # Disable certificate verification for probing
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Attempt the handshake
        ssl_sock = context.wrap_socket(sock, server_hostname=sni_host)
        
        print(f"[+] SUCCESS! Handshake established with {sni_host}")
        print(f"[+] Protocol: {ssl_sock.version()}")
        print(f"[+] Cipher: {ssl_sock.cipher()}")
        cert = ssl_sock.getpeercert(binary_form=True)
        if cert:
            print("[+] Peer Certificate obtained.")
        
        ssl_sock.close()
        return True
    except ssl.SSLError as e:
        print(f"[-] SSL Error with {sni_host}: {e}")
    except Exception as e:
        print(f"[-] Connection Error with {sni_host}: {e}")
    finally:
        sock.close()
    return False

if __name__ == "__main__":
    ip = "46.183.184.43"
    port = 4443
    
    # Test common patterns or leaked info
    test_snis = [
        "graphite.paragon.io",
        "portal.paragon-solutions.io",
        "valentina.cz",
        "dinosaur.getfoxyproxy.org", # Neighbor pattern
        "mammoth.getfoxyproxy.org",
        "api.graphite-system.net",
        "c2.pretzellogix.com" # Fake name based on BIGPRETZEL
    ]
    
    for sni in test_snis:
        emulate_handshake(ip, port, sni)
