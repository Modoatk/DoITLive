import time
import BaseHTTPServer

import errorbox
import main


HOST_NAME = 'localhost'

PORT_NUMBER = 8080


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        if s.path.endswith('.css'):
            s.send_header("Content-type", "text/css")
        elif s.path.endswith('.html'):
            s.send_header("Content-type", "text/html")
        s.end_headers()
        
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.end_headers()
        path = s.path

        if path == '/':
            f = open('../bootstrap/index.html')
            x = f.read()
            s.wfile.write(x)
        elif path == '/error':
            s.wfile.write('<br>'.join(errorbox.get_errors()))
        else:
            f = open('../bootstrap' + path) # TODO: Security hole (path exploit) also path
            x = f.read()
            s.wfile.write(x)


    def do_POST(s):
        if s.path == "/start":
            main.start_service("../flybox")
            s.send_response(200)
            s.end_headers()
            s.wfile.write("")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - {0}:{1}".format(HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - {0}:{1}".format(HOST_NAME, PORT_NUMBER)