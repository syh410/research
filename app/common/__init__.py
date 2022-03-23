from flask import request, current_app
import cv2
import numpy as np
import urllib
import zipfile
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import shutil

def get_image_v1(image='image'):
    if request.files[image]:
        img = cv2.imdecode(np.fromstring(request.files[image].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    return None

def get_image_v2(image='image', url='url',images='images'):
    if request.files.get(image) is not None:
        img = cv2.imdecode(np.fromstring(request.files[image].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    if request.form.get(url) is not None:
        req = urllib.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    if request.files.get(images) is not None:
        profile = request.files[images]
        img_root_dir = "./images/"
        if not os.path.exists(img_root_dir):
            os.mkdir(img_root_dir)
        profile.save(os.path.join(img_root_dir, secure_filename(profile.filename)))
        zfile = zipfile.ZipFile(os.path.join(img_root_dir, secure_filename(profile.filename)),'r')
        faceIds = []
        images = []
        for name in zfile.namelist()[1:]:
            img = cv2.imdecode(np.fromstring(zfile.read(name), np.uint8), cv2.IMREAD_UNCHANGED)
            if len(img.shape) > 2 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            Index1 = name.rfind("/")
            Index2 = name.find(",")
            faceid = name[Index1+1:Index2]
            faceIds.append(faceid)
            images.append(img)
        shutil.rmtree(img_root_dir)
        return mFaceids, mImages
    

    return None