import BaseHTTPServer
import chipcap2
import json

class RHTempRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        s = chipcap2.Sensor(1)
        rh, tempF = s.read()
        data = {"rh": rh, "tempF": tempF}
        self.wfile.write(json.dumps(data))

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=RHTempRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
