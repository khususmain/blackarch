import requests
import concurrent.futures
import sys

def fuzz(url):
    # Wordlist of high-value API endpoints
    payloads = [
        "api/v1/users", "api/admin", "api/debug", "api/test", 
        "actuator/health", "actuator/env", "actuator/heapdump", # Spring Boot
        ".env", "config.json", "web.config", "server-status", # Config files
        "graphql", "graphiql", "console", "dashboard", # Interfaces
        "swagger-ui.html", "v2/api-docs", "api-docs", # Docs
        "user/register", "user/password_reset", # Auth
        "telescope", "_profiler", "phpinfo.php", # Debuggers
        "storage/logs/laravel.log", ".git/HEAD" # Information leaks
    ]
    
    headers = {'User-Agent': 'Astro/1.0'}
    
    print(f"[*] Fuzzing {url} with {len(payloads)} payloads...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(requests.get, f"{url}/{p}", headers=headers, timeout=3): p for p in payloads}
        for future in concurrent.futures.as_completed(futures):
            p = futures[future]
            try:
                r = future.result()
                # Filter for interesting status codes (200, 401, 500) - 403/404 are noise
                if r.status_code in [200, 401, 500]:
                    print(f"[+] FOUND: {url}/{p} [{r.status_code}] (Size: {len(r.content)})")
            except Exception:
                pass

if __name__ == "__main__":
    targets = [
        "https://redhat.com",
        "https://www.redhat.com",
        "https://my.redhat.com",
        "https://tdwpreweb.redhat.com"
    ]
    for t in targets:
        fuzz(t)
