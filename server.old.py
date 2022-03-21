#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import result
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from paddlespeech.cli import TTSExecutor
import paddlehub as hub
import uuid
import cv2
import numpy as np
import paddle
from pydub import AudioSegment
from License_Plate_Detection_Pytorch.main import VehicleLicensePlate
from face_recognition.face_recognition_client import FaceRecognitionClient
from light_detector import LightDetector


app = Flask(__name__)
cors = CORS(app)


def get_image():
    if request.files['image']:
        return cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED), False
    return "Image not found", True


tts_executor = TTSExecutor()
@cross_origin()
@app.route('/api/v1/tts', methods=['POST'])
def tts():
    content = request.json
    text = content['text']
    if not text:
        return "Text not found", 400
    wav_file = tts_executor(
        text=text,
        output='/tmp/' + str(uuid.uuid4()) + '.wav',
        am='fastspeech2_csmsc',
        am_config=None,
        am_ckpt=None,
        am_stat=None,
        spk_id=0,
        phones_dict=None,
        tones_dict=None,
        speaker_dict=None,
        voc='pwgan_csmsc',
        voc_config=None,
        voc_ckpt=None,
        voc_stat=None,
        lang='zh',
        device=paddle.get_device())
    print('Wave file has been generated: {}'.format(wav_file))

    def wav_to_mp3(wav_file):
        mp3_file = wav_file.replace(".wav", ".mp3")
        AudioSegment.from_wav(wav_file).export(mp3_file, format="mp3")
        print('Mp3 file has been generated: {}'.format(mp3_file))
        return mp3_file

    return send_file(wav_to_mp3(wav_file))


mask_detector = hub.Module(name="pyramidbox_lite_server_mask")
@cross_origin()
@app.route('/api/v1/mask', methods=['POST'])
def mask():
    image, err = get_image()
    if err:
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


vehicles_detector = hub.Module(name="yolov3_darknet53_vehicles")
@cross_origin()
@app.route('/api/v1/vehicle', methods=['POST'])
def vehicle():
    image, err = get_image()
    if err:
        return "Image not found", 400
    result = vehicles_detector.object_detection(
        images=[image],
        use_gpu=True,
        visualization=False)

    def format_data(result):
        count = len(result["data"])
        data = []
        count_map = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorbike": 0,
            "tricycle": 0,
            "carplate": 0,
        }
        for i in range(count):
            data.append({
                "rect": {
                    "bottom": result["data"][i]["bottom"],
                    "top": result["data"][i]["top"],
                    "left": result["data"][i]["left"],
                    "right": result["data"][i]["right"],
                },
                "label": result["data"][i]["label"],
                "score": result["data"][i]["confidence"],
            })
            count_map[result["data"][i]["label"]] += 1
        return {
            "count": count,
            "car_count": count_map["car"],
            "truck_count": count_map["truck"],
            "bus_count": count_map["bus"],
            "motorbike_count": count_map["motorbike"],
            "tricycle_count": count_map["tricycle"],
            "carplate_count": count_map["carplate"],
            "data": data,
        }

    return jsonify(format_data(result[0]))


plate_recognition = VehicleLicensePlate()
@cross_origin()
@app.route('/api/v1/vlpr', methods=['POST'])
def vlpr():
    image, err = get_image()
    if err:
        return "Image not found", 400
    result = plate_recognition.plate_recognition(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))


pedestrian_detector = hub.Module(name="yolov3_darknet53_pedestrian")
@cross_origin()
@app.route('/api/v1/pedestrian', methods=['POST'])
def pedestrian():
    image, err = get_image()
    if err:
        return "Image not found", 400
    result = pedestrian_detector.object_detection(
        images=[image],
        use_gpu=True,
        visualization=False)

    def format_data(result):
        count = len(result["data"])
        data = []
        for i in range(count):
            data.append({
                "rect": {
                    "bottom": result["data"][i]["bottom"],
                    "top": result["data"][i]["top"],
                    "left": result["data"][i]["left"],
                    "right": result["data"][i]["right"],
                },
                "score": result["data"][i]["confidence"]
            })
        return {
            "count": count,
            "data": data
        }

    return jsonify(format_data(result[0]))


light_detector = LightDetector()
@cross_origin()
@app.route('/api/v1/light', methods=['POST'])
def light():
    image, err = get_image()
    if err:
        return "Image not found", 400
    result = light_detector.detection(image)

    def format_data(result):
        return {
            "count": len(result),
            "data": result
        }

    return jsonify(format_data(result))


face_recognition_client = FaceRecognitionClient()
@cross_origin()
@app.route('/api/v1/face', methods=['POST'])
def face():
    image, err = get_image()
    if err:
        return "Image not found", 400
    rtn, result = face_recognition_client.Search(image)
    if rtn != 0:
        return "face recognition failed", 400
    def format_data(result):
        return {
            "msg": "SUCCESS",
            "code": 0,
            "data": result
        }
    return jsonify(format_data(result))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)