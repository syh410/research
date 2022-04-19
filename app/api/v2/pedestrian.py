import paddlehub as hub
from common import get_image_v2
from flask import jsonify
from . import v2_bp
from pedestrian_detector import PedestrianDetector

pedestrian_detector = PedestrianDetector()
@v2_bp.route('/pedestrian', methods=['POST'])
def pedestrian():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    result = pedestrian_detector.predict(image=image)
    def format_data(result):
        count = len(result)
        return {
            "msg": "OK",
            "code": 0,
            "count": count,
            "data": result
        }

    return jsonify(format_data(result))