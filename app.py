from flask import Flask, send_file
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/banner.png')
def serve_banner_png():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'banner.png')
    return send_file(file_path)

@app.route('/banner.gif')
def serve_banner_gif():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'banner.gif')
    return send_file(file_path)

if __name__ == "__main__":
    app.run(port=8000)
