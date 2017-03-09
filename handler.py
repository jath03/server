#!/usr/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib, tools

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.myLog()
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png'}
        t_type = re.compile('\/|(\.\w*)')
        r_file = self.path.split('?')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        try:
            cookies = [h.split('=') for h in self.headers['Cookie'].split('; ')] 
        except:
            cookies = None
        tools.cookies(cookie=cookies, method='write')
        if ex != '.py' and ex != '':
            res = 200
            fileToSend = None
            hds = []
            root = pathlib.PurePath('/home/jack/projects/local/server/files')
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
                with open('/home/jack/projects/local/server/files/session.dat', 'wb') as file:
                    params = dict()
                    da = dict()
                    for pair in list(r_file[1].split('&')):
                        key, value = pair.split('=')
                        params[key] = str(value)
                    da.append(params)
                    print(da)
                    pickle.dump(da, file)
            except IndexError:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            file = subprocess.run(['python3.5', '/home/jack/projects/local/server/files%s'% r_file[0]], stdout=subprocess.PIPE)
            self.end_headers()
            self.wfile.write(file.stdout)
    def do_POST(self):
        self.myLog()
        f_type_map = {'.html': 'text/html', '.css': 'text/css', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.png': 'image/png'}
        t_type = re.compile('\/|(\.\w*)')
        r_file = self.path.split('?')
        requested_type = t_type.findall(self.path)
        ex = requested_type[-1]
        v = int(self.headers['Content-Length'])
        data = self.rfile.read(v)
        if ex != '.py' and ex != '':
            res = 200
            fileToSend = None
            hds = []
            root = pathlib.PurePath('/home/jack/projects/local/server/files')
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
                with open('/home/jack/projects/local/server/files/session.dat', 'wb') as file:
                    d = dict()
                    da = dict()
                    for pair in list(r_file[1].split('&')):
                        key, value = pair.split('=')
                        d[key] = str(value)
                    da.append(d)
                    da.append(dict(data))
                    pickle.dump(da, file)
            except IndexError:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            file = subprocess.run(['python3.5', '/home/jack/projects/local/server/files%s'% r_file[0]], stdout=subprocess.PIPE)
            self.wfile.write(file.stdout)

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
        with open('/home/jack/projects/local/.spy/data/ips.dat', 'ab') as f:
            pickle.dump(self.client_address[0], f)
