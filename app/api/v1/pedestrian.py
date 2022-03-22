import paddlehub as hub
from common import get_image_v1
from flask import jsonify
from . import v1_bp

pedestrian_detector = hub.Module(name="yolov3_darknet53_pedestrian")
@v1_bp.route('/pedestrian', methods=['POST'])
def pedestrian():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = pedestrian_detector.object_detection(
        images=[image],
        use_gpu=True,
        visualization=False)

    def format_data(result):
        count = len(result["data"])
        data = []
        for i in range(count):
            data.append({
                "rect": {
                    "bottom": result["data"][i]["bottom"],
                    "top": result["data"][i]["top"],
                    "left": result["data"][i]["left"],
                    "right": result["data"][i]["right"],
                },
                "score": result["data"][i]["confidence"]
            })
        return {
            "count": count,
            "data": data
        }

    return jsonify(format_data(result[0]))
