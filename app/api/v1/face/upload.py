import cv2
from common import get_image_v1
from flask import jsonify, request
from . import face_bp
from . import face_recognition_client


@face_bp.route('/upload', methods=['POST'])
def upload():
    image = get_image_v1()
    if image is None:
        return jsonify({
            "msg": "Image not found",
            "code": -1
        }), 400
    image = cv2.imencode('.jpg', image)[1].tostring()
    repo_id = request.form.get("repo_id")
    if repo_id is None:
        return jsonify({
            "msg": "repo_id not found",
            "code": -1
        }), 400
    face_id = request.form.get("face_id")
    if face_id is None:
        return jsonify({
            "msg": "face_id not found",
            "code": -1
        }), 400
    
    rtn = face_recognition_client.upload(image, face_id, repo_id)
    if rtn != 0:
        return jsonify({
            "msg": "face upload failed",
            "code": rtn
        }), 400
    def format_data():
        return {
            "msg": "SUCCESS",
            "code": 0
        }
    return jsonify(format_data())