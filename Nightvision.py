#!/usr/bin/env python3

from ssl import create_default_context
from flask import Flask, request, send_file
from flask_cors import CORS
import os.path
import argparse


parser = argparse.ArgumentParser(prog='Nightvision', 
                                 description="Nightvision acts as a fake web server that outputs requests - useful for blind SSRF, XSS etc.")

parser.add_argument("-s", "--secure", action="store_true", help="Enables HTTPS and generates certificates if required")
parser.add_argument("-p", "--port", help="The port to listen on - defaults to 80/443")
args = parser.parse_args()

app = Flask(__name__)
CORS(app)


@app.route('/payload.js') 
def payload():
    print("[+] Sending payload")
    return send_file("./payload.js", download_name="payload.js")

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route("/<string:path>", methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def inputs(path):
    data = request.get_data()
    print("[+] Received: \r\n%s" % data)
    return "Thanks"


if (args.secure):
    file_path = os.path.dirname(__file__)
    cert = file_path + "/cert.pem"
    key = file_path + "/key.pem"
    if (os.path.isfile(cert) == False or os.path.isfile(key) == False):
        os.system("openssl req -x509 -newkey rsa:4096 -nodes -out "+cert+" -keyout "+key+" -days 1440")
    port = args.port or 443
    app.run(host='0.0.0.0', port=port, ssl_context=(cert, key))
else:
    port = args.port or 80
    app.run(host='0.0.0.0', port=port)


