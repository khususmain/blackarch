import requests
import concurrent.futures
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validate(url):
    headers = {"X-Forwarded-For": "10.49.8.173", "User-Agent": "Astro"}
    try:
        r = requests.get(f"https://{url}", headers=headers, timeout=3, verify=False)
        if r.status_code == 200:
            return url
    except:
        pass
    return None

if __name__ == "__main__":
    try:
        with open("audit_telkomsel/subdomains_all.txt", "r") as f:
            subs = [line.strip() for line in f.readlines()[:100]]
        
        print(f"[*] Validating {len(subs)} subdomains...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(validate, subs))
        
        live_targets = [r for r in results if r]
        with open("audit_telkomsel/live_verified.txt", "w") as f:
            for t in live_targets:
                f.write(f"https://{t}\n")
        print(f"[+] Found {len(live_targets)} live targets via bypass.")
    except Exception as e:
        print(f"[-] Error: {e}")
