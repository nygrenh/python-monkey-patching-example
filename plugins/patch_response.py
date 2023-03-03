WebServer = globals()["WebServer"]

global original_get_response_text
original_get_response_text = WebServer.get_response_text

def new_get_response_text(self):
    original_response = original_get_response_text(self)
    return f"[Hello from the plugin!] {original_response}"

WebServer.get_response_text = new_get_response_text
