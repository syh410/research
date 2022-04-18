import cv2
from paddle_serving_client import Client
from paddle_serving_app.reader import DetectionSequential, \
    DetectionResize, \
    DetectionNormalize, \
    DetectionTranspose

class VehicleDetector:
    def __init__(self, url):
        self.preprocess = DetectionSequential([
            DetectionResize(
                (608, 608), False, interpolation=2),
            DetectionNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], True),
            DetectionTranspose((2, 0, 1)),
        ])
        self.client = Client()
        self.client.load_client_config("./app/vehicle_detector/vehicle_client/serving_client_conf.prototxt")
        if isinstance(url, str):
            self.client.connect([url])
        if isinstance(url, list):
            self.client.connect(url)

    def predict(self, image):
        im, _ = self.preprocess(image)
        fetch_map = self.client.predict(
            feed={
                "@HUB_yolov3_darknet53_vehicles@image": im,
                "@HUB_yolov3_darknet53_vehicles@im_size": image.shape[:2],
            },
            fetch=["@HUB_yolov3_darknet53_vehicles@multiclass_nms.tmp_0"],
            batch=False)
        return fetch_map