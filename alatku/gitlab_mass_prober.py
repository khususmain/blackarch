import requests
import concurrent.futures
import random
import sys

# Konfigurasi Target
START_ID = 20000
END_ID = 21000  # Scan 1000 proyek dalam satu batch cepat
THREADS = 50

# Rotasi User Agent untuk Evasion
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def scan_project(id):
    url = f"https://gitlab.com/api/v4/projects/{id}"
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        # Menggunakan session untuk performa (bisa dioptimalkan lebih lanjut dengan global session)
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            data = r.json()
            name = data.get('name_with_namespace', 'Unknown')
            web_url = data.get('web_url', 'Unknown')
            return f"[+] PUBLIC: ID {id} | {name} | {web_url}"
        elif r.status_code == 403:
            return f"[*] PRIVATE: ID {id} (Exist but Locked)"
    except:
        pass
    return None

def main():
    print(f"[*] Starting Mass Scan: IDs {START_ID} to {END_ID} with {THREADS} threads...")
    found_public = 0
    found_private = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(scan_project, i): i for i in range(START_ID, END_ID)}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(result)
                if "PUBLIC" in result:
                    found_public += 1
                elif "PRIVATE" in result:
                    found_private += 1

    print("-" * 40)
    print(f"[MISSION COMPLETE] Scan Finished.")
    print(f"[+] Total Public Projects Found: {found_public}")
    print(f"[*] Total Private Projects Detected: {found_private}")

if __name__ == "__main__":
    main()
