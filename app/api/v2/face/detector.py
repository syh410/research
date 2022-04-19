import paddlehub as hub
from common import get_image_v2
from flask import jsonify
from . import face_bp
from face_detector import FaceDetector


face_detector = FaceDetector()
@face_bp.route('/detector', methods=['POST'])
def detector():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1,
        })
    result = face_detector.predict(image=image)

    def format_data(result):
        count = len(result)
        return {
            "msg": "OK",
            "code": 0,
            "count": count,
            "data": result
        }

    return jsonify(format_data(result))
