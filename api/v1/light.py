from light_detector import LightDetector
from common import get_image_v1
from flask import jsonify
from . import v1_bp


light_detector = LightDetector("/home/pji/third/light.pth")
@v1_bp.route('/light', methods=['POST'])
def light():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = light_detector.detection(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))
