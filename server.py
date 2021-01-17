import http.server
import socketserver
import imgcompare
from PIL import Image
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen
import json
from io import BytesIO
import validators

class ImageComparisonHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        token = parse_qs(parsed.query)['token'][0] if 'token' in parse_qs(parsed.query) else None
        # no token provided
        if token == None:
            response = {
                'success': False,
                'error': 'Authetication failed.'
            }
            self._set_headers(401)
            self.wfile.write(self._html(response))
        # valid token
        elif token == TOKEN:
            if self.path.startswith('/image-comparison', 0, 17):
                api = ImageComparisonAPI()
                img_a_path = parse_qs(parsed.query)['img_a'][0]
                img_b_path = parse_qs(parsed.query)['img_b'][0]
                percent = api.get_percent(img_a_path, img_b_path)
                response = {
                    'success': True,
                    'percent': str(percent) + '%'
                }
                self._set_headers(200)
                self.wfile.write(self._html(response))       
        # invalid token
        else:
            response = {
                'success': False,
                'error': 'Invalid credentials'
            }
            self._set_headers(403)
            self.wfile.write(self._html(response)) 
        return
    
    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes message
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")

class ImageComparisonAPI:
    def get_percent(self, img_a_path, img_b_path):
        # passing as url or local file
        img_a = Image.open(urlopen(img_a_path)) if validators.url(img_a_path) else Image.open(img_a_path)
        img_b = Image.open(urlopen(img_b_path)) if validators.url(img_b_path) else Image.open(img_b_path)
        # different file type handler
        if img_a.mode != img_b.mode:
            img_a = img_a if img_a.mode == 'RGB' else img_a.convert('RGB')
            img_b = img_b if img_b.mode == 'RGB' else img_b.convert('RGB')
        # different size handler
        if img_a.size != img_b.size:
            img_a = img_a.resize((img_b.width, img_b.height))
        return 100.0 - imgcompare.image_diff_percent(img_a, img_b)

PORT = 5000
handler = ImageComparisonHandler
TOKEN = 'kmrhn74zgzcq4nqb'
my_server = socketserver.TCPServer(("", PORT), handler)
my_server.serve_forever()