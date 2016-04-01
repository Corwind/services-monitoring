import http.server
import subprocess
import yaml
import json
import sys
from socketserver import ThreadingMixIn


def config(conf):
    with open(conf, 'r') as c:
        CONFIG = yaml.load('\n'.join(c.readlines()))
    return CONFIG


class RequestHandler(http.server.BaseHTTPRequestHandler):
    config = None

    def get_status(self):
        result = {}
        if not self.config:
            self.config = config(sys.argv[1])
        for srv in self.config['services']:
            cp = ''
            try:
                cp = subprocess.check_output([self.config['command'],
                *(self.config['strformat'].format(status=self.config['arg'],
                    service=srv).split())], universal_newlines =
                True)
            except Exception as e:
                cp = e.output
            if 'running' in cp:
                result[srv] = ['running', cp]
            else:
                result[srv] = ['inactive', cp]
        return result

    def do_GET(self):
        print(self.headers)
        try:
            if self.path.startswith('/query'):
                data = self.get_status()
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self.send_error(404)
        except Exception as e:
            print(e)
            print(e.args)
            print(type(e))
            self.send_error(500, message=str(e))


class MHTTPServer(http.server.HTTPServer, ThreadingMixIn):
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <config-file>'.format(sys.argv[0]))
        sys.exit(1)

    CONFIG = {}
    config(sys.argv[1])
    server = MHTTPServer(('127.0.0.1', 4242), RequestHandler)
    server.serve_forever()
