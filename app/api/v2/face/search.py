import cv2
from common import get_image_v2
from flask import jsonify, request, current_app
from . import face_bp
from . import face_recognition_client


@face_bp.route('/search', methods=['POST'])
def search():
    image = get_image_v2()
    current_app.logger.warn("image")
    current_app.logger.warn(image)
    repo_id = request.form.get("repo_id")
    current_app.logger.warn("repo_id")
    current_app.logger.warn(repo_id)
    if image is None:
        current_app.logger.warn("image 或 url 参数不存在")
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1,
        })
    image = cv2.imencode('.jpg', image)[1].tostring()

    if repo_id is None:
        current_app.logger.warn("repo_id参数不存在")
        return jsonify({
            "msg": "repo_id 参数不存在",
            "code": 1,
        })
    rtn, result = face_recognition_client.search(image, repo_id)
    if rtn != 0:
        error_codes = {
            3: "未检测到人脸",
            30000: "repo_id 不存在",
        }
        msg = "人脸上传失败"
        if rtn in error_codes:
            msg = error_codes[rtn]
            current_app.logger.warn(msg)
        return {
            "msg": msg,
            "code": rtn
        }
    def format_data(result):
        return {
            "msg": "OK",
            "code": 0,
            "data": result
        }
    return jsonify(format_data(result))
