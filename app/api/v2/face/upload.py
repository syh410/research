import cv2
from common import get_image_v2
from flask import jsonify, request
from . import face_bp
from . import face_recognition_client


@face_bp.route('/upload', methods=['POST'])
def upload():
    image = get_image_v2()
    if image is None:
        return jsonify({
            "msg": "image 或 url 参数不存在",
            "code": 1
        }), 400
    image = cv2.imencode('.jpg', image)[1].tostring()
    repo_id = request.form.get("repo_id")
    if repo_id is None:
        return jsonify({
            "msg": "repo_id 参数不存在",
            "code": 1
        }), 400
    face_id = request.form.get("face_id")
    if face_id is None:
        return jsonify({
            "msg": "face_id 参数不存在",
            "code": 1
        }), 400
    
    rtn = face_recognition_client.upload(image, face_id, repo_id)
    if rtn != 0:
        error_codes = {
            3: "未检测到人脸",
            30001: "face_id 重复",
        }
        msg = "人脸上传失败"
        if rtn in error_codes:
            msg = error_codes[rtn]
        return jsonify({
            "msg": msg,
            "code": rtn
        }), 400
    def format_data():
        return {
            "msg": "OK",
            "code": 0
        }
    return jsonify(format_data())