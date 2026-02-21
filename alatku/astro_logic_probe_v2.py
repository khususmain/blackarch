import socket
import time

def fragmented_hello(target_ip, target_port, sni):
    print(f"[*] Attempting Fragmented Handshake to {target_ip}:{target_port} with SNI: {sni}")
    
    # Construct a basic TLS ClientHello with SNI
    # (Simplified for demonstration, normally would use a full valid structure)
    # Using a pre-built ClientHello or similar
    
    # For simplicity, we'll use the SSL module to get a ClientHello and then fragment it
    # This is tricky with high-level SSL modules. 
    # Let's use a more direct approach: send a few bytes at a time.
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((target_ip, target_port))
        
        # We'll send a very basic TLS Record Layer Header (Handshake)
        # 16 03 01 ... (TLS 1.2 Handshake)
        # But wait, we need the full ClientHello.
        
        # Let's use a trick: open a connection, and send 1 byte every 0.5s.
        # Some WAFs/Firewalls time out or fail to reassemble if it's too slow or fragmented.
        
        # We'll just try to send a few random bytes to see if the server responds at all
        # or if it waits for more.
        
        payload = b"\x16\x03\x01\x00\x05\x01\x00\x00\x01\x00" # Very partial ClientHello
        
        for byte in payload:
            sock.send(bytes([byte]))
            print(f"[>] Sent byte: {hex(byte)}")
            time.sleep(0.5)
            
        # Try to read response
        sock.settimeout(2)
        try:
            resp = sock.recv(1024)
            print(f"[+] Received response: {resp.hex()}")
        except socket.timeout:
            print("[-] No immediate response (Timeout).")
            
        sock.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    fragmented_hello("46.183.184.43", 4443, "graphite.paragon.io")
