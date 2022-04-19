import cv2
from paddle_serving_client import Client
from paddle_serving_app.reader import DetectionSequential, \
    DetectionResize, \
    DetectionNormalize, \
    DetectionTranspose

class MaskDetector:
    def __init__(self, url= 'mask_detection:9396', thresholds = 0.5):
        self.preprocess = DetectionSequential([
            DetectionResize(
                (128, 128), False, interpolation=2),
            DetectionNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], True),
            DetectionTranspose((2, 0, 1)),
        ])
        self.client = Client()
        self.thresholds = thresholds
        self.client.load_client_config("./mask_detector/mask_client/serving_client_conf.prototxt")
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
            fetch=["save_infer_model/scale_0"],
            batch=False)
        result = []
        for data in fetch_map['save_infer_model/scale_0']:
            mask = True
            if float(data[1]) <= self.thresholds:
                mask = False
            result.append({
                "mask": mask,
                "score": float(data[1])
            })

        return result