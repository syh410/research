import cv2
from paddle_serving_client import Client
from paddle_serving_app.reader import DetectionSequential, \
    DetectionResize, \
    DetectionNormalize, \
    DetectionTranspose

class FaceDetector:
    def __init__(self, url= 'face_detection:9395', thresholds = 0.5):
        self.preprocess = DetectionSequential([
            DetectionResize(
                (1024, 1024), False, interpolation=2),
            DetectionNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], True),
            DetectionTranspose((2, 0, 1)),
        ])
        self.client = Client()
        self.thresholds = thresholds
        self.client.load_client_config("./face_detector/face_client/serving_client_conf.prototxt")
        if isinstance(url, str):
            self.client.connect([url])
        if isinstance(url, list):
            self.client.connect(url)

    def predict(self, image):
        im, _ = self.preprocess(image)
        fetch_map = self.client.predict(
            feed={
                "image": im,
            },
            fetch=["detection_output_0.tmp_0"],
            batch=False)
        result = []
        for data in fetch_map['detection_output_0.tmp_0']:
            if float(data[1]) <= self.thresholds:
                continue
            result.append({
                "score": float(data[1]),
                "rect":{
                    "left": float(max(data[2]*1000, 0)),
                    "top": float(max(data[3]*1000, 0)),
                    "right": float(max(data[4]*1000, 0)),
                    "bottom": float(max(data[5]*1000, 0))
                }
            })

        return result
