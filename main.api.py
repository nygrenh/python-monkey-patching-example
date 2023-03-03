import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import pkgutil
import importlib

import plugins_stable

host = 'localhost'
port = 3035

current_file_directory = os.path.dirname(os.path.realpath(__file__))

loaded_plugins = []

class Context:
    def __init__(self, response_text: str) -> None:
        self._response_text = response_text
    
    def set_response_text(self, new_text: str):
        self._response_text = new_text
    
    def get_response_text(self) -> str:
        return self._response_text


class WebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        response_text = self.get_response_text(self.client_address[0])
        context = Context(response_text)
        for plugin in loaded_plugins:
            plugin.run(context)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(context.get_response_text(), "utf-8"))

    def get_response_text(self, client_address):
        return f"Hello {client_address}, this is the server."


def load_plugins():
    plugins = []
    for _, name, _ in pkgutil.iter_modules(plugins_stable.__path__, f"{plugins_stable.__name__}."):
        print(f"Loading plugin {name}")
        plugins.append(importlib.import_module(name))
    global loaded_plugins
    loaded_plugins = plugins


if __name__ == "__main__":
    server = HTTPServer((host, port), WebServer)
    load_plugins()

    try: 
        print(f"Serving on http://{host}:{port}.")
        server.serve_forever()
        
    except KeyboardInterrupt:
        pass



