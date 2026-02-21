import requests
import urllib3
import json
import random
import string

# Disable SSL warnings for self-signed/proxy certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_IP = "46.183.184.147"
TARGET_PORT = 4443
SNI_HOST = "dinosaur.getfoxyproxy.org" # The cover domain

def generate_random_id(length=16):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def probe_c2():
    url = f"https://{TARGET_IP}:{TARGET_PORT}/api/v1/ping"
    
    # Header sets to mimic different infection stages
    
    # 1. Android Infection (WhatsApp Context)
    headers_android = {
        'Host': SNI_HOST,
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14; SM-S918B Build/UP1A.231005.007)',
        'X-Machine-ID': generate_random_id(32),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    # 2. iOS Infection (Background Process)
    headers_ios = {
        'Host': SNI_HOST,
        'User-Agent': 'CFNetwork/1490.0.4 Darwin/23.2.0',
        'X-Client-Uuid': str(random.getrandbits(128)),
        'X-Priority': 'high',
        'Accept-Language': 'en-us',
        'Connection': 'keep-alive'
    }

    # 3. Direct API Probe (Graphite Dashboard Mimic)
    headers_dashboard = {
        'Host': SNI_HOST,
        'User-Agent': 'Graphite-Console/2.4.1',
        'Authorization': 'Bearer null',
        'X-Requested-With': 'XMLHttpRequest'
    }

    scenarios = [
        ("Android Implant", headers_android, {"status": "idle", "battery": 82}),
        ("iOS Implant", headers_ios, {"h": "heartbeat", "v": "2.0"}),
        ("Dashboard Login", headers_dashboard, None)
    ]

    print(f"[*] INITIATING ASTRO-MIMIC PROTOCOL ON {TARGET_IP}:{TARGET_PORT}...")
    print(f"[*] Using SNI/Host: {SNI_HOST}")

    for name, headers, payload in scenarios:
        print(f"\n[>] Attempting Scenario: {name}")
        try:
            # We need to manually force the Host header because requests usually overwrites it with the URL IP
            # But creating a custom session adapter is complex for a quick script. 
            # Instead, we rely on the fact that requests sends what we tell it if verified correctly.
            # However, for SNI to work, we might need a custom adapter if the server is strict. 
            # Let's try standard request first with verify=False.
            
            response = requests.post(
                url, 
                headers=headers, 
                json=payload if payload else {}, 
                verify=False, 
                timeout=10
            )
            
            print(f"   [+] Status Code: {response.status_code}")
            print(f"   [+] Server Header: {response.headers.get('Server', 'Hidden')}")
            print(f"   [+] Content-Length: {response.headers.get('Content-Length', '0')}")
            
            if response.status_code != 400:
                print(f"   [!] INTERESTING RESPONSE! Response Body (First 100 chars):")
                print(f"       {response.text[:100]}")
            else:
                print("   [-] Blocked by Squid/WAF (400 Bad Request)")

        except Exception as e:
            print(f"   [-] Error: {e}")

if __name__ == "__main__":
    probe_c2()
