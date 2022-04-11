from flask import Blueprint
from face_recognition import FaceRecognitionClient

face_bp = Blueprint('face', __name__, url_prefix='/face')
face_recognition_client = FaceRecognitionClient()

__all__ = [
    "face_bp",
    "compare",
    "detector",
    "search",
    "upload",
    "batch_upload",
    "update",
    "delete",
]
