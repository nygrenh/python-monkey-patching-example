import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import pkgutil


host = 'localhost'
port = 3035

current_file_directory = os.path.dirname(os.path.realpath(__file__))
plugins_directory = os.path.join(current_file_directory, "plugins")

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        response_text = self.get_response_text(self.client_address[0])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(response_text, "utf-8"))

    def get_response_text(self, client_address):
        return f"Hello {client_address}, this is the server."

def load_plugins():
    for filename in os.listdir(plugins_directory):
        file_path = os.path.join(plugins_directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as filename:
                contents = filename.read()
            print(f"Loading plugin {file_path}.")
            exec(contents)


if __name__ == "__main__":
    server = HTTPServer((host, port), WebServer)
    load_plugins()

    try: 
        print(f"Serving on http://{host}:{port}.")
        server.serve_forever()
        
    except KeyboardInterrupt:
        pass

