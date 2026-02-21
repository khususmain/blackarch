import os
import time
import hashlib
import socket
import psutil
import threading
from datetime import datetime

# [TIER 5 CONFIGURATION]
WATCH_DIRS = ["/workspaces/blackarch", "/etc/passwd", "/etc/shadow"]
WHITELIST_PORTS = [22, 2222, 80, 443, 8000, 8080, 53, 5353, 3000, 5000] 
WHITELIST_PROCS = ["code", "node", "python3", "sshd", "bash", "zsh", "sh", "dockerd"]
LOG_FILE = "/tmp/astro_sentinel.log"
CANARY_FILES = ["/workspaces/blackarch/secret_passwords.txt", "/tmp/.azure_keys"]
KILL_MODE = True # GOD MODE ACTIVE

class AstroSentinel:
    def __init__(self):
        self.file_hashes = {}
        self.running = True
        self.deploy_canaries()
        self.log_event("[*] ASTRO OBLIVION (Tier 5) Initialized. GOD MODE DEFENSE ACTIVE.")

    def deploy_canaries(self):
        # Create honeytokens/traps
        trap_content = "AZURE_CLIENT_ID=0000-0000-0000-0000\nAZURE_SECRET=fake_key_do_not_touch"
        for canary in CANARY_FILES:
            if not os.path.exists(canary):
                with open(canary, "w") as f:
                    f.write(trap_content)
                self.log_event(f"[+] CANARY DEPLOYED: {canary}")

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        print(f"\033[91m{formatted_msg}\033[0m") # Red for Alert
        with open(LOG_FILE, "a") as f:
            f.write(formatted_msg + "\n")
        
        # Anti-Forensics: Wipe log if too big to prevent analysis
        if os.path.getsize(LOG_FILE) > 1024 * 1024: # 1MB
            open(LOG_FILE, 'w').close()

    def get_file_hash(self, filepath):
        try:
            if not os.path.exists(filepath):
                return None
            if os.path.isdir(filepath):
                return "DIR"
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except Exception:
            return None

    def scan_integrity(self):
        # Initial Scan
        for path in WATCH_DIRS + CANARY_FILES:
            if os.path.isfile(path):
                self.file_hashes[path] = self.get_file_hash(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        self.file_hashes[full_path] = self.get_file_hash(full_path)

        while self.running:
            try:
                # Check Canary Traps First (High Priority)
                for canary in CANARY_FILES:
                    if os.path.exists(canary):
                        current_hash = self.get_file_hash(canary)
                        if canary in self.file_hashes and self.file_hashes[canary] != current_hash:
                            self.log_event(f"[!!!] TRAP TRIGGERED: {canary} was touched! INTRUDER DETECTED.")
                            self.file_hashes[canary] = current_hash
                            # In real TIER 5, we would lock the filesystem here.
                
                # Standard Integrity Check
                current_files = set()
                for path in WATCH_DIRS:
                    if os.path.isfile(path):
                        current_files.add(path)
                        new_hash = self.get_file_hash(path)
                        if path in self.file_hashes and self.file_hashes[path] != new_hash:
                            self.log_event(f"[!] FILE MODIFIED: {path}")
                            self.file_hashes[path] = new_hash
                    elif os.path.isdir(path):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                full_path = os.path.join(root, file)
                                current_files.add(full_path)
                                new_hash = self.get_file_hash(full_path)
                                
                                if full_path not in self.file_hashes:
                                    self.log_event(f"[+] NEW FILE: {full_path}")
                                    self.file_hashes[full_path] = new_hash
                                elif self.file_hashes[full_path] != new_hash:
                                    self.log_event(f"[!] FILE MODIFIED: {full_path}")
                                    self.file_hashes[full_path] = new_hash
                
                # Check for deletions
                deleted = set(self.file_hashes.keys()) - current_files
                for f in deleted:
                    self.log_event(f"[!] FILE DELETED: {f}")
                    del self.file_hashes[f]

            except Exception as e:
                pass
            time.sleep(5) # Faster sampling for Tier 5

    def scan_network(self):
        while self.running:
            try:
                for conn in psutil.net_connections(kind='inet'):
                    if conn.status == 'ESTABLISHED' or conn.status == 'LISTEN':
                        laddr = conn.laddr
                        raddr = conn.raddr
                        
                        # Check Port Whitelist
                        if laddr.port not in WHITELIST_PORTS and (raddr and raddr.port not in WHITELIST_PORTS):
                            proc_name = "Unknown"
                            try:
                                proc = psutil.Process(conn.pid)
                                proc_name = proc.name()
                            except:
                                continue # Process already gone
                            
                            # Check Process Whitelist
                            is_safe = False
                            for safe_proc in WHITELIST_PROCS:
                                if safe_proc in proc_name:
                                    is_safe = True
                                    break
                            
                            if not is_safe:
                                msg = f"[!] UNAUTHORIZED PROCESS: {proc_name} ({conn.pid}) on Port {laddr.port}"
                                self.log_event(msg)
                                
                                if KILL_MODE:
                                    try:
                                        os.kill(conn.pid, 9)
                                        self.log_event(f"[💀] TIER 5 ACTION: KILLED process {proc_name} ({conn.pid})")
                                    except Exception as e:
                                        self.log_event(f"[-] FAILED TO KILL: {e}")

            except Exception:
                pass
            time.sleep(2) # Aggressive scanning

    def start(self):
        t1 = threading.Thread(target=self.scan_integrity)
        t2 = threading.Thread(target=self.scan_network)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False

if __name__ == "__main__":
    sentinel = AstroSentinel()
    sentinel.start()
