from License_Plate_Detection_Pytorch import VehicleLicensePlate
from common import get_image_v1
from flask import jsonify
from . import v1_bp

plate_recognition = VehicleLicensePlate()
@v1_bp.route('/vlpr', methods=['POST'])
def vlpr():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = plate_recognition.plate_recognition(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))
