#!/usr/bin/python3.5
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading, pickle, re, subprocess, urllib, os, pathlib, argparse, socket
from handler import MyHandler
import netifaces as ni
par = argparse.ArgumentParser()
par.add_argument("-p", "--port", nargs=1, action='store')
args = par.parse_args()
port = int(args.port[0])
addresses = list()
server_address = (ni.ifaddresses('wlan0')[2][0]['addr'], port)
print(server_address)
def run():
    print('starting server ...')
    httpd = HTTPServer(server_address, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
bg_server = threading.Thread(target=run)
if __name__ == "__main__":
    bg_server.start()
    print('\nserver started at {}:{}'.format(server_address))
