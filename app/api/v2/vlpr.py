from plate_detector import PlateDetectionClient, LprnetDetectionClient
from common import get_image_v2
from flask import jsonify
from . import v2_bp
import cv2
import numpy as np

plate_detector = PlateDetectionClient()
lprnet_recognition = LprnetDetectionClient()
@v2_bp.route('/vlpr', methods=['POST'])
def vlpr():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        })
    results = plate_detector.predict(image = image)
    data = []
    if len(results):
        rect = []
        score = []
        images = []
        for result in results:
            score.append(result["score"])
            rect.append(result["rect"])
            pts_o = np.float32([[result["point"]["topleft"]["x"], result["point"]["topleft"]["y"]],
                                                [result["point"]["topright"]["x"], result["point"]["topright"]["y"]],
                                                [result["point"]["bottomleft"]["x"], result["point"]["bottomleft"]["y"]],
                                                [result["point"]["bottomright"]["x"], result["point"]["bottomright"]["y"]]])
            top = max(result["point"]["topleft"]["y"], result["point"]["topright"]["y"])
            bottom = max(result["point"]["bottomleft"]["y"], result["point"]["bottomright"]["y"])
            left = max(result["point"]["topleft"]["x"], result["point"]["bottomleft"]["x"])
            right = max(result["point"]["topright"]["x"], result["point"]["bottomright"]["x"])
            pts_d = np.float32([[left, top], [right, top], [left, bottom], [right, bottom]])
            img = cv2.getPerspectiveTransform(pts_o, pts_d)
            img = cv2.warpPerspective(image, img, (image.shape[1], image.shape[0]))
            img = img[int(top- 1):int(bottom + 1), int(left - 1):int(right + 1)]
            images.append(img)
        results = lprnet_recognition.predict(images = images)
        for i, result in enumerate(results):
            data.append({
                "license" : result,
                "score" : score[i],
                "rect" : rect[i]
            })

    def format_data(data):
        return {
            "code": 0,
            "msg": "OK",
            "count": len(data),
            "data": data
        }

    return jsonify(format_data(data))

