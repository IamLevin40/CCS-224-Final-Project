import http.server
import socketserver
import threading
import os

PORT = 8000
SERVE_DIR = os.path.abspath("temp_html")

def start_server():
    os.makedirs(SERVE_DIR, exist_ok=True)
    os.chdir(SERVE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def run_server_in_background():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
