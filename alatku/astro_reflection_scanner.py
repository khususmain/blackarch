import requests
import urllib.parse
import sys

# TARGET CONFIGURATION
TARGET = "https://tv8.lk21official.cc/search"
PARAMS = ["s", "q", "id", "query", "p", "page", "cat", "genre", "year", "country", "sort", "order", "type"]
PAYLOAD = "ASTRO_\"<>" # Specifically testing for \" < >

def scan_reflections():
    print(f"[*] Scanning {TARGET} for Unescaped Reflections...")
    print(f"[*] Payload: {PAYLOAD}")
    
    headers = {
        'User-Agent': 'Googlebot/2.1'
    }

    for param in PARAMS:
        try:
            # Construct URL with payload
            test_url = f"{TARGET}?{param}={urllib.parse.quote(PAYLOAD)}"
            response = requests.get(test_url, headers=headers, timeout=5, verify=False)
            
            if PAYLOAD in response.text:
                print(f"[+] !!! UNESCAPED REFLECTION FOUND !!!")
                print(f"    Parameter: {param}")
                print(f"    URL: {test_url}")
            elif "ASTRO_" in response.text:
                # Find the reflected portion to see what was escaped
                start_idx = response.text.find("ASTRO_")
                reflection = response.text[start_idx:start_idx+20]
                print(f"[-] Reflected (Escaped): {param} -> {reflection}...")
            else:
                pass # No reflection
                
        except Exception as e:
            print(f"[-] Error testing {param}: {e}")

if __name__ == "__main__":
    scan_reflections()
