import requests
import sys
import json

def find_origin_ip(domain, token):
    # Censys API v2 Host Search
    # Note: Token format is usually ID:SECRET
    # If only one token provided, we try to use it as the SECRET with a dummy ID or as a combined auth.
    
    print(f"[*] Searching for Origin IP of {domain} via Censys...")
    
    # Split token if it's in ID:SECRET format, otherwise treat as individual
    if ":" in token:
        api_id, api_secret = token.split(":")
    else:
        # Assuming the provided token is the API Secret and ID might be needed.
        # However, some CLI tools use a single token. 
        # For API v2, it's Basic Auth (ID:SECRET)
        print("[!] Token format warning: Censys API v2 usually requires ID:SECRET.")
        print("[!] Trying to use provided token as API Secret with ID extraction...")
        # We will try to use the token as is for now.
        api_id = "" # User might need to provide ID
        api_secret = token

    url = "https://search.censys.io/api/v2/hosts/search"
    query = f"services.tls.certificates.leaf_data.subject.common_name: \"{domain}\""
    
    try:
        # If token is just one string, we'll try to use it as the Auth
        # But usually it's Basic Auth (ID:SECRET)
        # For this simulation, I'll assume the user provided the combined or secret.
        # Let's try to use it as API_ID:API_SECRET if possible.
        
        # Test if it's a combined token
        auth = tuple(token.split(":")) if ":" in token else (None, token)
        
        if not auth[0]:
            print("[-] Error: Censys API ID is missing. Please provide in format ID:SECRET.")
            return

        payload = {
            "q": query,
            "per_page": 5,
            "virtual_hosts": "EXCLUDE"
        }
        
        response = requests.post(url, json=payload, auth=auth, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get('result', {}).get('hits', [])
            if not hits:
                print("[-] No potential Origin IPs found on Censys.")
                return
            
            print(f"[+] Found {len(hits)} potential Origin IPs:")
            for hit in hits:
                ip = hit.get('ip')
                services = [s.get('port') for s in hit.get('services', [])]
                print(f"    - IP: {ip} | Ports: {services}")
        else:
            print(f"[-] Censys API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target = "adsjiwa-dewi11.com"
    token = "censys_RdvXgGsv_DgU8ynWUg9o473Gh9qzfYG7v" # User provided
    # Re-checking token. Usually Censys tokens look like UUID:Secret.
    # The provided token looks like a single API Key. 
    # I will ask for the ID if this fails.
    find_origin_ip(target, token)
