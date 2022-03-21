from flask import request
import cv2
import numpy as np

def get_image():
    if request.files['image']:
        return cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED), False
    return "Image not found", True
