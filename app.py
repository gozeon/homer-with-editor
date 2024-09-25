import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == '/editconfig':
            try:
                with open('assets/config.yml', 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"""<!doctype html>
                        <meta charset=utf8>
                        <button onclick='save()'>save</button>
                        <script>const doc = `{content}`</script>
                        <script src='/editconfig/editor.bundle.js'></script>""".encode('utf-8'))
            except FileNotFoundError:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/editconfig':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            with open('assets/config.yml', 'w', encoding='utf-8') as file:
                file.write(post_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_response(404)
            self.end_headers()
            
def run(port=8080):
    os.chdir('.')  
    handler_class = CustomHTTPRequestHandler
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    print(f'Serving static files from the current directory on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
