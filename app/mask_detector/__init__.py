from paddle_serving_client import Client
from paddle_serving_app.reader import DetectionSequential, \
    DetectionResize, \
    DetectionNormalize, \
    DetectionTranspose
import numpy as np

class MaskDetector:
    def __init__(self, url= 'mask_detection:9396'):
        self.preprocess = DetectionSequential([
            DetectionResize(
                (128, 128), False, interpolation=2),
            DetectionNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], True),
            DetectionTranspose((2, 0, 1)),
        ])
        self.client = Client()
        self.client.load_client_config("./mask_detector/mask_client/serving_client_conf.prototxt")
        if isinstance(url, str):
            self.client.connect([url])
        if isinstance(url, list):
            self.client.connect(url)

    def predict(self, images):
        ims = []
        for image in images:
            im, _ = self.preprocess(image)
            ims.append(im)
        fetch_map = self.client.predict(
            feed={
                "image": np.array(ims),
            },
            fetch=["save_infer_model/scale_0"],
            batch=True)
        result = []
        for data in fetch_map['save_infer_model/scale_0']:
            mask = True
            if float(data[1]) <= float(data[0]):
                mask = False
            result.append({
                "mask": mask,
                "score": float(data[1])
            })

        return result