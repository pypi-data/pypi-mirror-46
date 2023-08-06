import sys
from flask import Flask
import webbrowser

def error(message):
    print("ERROR: {}".format(message), file=sys.stderr)
    return None

class DevServer():
    def __init__(self, port=5000):
        self.app = Flask(__name__)
        self.port = port

    def start(self):
        webbrowser.open("http://localhost:" + str(self.port), new=0, autoraise=False)
        self.app.run("127.0.0.1", port=self.port, debug=True)
