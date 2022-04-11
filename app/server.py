#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from api import api_bp

app = Flask(__name__)

if __name__ == '__main__':
    CORS(app)
    app.config["JSON_AS_ASCII"] = False
    app.register_blueprint(api_bp)

    app.run(host="0.0.0.0", port=5000)
