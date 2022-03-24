import cv2
from flask import jsonify, request
from common import get_image_v2
from . import face_bp
from . import face_recognition_client


@face_bp.route('/batch_upload', methods=['PUT', 'POST'])
def batch_upload():
    face_ids, images = get_image_v2()
    if images is None:
        return jsonify({
            "msg": "images 参数不存在",
            "code": 1
        }), 400
    i = 0
    failed_id_list = []
    succ_num = 0
    fail_num = 0
    for i, image in enumerate(images):
        image = cv2.imencode('.jpg', image)[1].tobytes()
        repo_id = request.form.get("repo_id")
        if repo_id is None:
            return jsonify({
                "msg": "repo_id 参数不存在",
                "code": 1,
            }), 400
        face_id = face_ids[i]
        rtn = face_recognition_client.upload(image, face_id, repo_id)
        if rtn != 0:
            failed_id_list.append(face_id)
            fail_num = fail_num + 1
        else:
            succ_num = succ_num + 1
    if len(failed_id_list) > 0:
        return jsonify({
                "code": 2,
                "msg": "人脸批量上传未实现，共上传人脸" + str(succ_num+fail_num) + "张，上传成功" + str(succ_num) + "张，上传失败" + str(fail_num) + "张，失败人脸id为：" + ' '.join(failed_id_list)
            }), 500
    def format_data():
        return {
            "msg": "人脸批量上传成功，共上传人脸" + str(succ_num) + "张",
            "code": 0
        }

    return jsonify(format_data())