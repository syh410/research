import paddlehub as hub
from common import get_image_v1
from flask import jsonify
from . import v1_bp

vehicles_detector = hub.Module(name="yolov3_darknet53_vehicles")
@v1_bp.route('/vehicle', methods=['POST'])
def vehicle():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = vehicles_detector.object_detection(
        images=[image],
        use_gpu=True,
        visualization=False)

    def format_data(result):
        count = len(result["data"])
        data = []
        count_map = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorbike": 0,
            "tricycle": 0,
            "carplate": 0,
        }
        for i in range(count):
            data.append({
                "rect": {
                    "bottom": result["data"][i]["bottom"],
                    "top": result["data"][i]["top"],
                    "left": result["data"][i]["left"],
                    "right": result["data"][i]["right"],
                },
                "label": result["data"][i]["label"],
                "score": result["data"][i]["confidence"],
            })
            count_map[result["data"][i]["label"]] += 1
        return {
            "count": count,
            "car_count": count_map["car"],
            "truck_count": count_map["truck"],
            "bus_count": count_map["bus"],
            "motorbike_count": count_map["motorbike"],
            "tricycle_count": count_map["tricycle"],
            "carplate_count": count_map["carplate"],
            "data": data,
        }

    return jsonify(format_data(result[0]))
