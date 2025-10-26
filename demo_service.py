from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "BentoML Demo Service",
                "status": "running",
                "endpoints": {
                    "predict": "POST /predict",
                    "health": "GET /health"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/predict':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                input_data = json.loads(post_data.decode('utf-8'))
                response = {
                    "prediction": "Demo prediction result",
                    "input": input_data,
                    "model": "demo_model_v1.0"
                }
            except:
                response = {
                    "error": "Invalid JSON input",
                    "example": {"data": [1, 2, 3, 4]}
                }

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = HTTPServer(('0.0.0.0', port), DemoHandler)
    print(f"Demo BentoML service running on port {port}")
    server.serve_forever()
