import cv2
from common import get_image_v1
from flask import jsonify
from . import face_bp
from . import face_recognition_client


@face_bp.route('/compare', methods=['POST'])
def compare():
    image1 = get_image_v1(image='image1')
    if image1 is None:
        return jsonify({
            "msg": "Image1 not found",
            "code": -1
        }), 400
    image1 = cv2.imencode('.jpg', image1)[1].tostring()
    image2 = get_image_v1(image='image2')
    if image2 is None:
        return jsonify({
            "msg": "Image2 not found",
            "code": -1
        }), 400
    image2 = cv2.imencode('.jpg', image2)[1].tostring()
    rtn, score = face_recognition_client.compare(image1, image2)
    if rtn != 0:
        return {
            "msg": "face compare failed",
            "code": rtn,
        }, 400
    def format_data(score):
        return {
            "msg": "SUCCESS",
            "code": 0,
            "score": score
        }
    return jsonify(format_data(score))