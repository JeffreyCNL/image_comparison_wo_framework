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
        path = self.path
        print(path)
        if path.startswith('/image-comparison', 0, 17):
            api = ImageComparisonAPI()
            parsed = urlparse.urlparse(path)
            img_a_path = parse_qs(parsed.query)['img_a'][0]
            img_b_path = parse_qs(parsed.query)['img_b'][0]
            percent = api.get_percent(img_a_path, img_b_path)
            self.path = 'otherPage.html'
            # self.send_response(200)
            # self.end_headers()
            # self.wfile.write(b'percent: ' + percent)
            # self.wfile.write(b'%.2f\r\n' % percent)
            # self.wfile.write(json.dumps({
                # 'percent': b'%.2f\r\n' % percent
            # }))
            # response = {
            #     'status':'SUCCESS',
            #     'data':'hello from server'
            # }
            # self.wfile.write(json.dumps(response))
        print(percent)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

class ImageComparisonAPI:
    def get_percent(self, img_a_path, img_b_path):
        img_a = Image.open(urlopen(img_a_path)) if validators.url(img_a_path) else Image.open(img_a_path)
        img_b = Image.open(urlopen(img_b_path)) if validators.url(img_b_path) else Image.open(img_b_path)
        # different file type handler
        if img_a.mode != img_b.mode:
            img_a = img_a if img_a.mode == 'RGB' else img_a.convert('RGB')
            img_b = img_b if img_b.mode == 'RGB' else img_b.convert('RGB')
        # different size handler
        if img_a.size != img_b.size:
            img_a = img_a.resize((img_b.width, img_b.height))
        return imgcompare.image_diff_percent(img_a, img_b)


PORT = 5000
handler = ImageComparisonHandler
my_server = socketserver.TCPServer(("", PORT), handler)
my_server.serve_forever()