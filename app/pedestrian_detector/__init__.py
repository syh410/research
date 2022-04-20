from paddle_serving_client import Client
from paddle_serving_app.reader import DetectionSequential, \
    DetectionResize, \
    DetectionNormalize, \
    DetectionTranspose

class PedestrianDetector:
    def __init__(self, url= 'pedestrian_detection:9394', thresholds = 0.5):
        self.preprocess = DetectionSequential([
            DetectionResize(
                (608, 608), False, interpolation=2),
            DetectionNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225], True),
            DetectionTranspose((2, 0, 1)),
        ])
        self.client = Client()
        self.thresholds = thresholds
        self.client.load_client_config("./pedestrian_detector/pedestrian_client/serving_client_conf.prototxt")
        if isinstance(url, str):
            self.client.connect([url])
        if isinstance(url, list):
            self.client.connect(url)

    def predict(self, image):
        im, _ = self.preprocess(image)
        fetch_map = self.client.predict(
            feed={
                "@HUB_yolov3_darknet53_pedestrian@image": im,
                "@HUB_yolov3_darknet53_pedestrian@im_size": image.shape[:2],
            },
            fetch=["@HUB_yolov3_darknet53_pedestrian@multiclass_nms.tmp_0"],
            batch=False)
        result = []
        for data in fetch_map["@HUB_yolov3_darknet53_pedestrian@multiclass_nms.tmp_0"]:
            if float(data[1]) <= self.thresholds:
                continue
            result.append({
                "score": float(data[1]),
                "rect":{
                    "left": float(data[2]),
                    "top": float(data[3]),
                    "right": float(data[4]),
                    "bottom": float(data[5])
                }
            })
        return result

