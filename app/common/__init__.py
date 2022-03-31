from flask import request, current_app
import cv2
import numpy as np
import urllib.request

def get_image_v1(image='image'):
    if request.files[image]:
        img = cv2.imdecode(np.fromstring(request.files[image].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    return None

def get_image_v2(image='image', url='url'):
    try:
        if request.files.get(image) is not None:
            img = cv2.imdecode(np.fromstring(request.files[image].read(), np.uint8), cv2.IMREAD_UNCHANGED)
            if len(img.shape) > 2 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
        if request.form.get(url) is not None:
            with urllib.request.urlopen(request.form.get(url)) as req:
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)
                if len(img.shape) > 2 and img.shape[2] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
    except Exception:
        return None
    return None
