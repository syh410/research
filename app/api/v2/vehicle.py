from common import get_image_v2
from flask import jsonify
from . import v2_bp
from vehicle_detector import VehicleDetector

vehicles_detector = VehicleDetector()
@v2_bp.route('/vehicle', methods=['POST'])
def vehicle():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    result = vehicles_detector.object_detection(
        images=[image],
        use_gpu=True,
        visualization=False,
        score_thresh=0.5)
    vehicles_detector.gpu_predictor.clear_intermediate_tensor()
    vehicles_detector.gpu_predictor.try_shrink_memory()

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
            "code": 0,
            "msg": "OK",
            "count": count,
            "car_count": count_map["car"],
            "truck_count": count_map["truck"],
            "bus_count": count_map["bus"],
            "motorbike_count": count_map["motorbike"],
            "tricycle_count": count_map["tricycle"],
            "carplate_count": count_map["carplate"],
            "data": result,
        }

    return jsonify(format_data(result[0]))
