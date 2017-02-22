#!/usr/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib, argparse, socket
from threadingHandler import MyHandler
import netifaces as ni
from socketserver import ThreadingMixIn

par = argparse.ArgumentParser()
par.add_argument("-p", "--port", nargs=1, action='store')
par.add_argument("-a", "--address", nargs=1, action='store')
args = par.parse_args()
port = int(args.port[0])
addresses = list()
if args.address is None:
    server_address = (socket.gethostbyname(socket.gethostname()), port)
else:
    server_address = (str(args.address[0]), port)
print(server_address)

class MyServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    print('starting server ...')
    httpd = MyServer(server_address, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
run()
