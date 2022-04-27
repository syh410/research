from light_detector import LightDetectionClient
from common import get_image_v2
from flask import jsonify
from . import v2_bp


light_detector = LightDetectionClient()
@v2_bp.route('/light', methods=['POST'])
def light():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    result = light_detector.predict(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))
