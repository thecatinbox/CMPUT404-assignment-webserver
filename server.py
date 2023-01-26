#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8')) 

        # Break down the request to find the request method and path 
        request_array = self.data.decode('utf-8').split()
        request_method = request_array[0]
        request_path = request_array[1]
        
        message = ""

        # Handle only the GET method 
        if request_method == "GET":
            if ".css" in request_path:
                # Supports mime-types for CSS
                content_type = "text/css"
            elif ".html" in request_path:
                # Supports mime-types for HTML 
                content_type = "text/html"
            else:
                if request_path[-1] == "/":
                    # Return index.html from directories (paths that end in /) 
                    request_path = request_path + "index.html"
                    content_type = "text/html"
                else:
                    # Use 301 to correct paths (add / at path ending)
                    message = "HTTP/1.1 301 Moved Permanently\r\n" + "Location:" + request_path +"/" +"\r\n\r\n" + "301 Moved Permanently"

            # If there is no 301 message 
            if message == "": 
                # Serve only files from ./www
                request_path = "./www" + request_path 
                # Check if the file exists 
                if os.path.isfile(request_path):
                    # Open file at path 
                    file = open(request_path, 'r')
                    message = "HTTP/1.1 200 OK\r\n" + "Content-Type:" + content_type + "\r\n\r\n" + file.read()
                else:
                    # Server 404 errors for paths not found
                    message = "HTTP/1.1 404 Not Found" + "\r\n\r\n" + "404 Not Found"
                
        else: 
            # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE) 
            message = "HTTP/1.1 405 Method Not Allowed" + "\r\n\r\n" + "405 Method Not Allowed"
        
        self.request.sendall(bytearray(message,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
