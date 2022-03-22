# coding:utf-8
from flask import Blueprint
from .face import *

v1_bp = Blueprint("v1", __name__, url_prefix="/v1")
v1_bp.register_blueprint(face_bp)

__all__ = [
    "v1_bp",
    "light",
    "mask",
    "pedestrian",
    "tts",
    "vehicle",
    "vlpr"
]
