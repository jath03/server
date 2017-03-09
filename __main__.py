#!/usr/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib, argparse
from handler import MyHandler
ag = argparse.ArgumentParser()
ag.add_argument('-t', '--test', action='store_true')
args = ag.parse_args()
print(args)
if args.test:
    address = ('192.168.5.1', 9999)
else:
    address = ('10.0.0.117', 6789)
def run():
    print('starting server ...')
    httpd = HTTPServer(address, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
bg_server= threading.Thread(target = run)
bg_server.start()
