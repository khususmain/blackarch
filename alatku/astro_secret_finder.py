import requests
import re
import sys

def find_secrets(url):
    print(f"[*] Scanning {url} for secrets...")
    try:
        r = requests.get(url, timeout=10)
        patterns = {
            'API Key': r'AIza[0-9A-Za-z-_]{35}',
            'Firebase URL': r'https://[a-z0-9.-]+\.firebaseio\.com',
            'Google Client ID': r'[0-9]+-[a-z0-9]+\.apps\.googleusercontent\.com',
            'Access Token': r'access_token\":\"[^\"]+\"',
            'AWS Key': r'AKIA[0-9A-Z]{16}'
        }
        for name, pattern in patterns.items():
            matches = re.findall(pattern, r.text)
            if matches:
                for match in matches:
                    print(f"[!] FOUND {name}: {match}")
        
        # Generic sensitive patterns
        generic = re.findall(r"(?i)(secret|password|auth|key|token)[\s:=]+[\"']([a-zA-Z0-9_\-\.]{12,})[\"']", r.text)
        for m in generic:
            print(f"[!] Potential Secret ({m[0]}): {m[1]}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        find_secrets(sys.argv[1])
