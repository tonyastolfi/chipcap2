import BaseHTTPServer
import chipcap2
import json
import datetime


def trim(s):
    return s.strip().lower()


class RHTempRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        s = chipcap2.Sensor(1)
        rh, tempF = s.read()
        accept = map(trim, self.headers.get("Accept").split(','))
        print accept
        if 'application/json' in accept:
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "ts": str(datetime.datetime.now()),
                "rh": rh,
                "tempF": tempF,
                "tempC": s.tempC,
                "chipcap2_raw_data": s_.data
            }
            self.wfile.write(json.dumps(data))
        else:
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write('rh {}\ntempF {}\ntempC {}\n'.format(rh, tempF, s.tempC))
            for i in range(len(s._data)):
                self.wfile.write('chipcap2_raw_data{offset="%02d"} %d\n' % (i, s._data[i]))


def run(host="0.0.0.0",
        port=8000,
        server_class=BaseHTTPServer.HTTPServer,
        handler_class=RHTempRequestHandler):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
