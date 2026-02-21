import requests
import sys
import concurrent.futures

class AstroRecon:
    def __init__(self, target):
        self.target = target
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def check_status(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5, allow_redirects=True)
            return url, response.status_code, response.headers.get('Server', 'Unknown')
        except Exception:
            return url, None, None

    def scan_subdomains(self, subdomains):
        print(f"[*] Starting Astro Scan on {self.target}...")
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            urls = [f"https://{sub}.{self.target}" for sub in subdomains]
            future_to_url = {executor.submit(self.check_status, url): url for url in urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url, status, server = future.result()
                if status:
                    print(f"[+] {url} - Status: {status} - Server: {server}")
                    results.append((url, status, server))
        return results

if __name__ == "__main__":
    target_domain = sys.argv[1]
    subs = ["api", "dev", "staging", "my", "tdwpreweb", "vpn", "corp", "internal", "test", "portal", "digitalpayment", "auth", "login", "admin", "db", "mail", "git", "jenkins", "gitlab", "jira", "confluence", "wiki", "monitor", "grafana", "prometheus", "k8s", "kubernetes", "beta", "old", "new", "v1", "v2", "api-dev", "api-staging", "api-test", "shop", "blog", "cdn", "static", "assets", "img", "media", "upload", "download", "files", "docs", "support", "help", "faq", "forum", "community", "dev-api", "staging-api", "test-api", "portal-dev", "portal-staging"]
    recon = AstroRecon(target_domain)
    recon.scan_subdomains(subs)
