import requests
import concurrent.futures

def probe(id):
    url = f"https://gitlab.com/api/v4/projects/{id}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"[!] SUCCESS: Project {id} is PUBLIC and ACCESSIBLE via API.")
        elif r.status_code == 403:
            print(f"[*] Project {id}: Forbidden (Private)")
    except:
        pass

if __name__ == '__main__':
    print("[*] Starting GitLab API IDOR Probe...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(probe, range(1000, 2000))
