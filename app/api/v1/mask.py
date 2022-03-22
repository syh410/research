import paddlehub as hub
from common import get_image_v1
from flask import jsonify
from . import v1_bp

mask_detector = hub.Module(name="pyramidbox_lite_server_mask")
@v1_bp.route('/mask', methods=['POST'])
def mask():
    image = get_image_v1()
    if image is None:
        return "Image not found", 400
    result = mask_detector.face_detection(
        images=[image],
        use_gpu=True,
        visualization=False)

    def format_data(result):
        count = len(result["data"])
        data = []
        mask_count = no_mask_count = 0
        for i in range(count):
            data.append({
                "rect": {
                    "bottom": result["data"][i]["bottom"],
                    "top": result["data"][i]["top"],
                    "left": result["data"][i]["left"],
                    "right": result["data"][i]["right"],
                },
                "mask": result["data"][i]["label"] == "MASK",
                "score": result["data"][i]["confidence"],
            })
            if result["data"][i]["label"] == "MASK":
                mask_count += 1
            else:
                no_mask_count += 1
        return {
            "count": count,
            "mask_count": mask_count,
            "no_mask_count": no_mask_count,
            "data": data,
        }

    return jsonify(format_data(result[0]))
