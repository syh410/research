import paddlehub as hub
from common import get_image_v2
from flask import jsonify
from . import v2_bp
import cv2
from face_detector import FaceDetector
from mask_detector import MaskDetector

mask_detector = MaskDetector()
face_detector = FaceDetector()
@v2_bp.route('/mask', methods=['POST'])
def mask():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    results = face_detector.predict(image=image)
    image = cv2.resize(image, (1024, 1024))
    data = []
    mask_count = no_mask_count = 0
    for result in results:
        rect = result['rect']
        img = image[int(rect['left']):int(rect['right']), int(rect['top']):int(rect['bottom'])]
        masks= mask_detector.predict(image=img)
        for mask in masks:
            data.append({
                    "score": mask['score'],
                    "rect": rect,
                    "mask": mask['mask'],
                })
            if mask['mask'] == True:
                mask_count += 1
            else:
                no_mask_count += 1

    def format_data(data, mask_count, no_mask_count):
        count = len(data)
        return {
            "msg": "OK",
            "code": 0,
            "count": count,
            "mask_count": mask_count,
            "no_mask_count": no_mask_count,
            "data": data,
        }

    return jsonify(format_data(data, mask_count, no_mask_count))
