import cv2
from common import get_image_v2
from flask import jsonify
from . import face_bp
from . import face_recognition_client


@face_bp.route('/compare', methods=['POST'])
def compare():
    image1 = get_image_v2(image='image1', url='url2')
    if image1 is None:
        return jsonify({
            "msg": "image1 或 url1 参数不存在",
            "code": 1
        }), 400
    image1 = cv2.imencode('.jpg', image1)[1].tostring()
    image2 = get_image_v2(image='image2', url='url2')
    if image2 is None:
        return jsonify({
            "msg": "image2 或 url2 参数不存在",
            "code": 1
        }), 400
    image2 = cv2.imencode('.jpg', image2)[1].tostring()
    rtn, score = face_recognition_client.compare(image1, image2)
    if rtn != 0:
        msg = "人脸比对失败"
        error_codes = {
            3: "未检测到人脸",
        }
        if rtn in error_codes:
            msg = error_codes[rtn]
        return {
            "msg": msg,
            "code": rtn,
        }, 400
    def format_data(score):
        return {
            "msg": "OK",
            "code": 0,
            "score": score
        }
    return jsonify(format_data(score))