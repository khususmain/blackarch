import json
import re

# Database of critical vulnerabilities for common PHP packages
VULN_DB = {
    "dompdf/dompdf": {
        "range": "<2.0.4",
        "vuln": "Remote Code Execution (RCE) via CSS/Font",
        "cve": "CVE-2023-23924"
    },
    "twig/twig": {
        "range": "<2.14.11",
        "vuln": "Server-Side Template Injection (SSTI)",
        "cve": "CVE-2022-23614"
    },
    "guzzlehttp/guzzle": {
        "range": "<6.5.8",
        "vuln": "Server-Side Request Forgery (SSRF) / Header Injection",
        "cve": "CVE-2022-29248"
    },
    "phpmailer/phpmailer": {
        "range": "<6.5.0",
        "vuln": "Remote Code Execution (RCE)",
        "cve": "CVE-2021-3603"
    },
    "league/flysystem": {
        "range": "<2.0.0",
        "vuln": "Local File Inclusion (LFI)",
        "cve": "Multiple"
    },
    "smarty/smarty": {
        "range": "<3.1.43",
        "vuln": "SSTI / RCE",
        "cve": "CVE-2021-29454"
    }
}

def check_version(pkg_ver, rule_ver):
    try:
        p_parts = [int(x) for x in re.findall(r'\d+', pkg_ver)]
        r_parts = [int(x) for x in re.findall(r'\d+', rule_ver)]
        
        for i in range(min(len(p_parts), len(r_parts))):
            if p_parts[i] < r_parts[i]:
                return True
            if p_parts[i] > r_parts[i]:
                return False
        return False
    except:
        return False

def analyze():
    print("[*] Analyzing dependencies from installed.json...")
    try:
        with open("seodomains_audit/installed.json", "r") as f:
            data = json.load(f)
        
        found_vulns = []
        packages = data.get("packages", [])
        
        print(f"[*] Scanned {len(packages)} packages.")
        
        for pkg in packages:
            name = pkg.get("name")
            version = pkg.get("version")
            
            # Check against DB
            if name in VULN_DB:
                rule = VULN_DB[name]
                rule_ver_clean = re.sub(r'[<>=]', '', rule["range"])
                
                is_vuln = check_version(version, rule_ver_clean)
                
                # Check logic: if installed version is older than rule version
                if is_vuln: 
                    print(f"\n[!] HIGH RISK: {name} v{version}")
                    print(f"    - Type: {rule['vuln']}")
                    print(f"    - Ref: {rule['cve']}")
                    found_vulns.append(name)
                else:
                    print(f"[+] Safe: {name} v{version}")
            
            if "phpunit" in name:
                print(f"[!] Warning: Dev tool '{name}' present in production!")

        if not found_vulns:
            print("\n[-] No critical CVEs matched in predefined list.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    analyze()
