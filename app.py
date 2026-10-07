from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Backend Application!")

server = HTTPServer(("127.0.0.1", 5001), Handler)
print("Backend running on port 5001")
server.serve_forever()
