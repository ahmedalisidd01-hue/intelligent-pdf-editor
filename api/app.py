from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Streamlit app would run here. For full functionality, use Streamlit Cloud instead.')
