import http.server, os, sys
os.chdir('/Users/rashetdacambridge/Documents/Git')
port = int(os.environ.get('PORT', 8765))
handler = http.server.SimpleHTTPRequestHandler
with http.server.HTTPServer(('', port), handler) as httpd:
    print(f'Serving on port {port}', flush=True)
    httpd.serve_forever()
