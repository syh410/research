from flask import jsonify
from . import face_bp


@face_bp.route('/batch_upload', methods=['PUT', 'POST'])
def batch_upload():
    faceIds, images = get_image_v2()
    if images is None:
        return jsonify({
            "msg": "images 参数不存在",
            "code": 1
        }), 400
    i = 0
    failed_id = ''
    for image in images:
        image = cv2.imencode('.jpg', image)[1].tobytes()
        repo_id = request.form.get("repo_id")
        if repo_id is None:
            return jsonify({
                "msg": "repo_id 参数不存在",
                "code": 1,
            }), 400
        face_id = faceIds[i]
        rtn = face_recognition_client.upload(image, face_id, repo_id)
        if rtn != 0:
            failed_id = failed_id + face_id + ','
        i = i + 1
    if failed_id:
        return jsonify({
                "code": 2,
                "msg": "人脸批量上传未实现(" + failed_id + "上传失败)"
            }), 500
    def format_data():
        return {
            "msg": "OK",
            "code": 0
        }

    return jsonify(format_data())