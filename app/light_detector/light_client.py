import cv2
from .proto import light_pb2_grpc, light_pb2
import grpc
import numpy as np

class LightDetectionClient:
    def __init__(self, url = 'light_detection:50052') -> None:
        channel = grpc.insecure_channel(url)
        self.client = light_pb2_grpc.LightServiceStub(channel=channel)
    def predict(self, image):
        image = cv2.imencode('.jpg', image)[1].tobytes()
        request = light_pb2.LightRequest(images = [image])
        responses = self.client.predict(request)
        data = []
        for response in responses.responses:
            for light in response.lights:
                data.append({
                    "score": float(light.score),
                    "rect":{
                        "left": float(light.rect.left),
                        "top": float(light.rect.top),
                        "right": float(light.rect.right),
                        "bottom": float(light.rect.bottom)
                    }
                })
        return data



# if __name__ == "__main__":
#     with open("./light.jpg", "rb") as f:
#         image = f.read()
#     conn = grpc.insecure_channel('localhost:50052')
#     client = light_pb2_grpc.LightServiceStub(channel=conn)
#     request = light_pb2.LightRequest(images=[image])
#     response = client.predict(request)
#     print(response)
