from flask import Flask
from flask_cors import CORS
from .v1 import *
from .v2 import *


def init_app():
    """Create Flask application."""
    app = Flask(__name__)

    app.register_blueprint(v1bp, url_prefix="/api/v1")

    return app