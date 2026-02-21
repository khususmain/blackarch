import subprocess
import time
import os
import sys
import re

def run_command(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def start_astro_link():
    print("🚀 [ASTRO-LINK] Initializing Connection...")
    
    # 1. Pastikan Bridge Server berjalan
    print("[*] Starting Bridge Server on port 8888...")
    # Mengasumsikan astro_bridge_server.py ada di direktori yang sama
    bridge = subprocess.Popen([sys.executable, "astro_bridge_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    # 2. Jalankan Cloudflare Tunnel
    print("[*] Requesting Cloudflare Tunnel...")
    cf = run_command("cloudflared tunnel --url tcp://127.0.0.1:8888")
    
    url_found = False
    try:
        while True:
            line = cf.stdout.readline()
            if not line:
                break
            
            # Cari URL di output cloudflared
            match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
            if match:
                url = match.group(0)
                print("
" + "="*50)
                print(f"✅ ASTRO-LINK IS ACTIVE!")
                print(f"🔗 URL: {url}")
                print("="*50)
                print("
[*] Keep this terminal open to maintain connection.")
                url_found = True
                
            if url_found and "Starting metrics server" in line:
                # Tunnel sudah stabil
                break
    except KeyboardInterrupt:
        print("
[!] Stopping Astro-Link...")
        bridge.terminate()
        cf.terminate()

if __name__ == "__main__":
    # Cek apakah cloudflared terinstall
    if subprocess.run("command -v cloudflared", shell=True, capture_output=True).returncode != 0:
        print("❌ Error: cloudflared tidak ditemukan. Install dengan: sudo pacman -S cloudflared")
        sys.exit(1)
        
    start_astro_link()
