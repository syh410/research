# coding:utf-8
from flask import Blueprint

v1bp = Blueprint("v1", __name__)

__all__ = [
    "v1bp",
    "tts"]
