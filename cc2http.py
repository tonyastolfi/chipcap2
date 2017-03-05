#!/usr/bin/python
import BaseHTTPServer
import chipcap2
import json
import datetime
import os
import sys
import time
import httplib


childpid = os.fork()
if childpid != 0:
    print 'PARENT EUID={}'.format(os.geteuid())
    time.sleep(1)
    c = httplib.HTTPConnection('localhost', 8000)
    c.request('GET', '/')
    r = c.getresponse()
    if r.status == 200:
        print 'ChipCap2 exporter is RUNNING'
        sys.exit(0)
    else:
        print 'Failed to start, killing'
        os.kill(childpid, 9)
        sys.exit(1)

print 'CHILD EUID={}'.format(os.geteuid())
        
loc = sys.argv[1]
try:
    with open('/var/run/chipcap2.pid', 'w') as fp:
        fp.write('{}'.format(os.getpid()))
except:
    pass


def trim(s):
    return s.strip().lower()


class RHTempRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            s = chipcap2.Sensor(1)
            rh, tempF = s.read()
            accept = map(trim, (self.headers.get("Accept") or '').split(','))
            self.send_response(200)
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
                self.wfile.write('rh{location="%s"} %f\ntempF{location="%s"} %f\ntempC{location="%s"} %f\n'
                                 % (loc, rh, loc, tempF, loc, s.tempC))
                for i in range(len(s._data)):
                    self.wfile.write('chipcap2_raw_data{location="%s", offset="%02d"} %d\n' % (loc, i, s._data[i]))
        except Exception as e:
            print 'Error: {}'.format(e)
            self.send_response(503)


def run(host="0.0.0.0",
        port=8000,
        server_class=BaseHTTPServer.HTTPServer,
        handler_class=RHTempRequestHandler):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
