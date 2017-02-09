#!/usr/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
#        self.myLog()
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png'}
        t_type = re.compile('\/|(\.\w*)')
        r_file = self.path.split('?')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        root = pathlib.PurePath(os.path.dirname(os.path.realpath(__file__)) + "files")
        print(root)
        if ex != '.py' and ex != '':
            res = 200
            fileToSend = None
            hds = []
            f = root.joinpath(r_file[0].strip('/'))
            if not pathlib.Path(f).exists():
                res = 404
            elif pathlib.Path(f).is_dir():
                 if pathlib.Path(f / 'index.html').exists():
                     f = f / 'index.html'
                     with open(str(f), 'r') as file:
                         fileToSend = file.read()
                         hds.append(('content-type', 'text/html'))
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
                with open('/tmp/params.dat', 'wb') as file:
                    d = dict()
                    for pair in list(r_file[1].split('&')):
                        key, value = pair.split('=')
                        d[key] = str(value)
                    pickle.dump(d, file)
            except IndexError:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            print(root)
            p = root / r_file[0]
            print(p)
            file = subprocess.run(['python', str(p)], stdout=subprocess.PIPE)
            self.wfile.write(file.stdout)
    def do_POST(self):
#        self.myLog()
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
    def myLog(self):
        with open('/home/jack/projects/.spy/data/ips.dat', 'ab') as f:
            pickle.dump(self.client_address[0], f)


