from flask import jsonify, request
from . import face_bp
from . import face_recognition_client


@face_bp.route('/delete', methods=['DELETE'])
def delete():
    repo_id = request.form.get("repo_id")
    if repo_id is None:
        return jsonify({
            "msg": "repo_id 参数不存在",
            "code": 1
        })
    face_id = request.form.get("face_id")
    if face_id is None:
        return jsonify({
            "msg": "face_id 参数不存在",
            "code": 1
        })
    
    rtn = face_recognition_client.delete(face_id, repo_id)
    if rtn != 0:
        error_codes = {
            30000: "face_id 不存在",
        }
        msg = "人脸删除失败"
        if rtn in error_codes:
            msg = error_codes[rtn]
        return jsonify({
            "msg": msg,
            "code": rtn
        })
    def format_data():
        return {
            "msg": "OK",
            "code": 0
        }
    return jsonify(format_data())