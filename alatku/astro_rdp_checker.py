import socket
import subprocess
import re
import concurrent.futures
import sys

def check_port(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, int(port)), timeout=timeout):
            return True
    except:
        return False

def validate_rdp(entry):
    entry = entry.strip()
    if not entry: return None
    
    # Updated regex to handle one or more backslashes or forward slashes
    # IP:Port@Domain\User;Pass
    match = re.match(r"([^:]+):([^@]+)@(?:([^\\]+)[\\/]+)?([^;]+);(.*)", entry)
    if not match:
        return f"[-] Invalid Format: {entry}"
    
    ip, port, domain, user, password = match.groups()
    if not domain: domain = ""
    
    if not check_port(ip, port):
        return f"[-] {ip}:{port} - Port Closed"
    
    cmd = [
        "xfreerdp",
        f"/v:{ip}:{port}",
        f"/u:{user}",
        f"/p:{password}",
        "/cert:ignore",
        "+auth-only"
    ]
    if domain:
        cmd.append(f"/d:{domain}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return f"[+] {ip}:{port} - VALID - {domain}\\{user}:{password}"
        else:
            if "Authentication only, exit status 0" in result.stdout or "Authentication only, exit status 0" in result.stderr:
                 return f"[+] {ip}:{port} - VALID - {domain}\\{user}:{password}"
            return f"[-] {ip}:{port} - Auth Failed - {domain}\\{user}:{password}"
    except subprocess.TimeoutExpired:
        return f"[-] {ip}:{port} - Timeout during Auth"
    except Exception as e:
        return f"[-] {ip}:{port} - Error: {str(e)}"

def main():
    try:
        with open("rdp_103_list.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] rdp_103_list.txt not found")
        return
    
    print(f"[*] Starting validation of {len(lines)} RDP entries...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(validate_rdp, lines))
    
    for res in results:
        if res:
            print(res)

if __name__ == "__main__":
    main()
