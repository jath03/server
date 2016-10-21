#!/usr/local/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png'}
        t_type = re.compile('\/|(\.\w*)')
        r_file = self.path.split('?')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        if ex != '.py' and ex != '':
            res = 200
            fileToSend = None
            hds = []
            root = pathlib.PurePath('/home/jack/projects/server/files')
            f = root.joinpath(r_file[0].strip('/'))
            if not pathlib.Path(f).exists():
                res = 404
            elif pathlib.Path(f).is_dir():
                 if pathlib.Path(f / 'index.html').exists():
                     f = f / 'index.html'
                     with open(str(f), 'r') as file:
                         fileToSend = file.read()
                         hds.append(('content-type', 'text/html'))
                     print(f)
                 else:
                     res = 404
            else:
                try:
                    with open(str(f), 'r') as file:
                        fileToSend = file.read()
                        hds.append(('content-type', f_type_map[ex]))
                except UnicodeDecodeError:
                    with open(str(f), 'rb') as file:
                        fileToSend = file.read()
                        hds.append(('content-type', f_type_map[ex]))
            if res == 200:
                self.send_response(res)
            else:
                self.send_error(res)
            for item in hds:
                i1, i2 = item
                self.send_header(i1, i2)
            self.end_headers()
            if fileToSend is not None:
                try:
                    self.wfile.write(fileToSend.encode('utf-8'))
                except AttributeError:
                    self.wfile.write(fileToSend)
            return
        else:
            try:
                with open('/home/jack/projects/server/files/params.dat', 'ab') as file:
                    d = dict()
                    for pair in r_file[1].split('&'):
                        key, value = pair.split('=')
                        d[key] = value
                    pickle.dump(d, file)
            except IndexError:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            file = subprocess.run(['python3.5', '/home/jack/projects/server/files%s'% r_file[0]], stdout=subprocess.PIPE)
            self.wfile.write(file.stdout)
    def do_POST(self):
        try:
            res = 200
            f = None
            hds = [('Content-Encoding', 'utf-8')]
            try:
                with open('/home/jack/projects/server/cgi-bin%s'% r_file[0]) as file:
                    f = file.read()
                    #f = 'This is my secret message'
                    #self.wfile.write(bytes(f, 'utf8'))
            except UnicodeDecodeError:
                with open('/home/jack/projects/server/cgi-bin%s'% r_file[0], 'rb') as file:
                    f = file
                    #self.wfile.write(f)
        except IOError:
            res = 404
            f = None
            #self.send_error(404, 'File Not Found')
            #self.wfile.write(bytes('404 file not found', 'utf8'))
        except KeyError:
            #self.send_response(200)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            with open('/home/jack/projects/server/cgi-bin') as file:
                #f = 'This is my secret message'
                f = file
                #self.wfile.write(bytes(f, 'utf8'))
        if res == 200:
            self.send_response(res)
        else:
            self.send_error(res)
        for item in hds:
            i1, i2 = item
            self.send_header(i1, i2)
        self.end_headers()
        if f != None:
            file = subprocess.run(['python', '/home/jack/projects/server/cgi-bin%s'% r_file[0]], stdout=subprocess.PIPE)
            self.wfile.write(file.stdout.encode('utf-8'))   
        
        else:
            pass
        return

    def do_OPTIONS(self):
        methods = ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']
        sup_methods = []
        self.send_response(200)
        for m in methods:
            if hasattr(self, 'do_' + m):
                sup_methods.append(m)
            else:
                pass
        print(sup_methods)
        meth = ', '.join(sup_methods)
        self.send_header('Allow', meth)
        self.end_headers()

server_address = ('192.168.5.1', 6789)
def run():
    print('starting server ...')
    httpd = HTTPServer(server_address, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
bg_server= threading.Thread(target = run)

if __name__ == '__main__':
    bg_server.start()
    print('\nserver started at %s:%s'% server_address)


