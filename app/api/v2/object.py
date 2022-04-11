from object_detection import ObjectDetector
from common import get_image_v2
from flask import jsonify
from . import v2_bp

object_detector = ObjectDetector()
@v2_bp.route('/object', methods=['POST'])
def light():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    result = object_detector.detection(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))
