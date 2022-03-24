# coding:utf-8
from flask import Blueprint
from .face import *

v2_bp = Blueprint("v2", __name__, url_prefix="/v2")
v2_bp.register_blueprint(face_bp)

__all__ = [
    "v2_bp",
    # "light",
    # "mask",
    # "pedestrian",
    # "tts",
    # "vehicle",
    # "vlpr"
]
