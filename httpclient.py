#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
import json

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):             
        return int([i for i in data.split(" ")][1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        body_index = data.find('\r\n\r\n')
        # print(body_index)
        return data[body_index+4:]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:            
            part = sock.recv(1024)    
            print(part)
            if (part):
                buffer.extend(part)
            else:
                done = not part            
        return buffer.decode('utf-8')

    def GET(self, url, args=None):              
    
        code = 500
        try:

            o = urllib.parse.urlparse(url)
            scheme = o.scheme
            
            port = o.port if o.port else 80
            host = o.hostname
            path = o.path if "/" in o.path else "/"

            print("scheme:", scheme)
            print("host:", host)
            print("port:", port)
            print("path:", path)
            self.connect(host, port)

        # TODO: use urllib.parse
        
            message = f"GET {path} HTTP/1.1\r\n" \
                      f"Host: {host}\r\n" \
                      f"Connection: close\r\n" \
                      f"\r\n"
                      
            print("Message:")
            print(message)
            self.sendall(message)            
            body = self.recvall(self.socket)          
            self.close()
            # code = self.get_code(body)
            print("body:")
            print(body)        
            body = str(body)    
            code = self.get_code(body)                
            body = self.get_body(body)
        except Exception as e:     
            print(e)      
            body = ""
        
        print(code)
        print(body)
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        o = urllib.parse.urlparse(url)

        port = o.port
        host = o.hostname
        path = o.path
        
        post_data = ""  # Replace with your data
        
        if args:
            for i, (key, value) in enumerate(args.items()):
                post_data += str(key) + "="
                post_data += str(value)
                if (i < len(args) - 1):
                    post_data += "&"

        self.connect(host, port)

        message =f"POST {path} HTTP/1.1\r\n" \
                f"Host: {host} \r\n" \
                f"Content-Type: application/x-www-form-urlencoded\r\n" \
                f"Content-Length: {len(post_data)}\r\n" \
                f"\r\n" \
                f"{post_data}"

        try:
            self.sendall(message)        
            self.socket.shutdown(socket.SHUT_WR)        
            body = self.recvall(self.socket)
            self.close()
            code = self.get_code(body)   
            body = self.get_body(body)
        
        except Exception as e:            
            print(e)
            body  = b""
        
        
        print("result:")
        print(code)
        print(body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        print(url)
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
