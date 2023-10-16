from http.server import HTTPServer, CGIHTTPRequestHandler
server = HTTPServer (('', 5000), CGIHTTPRequestHandler)
server.serve_forever()