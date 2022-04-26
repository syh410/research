import cv2
import numpy as np
import grpc
from .proto import lprnet_pb2, lprnet_pb2_grpc

image_size = (94, 24)

class LprnetDetectionClient:
    def __init__(self, url = 'lprnet_detection:50054') -> None:
        channel = grpc.insecure_channel(url)
        self.client = lprnet_pb2_grpc.LprnetServiceStub(channel = channel)
    def predict(self, images):
        img = []
        for image in images:
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_CUBIC)
            image = image.astype("float32")
            image -= 127.5
            image *= 0.0078125
            img.append(np.ndarray.tobytes(np.transpose(image, (2, 0, 1))))
        request = lprnet_pb2.LprnetRequest(images=img)
        responses = self.client.predict(request)
        data = []
        for label in responses.labels:
            data.append(label)
        return data