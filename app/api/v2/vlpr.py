from License_Plate_Detection_Pytorch import VehicleLicensePlate
from common import get_image_v2
from flask import jsonify
from . import v2_bp

plate_recognition = VehicleLicensePlate()
@v2_bp.route('/vlpr', methods=['POST'])
def vlpr():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        }), 200
    result = plate_recognition.plate_recognition(image)

    def format_data(result):
        return {
            "code": 0,
            "msg": "OK",
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))
