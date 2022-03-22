import cv2
from common import get_image_v1
from flask import jsonify, request
from . import face_bp
from . import face_recognition_client


@face_bp.route('/search', methods=['POST'])
def search():
    image = get_image_v1()
    if image is None:
        return jsonify({
            "msg": "Image not found",
            "code": -1,
            "data": []
        }), 400
    image = cv2.imencode('.jpg', image)[1].tostring()
    repo_id = request.form.get("repo_id")
    if repo_id is None:
        return jsonify({
            "msg": "repo_id not found",
            "code": -1
        }), 400
    rtn, result = face_recognition_client.search(image, repo_id)
    if rtn != 0:
        return {
            "msg": "face recognition failed",
            "code": rtn,
            "data": []
        }, 400
    def format_data(result):
        return {
            "msg": "SUCCESS",
            "code": 0,
            "data": result
        }
    return jsonify(format_data(result))
