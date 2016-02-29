from http.server import HTTPServer, CGIHTTPRequestHandler

port = 8080
host_name = "localhost"
httpd = HTTPServer((host_name, port), CGIHTTPRequestHandler)
print("server started, to quit press <ctrl-c>")
httpd.serve_forever()