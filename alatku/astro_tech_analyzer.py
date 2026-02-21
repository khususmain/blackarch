import requests
import sys

def analyze(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"URL: {url}")
        print(f"Status: {r.status_code}")
        print(f"Server: {r.headers.get('Server')}")
        print(f"X-Powered-By: {r.headers.get('X-Powered-By')}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        
        # Tech detection
        techs = []
        if 'Drupal' in r.text or 'drupal' in r.headers.get('X-Generator', ''): techs.append('Drupal')
        if 'React' in r.text or 'react' in r.text: techs.append('React')
        if 'nginx' in r.headers.get('Server', '').lower(): techs.append('Nginx')
        if 'envoy' in r.headers.get('server', '').lower() or 'x-envoy' in str(r.headers).lower(): techs.append('Envoy Proxy')
        
        print(f"Detected Tech: {', '.join(techs)}")
        print("-" * 30)
    except Exception as e:
        print(f"Error analyzing {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        analyze(target)
    else:
        print("Usage: python3 astro_tech_analyzer.py <url>")
