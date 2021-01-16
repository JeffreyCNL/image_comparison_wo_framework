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
        # token = parse_qs(parsed.query)['token'][0]
        # if token != 'kmrhn74zgzcq4nqb':
        #     response = {
        #         'success': False,
        #         'error': 'Authetication failed.'
        #     }
        #     self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        # if self.headers.get('Authorization') == None:
        #     self.do_AUTHHEAD()
        #     response = {
        #         'success': False,
        #         'error': 'Authetication failed.'
        #     }
        #     self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # elif self.path.startswith('/image-comparison', 0, 17):
        #     parsed = urlparse.urlparse(self.path)
        #     api = ImageComparisonAPI()
        #     img_a_path = parse_qs(parsed.query)['img_a'][0]
        #     img_b_path = parse_qs(parsed.query)['img_b'][0]
        #     percent = api.get_percent(img_a_path, img_b_path)
        #     self.path = 'otherPage.html'
        #     self.send_header('Content-type','text/html')
        #     self.send_response(200)
        #     self.end_headers()
        #     self.wfile.write(b'<!DOCTYPE html>\n<meta charset=utf-8 />\n<title>Notification page</title>\n')
            # response = {
            #     'success': True,
            #     'percent': str(percent)
            # }
            # self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            # self.end_headers()
            # self.wfile.write(b'percent: ' + bytes(str(percent), 'utf-8'))
            # self.wfile.write(b'%.2f\r\n' % percent)
            # self.wfile.write(json.dumps({
                # 'percent': b'%.2f\r\n' % percent
            # }))
            # response = {
            #     'status':'SUCCESS',
            #     'data':'hello from server'
            # }
            # self.wfile.write(json.dumps(response))
            #print(percent)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.wfile.write(b'<!DOCTYPE html>\n<meta charset=utf-8 />\n<title>Notification page</title>\n')
        self.wfile.write(b'<style>body {max-width:400px; background:#fff8ea;}</style>\n')
        self.wfile.write(b'\n<p>\nSehr geehrte Damen und Herren,<br />\n<br />\naufgrund eines technischen Problems ist die Seite derzeit offline. Wir arbeiten bereits an einer L&ouml;sung und werden wohl bereits morgen wieder wie gewohnt erreichbar sein. <br />\n<br />\nVielen Dank f&uuml;r Ihr Verst&auml;ndnis,<br />\nDas Team\n</p>\n\n')
        #self.wfile.write('<!-- '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' // '+self.path+'-->\n')
            

        return
        # return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        print ("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print ("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    

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
        return imgcompare.image_diff_percent(img_a, img_b)


PORT = 5000
handler = ImageComparisonHandler
my_server = socketserver.TCPServer(("", PORT), handler)
my_server.serve_forever()