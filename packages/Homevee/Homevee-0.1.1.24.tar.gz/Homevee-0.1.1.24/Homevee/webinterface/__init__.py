#!/usr/bin/python
# -*- coding: utf-8 -*-
import http.server
import os
import socketserver

from Homevee.Helper import Logger

PORT = 8000

def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", PORT), Handler)

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    Logger.log("HTTP-Server running on port: "+str(8000))

    httpd.serve_forever()