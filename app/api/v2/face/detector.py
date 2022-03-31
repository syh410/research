import paddlehub as hub
from common import get_image_v2
from flask import jsonify
from . import face_bp


face_detector = hub.Module(name="pyramidbox_lite_server")
@face_bp.route('/detector', methods=['POST'])
def detector():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1,
        })
    result = face_detector.face_detection(
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
            "msg": "OK",
            "code": 0,
            "count": count,
            "data": data
        }

    return jsonify(format_data(result[0]))
