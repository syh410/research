#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from api import api_bp

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api_bp)

    app.run(host="127.0.0.1", port=5001)