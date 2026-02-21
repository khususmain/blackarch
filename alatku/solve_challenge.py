import requests
import re
import subprocess
import json
import urllib.parse
import sys

def solve(target_url, post_data=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    resp = session.get(target_url)
    body = resp.text
    
    if "One moment, please..." not in body:
        if post_data:
            if post_data.startswith("<?xml"):
                headers["Content-Type"] = "text/xml"
                resp = session.post(target_url, data=post_data, headers=headers)
            else:
                resp = session.post(target_url, data=post_data)
            return session.cookies.get_dict(), resp.text
        return session.cookies.get_dict(), body

    r_match = re.search(r"var R=\[(.*?)\];", body)
    if not r_match: return None, body
    r_str = r_match.group(1)
    
    rotate_match = re.search(r"\(function\(c,L\)\{.*?\}\(a0q,(0x[0-9a-f]+)\)\);", body, re.DOTALL)
    if not rotate_match: return None, body
    rotate_block = rotate_match.group(0)
    target_val = rotate_match.group(1)
    
    l_match = re.search(r"L=\+\(\((.*?)\)\)", body)
    k_match = re.search(r"K=\+\(\((.*?)\)\)", body)
    
    def eval_js_num(js_num):
        res = subprocess.check_output(["node", "-e", f"console.log(+({js_num}))"])
        return int(res.strip())

    L = eval_js_num(l_match.group(1))
    K = eval_js_num(k_match.group(1))
    
    node_script = f"""
    var R = [{r_str}];
    function a0q() {{ return R; }}
    function a0O(c, L) {{
        var q = a0q();
        return a0O = function(O, h) {{
            O = O - 0x123;
            var s = q[O];
            return s;
        }}, a0O(c, L);
    }}
    {rotate_block}
    function y(O) {{ return R[O - 0x123]; }}
    """
    
    a0m_match = re.search(r"var a0m=\{(.*?)\};", body)
    if a0m_match:
        node_script += f"var a0m={{{a0m_match.group(1)}}};"
        node_script += "var id_val = y(a0m.r) + y(a0m.j) + y(a0m.t) + 'c7';"
    else:
        node_script += "var id_val = y(0x146) + y(0x143) + y(0x134) + 'c7';"
        
    node_script += "console.log(id_val);"
    
    id_val = subprocess.check_output(["node", "-e", node_script]).decode().strip()
    wsidchk = L + K
    
    ts_match = re.search(r"ts',\s*'(.*?)'", body)
    if not ts_match: ts_match = re.search(r"ts',\s*\"(.*?)\"", body)
    if not ts_match: ts_match = re.search(r"k\[y\(a0m.e\)\]='(.*?)'", body)
    ts = ts_match.group(1)
    
    action_match = re.search(r"a='(.*?)'", body)
    action = action_match.group(1)
    
    p_match = re.search(r"p='(.*?)'", body)
    p_val = urllib.parse.unquote(p_match.group(1))
    
    params = {"id": id_val, "wsidchk": wsidchk, "pdata": p_val, "ts": ts}
    base_url = "/".join(target_url.split("/")[:3])
    post_url = base_url + action
    
    post_resp = session.get(post_url, params=params, allow_redirects=False)
    
    if post_resp.status_code == 302:
        redirect_url = post_resp.headers.get("Location")
        if not redirect_url.startswith("http"): redirect_url = base_url + redirect_url
        if post_data:
            if post_data.startswith("<?xml"):
                headers["Content-Type"] = "text/xml"
                final_resp = session.post(redirect_url, data=post_data, headers=headers)
            else:
                final_post_data = dict(urllib.parse.parse_qsl(post_data))
                final_resp = session.post(redirect_url, data=final_post_data)
        else:
            final_resp = session.get(redirect_url)
        return session.cookies.get_dict(), final_resp.text
    
    return None, body

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 solve_challenge.py <url> [post_data] [output_file]")
        sys.exit(1)
    
    target_url = sys.argv[1]
    post_data = sys.argv[2] if len(sys.argv) > 2 and ("=" in sys.argv[2] or "<?xml" in sys.argv[2]) else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else (sys.argv[2] if len(sys.argv) > 2 and not post_data else None)
    
    cookies, body = solve(target_url, post_data)
    if cookies:
        if output_file:
            with open(output_file, "w") as f:
                f.write(body)
            print(f"[+] Saved full body to {output_file}")
        else:
            print(f"BODY_LEN: {len(body)}")
            print(f"BODY_SAMPLE: {body[:500]}")
        
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        print(f"COOKIE: {cookie_str}")
    else:
        print("[-] Failed to bypass challenge.")
