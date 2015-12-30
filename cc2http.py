import BaseHTTPServer
import chipcap2
import json
import datetime

class RHTempRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        s = chipcap2.Sensor(1)
        rh, tempF = s.read()
        data = {"ts": str(datetime.datetime.now()), "rh": rh, "tempF": tempF}
        self.wfile.write(json.dumps(data))

def run(host="localhost",
        port=8000,
        server_class=BaseHTTPServer.HTTPServer,
        handler_class=RHTempRequestHandler):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
