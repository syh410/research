from flask import jsonify
from . import face_bp


@face_bp.route('/batch_upload', methods=['PUT', 'POST'])
def batch_upload():
    return jsonify({
        "code": 2,
        "msg": "人脸批量上传未实现"
    }), 500