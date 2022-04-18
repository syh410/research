from common import get_image_v1
from flask import jsonify
from . import v1_bp
from vehicle_detector import VehicleDetector

vehicles_detector = VehicleDetector()
@v1_bp.route('/vehicle', methods=['POST'])
def vehicle():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = vehicles_detector.predict(image=image)

    def format_data(result):
        count = len(result)
        count_map = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorbike": 0,
            "tricycle": 0,
            "carplate": 0,
        }
        for item in result:
            count_map[item["label"]] += 1
        return {
            "count": count,
            "car_count": count_map["car"],
            "truck_count": count_map["truck"],
            "bus_count": count_map["bus"],
            "motorbike_count": count_map["motorbike"],
            "tricycle_count": count_map["tricycle"],
            "carplate_count": count_map["carplate"],
            "data": result,
        }

    return jsonify(format_data(result))
