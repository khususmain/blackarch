import socket
import subprocess
import re
import concurrent.futures
import sys
import os

def check_port(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, int(port)), timeout=timeout):
            return True
    except:
        return False

def validate_rdp(entry):
    entry = entry.strip()
    if not entry: return None
    
    match = re.match(r"([^:]+):([^@]+)@(?:([^\\]+)[\\/]+)?([^;]+);(.*)", entry)
    if not match:
        return f"[-] Invalid Format: {entry}"
    
    ip, port, domain, user, password = match.groups()
    if not domain: domain = ""
    
    if not check_port(ip, port):
        return f"[-] {ip}:{port} - Port Closed"
    
    target_user = f"{domain}\\\\{user}" if domain else user
    
    cmd = [
        "hydra",
        "-l", user,
        "-p", password,
        ip,
        "rdp",
        "-s", port,
        "-t", "1",
        "-W", "1"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        if "1 valid password found" in result.stdout:
            return f"[+] {ip}:{port} - VALID - {target_user}:{password}"
        else:
            return f"[-] {ip}:{port} - Auth Failed - {target_user}:{password}"
    except subprocess.TimeoutExpired:
        return f"[-] {ip}:{port} - Timeout"
    except Exception as e:
        return f"[-] {ip}:{port} - Error: {str(e)}"

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "rdp_batch_5.txt"

    if not os.path.exists(input_file):
        print(f"[-] {input_file} not found")
        return
        
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Starting deep validation of {len(lines)} RDP entries...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(validate_rdp, lines))
    
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    valid_count = 0
    for res in results:
        if res and "[+]" in res:
            print(res)
            valid_count += 1
    print("="*50)
    print(f"[*] Scan Complete. Found {valid_count} valid RDP.")

if __name__ == "__main__":
    main()
