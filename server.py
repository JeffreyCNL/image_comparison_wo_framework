import http.server
import socketserver
import imgcompare
from PIL import Image
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json

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
            pload = {
                'percent': percent
            }
            # self.path = 'otherPage.html'
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
        img_a = Image.open(img_a_path)
        img_b = Image.open(img_b_path)
        # different file type handler
        if img_a.mode != img_b.mode:
            if img_a.mode == 'RGBA':
                img_a = img_a.convert('RGB')
            if img_b.mode == 'RGBA':
                img_b = img_b.convert('RGB')
        # different size handler
        if img_a.size != img_b.size:
            new_width = img_b.width
            new_height = img_b.height
            img_a = img_a.resize((new_width, new_height))
        return imgcompare.image_diff_percent(img_a, img_b)


PORT = 5000
handler = ImageComparisonHandler
my_server = socketserver.TCPServer(("", PORT), handler)
my_server.serve_forever()