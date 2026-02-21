import requests
import concurrent.futures
import sys

TARGET = "https://seodomains.com.hr"
WORDLIST = "short_list.txt"
EXTS = ["", ".php", ".env", ".bak", ".old", ".zip"]

def probe(path):
    url = f"{TARGET}/{path}"
    try:
        r = requests.get(url, verify=False, timeout=5, allow_redirects=False)
        if r.status_code in [200, 204, 301, 302, 403]:
            # Filter out common 403s if needed, but 403 can indicate existence
            print(f"[+] FOUND: {url} | Status: {r.status_code} | Size: {len(r.content)}")
            return f"{url} [{r.status_code}]"
    except:
        pass
    return None

def run():
    print(f"[*] Starting Deep Fuzzing on {TARGET}...")
    with open(WORDLIST, "r") as f:
        words = [line.strip() for line in f if line.strip()]
    
    paths = []
    for w in words:
        for ext in EXTS:
            paths.append(f"{w}{ext}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(probe, paths))
    
    print("[*] Fuzzing Complete.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        TARGET = sys.argv[1].rstrip("/")
        WORDLIST = sys.argv[2]
        run()
    else:
        print("Usage: python3 astro_fuzzer.py <target_url> <wordlist_path>")
