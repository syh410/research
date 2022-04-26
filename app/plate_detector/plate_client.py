import grpc
from .proto import plate_pb2, plate_pb2_grpc
import cv2

class PlateDetectionClient:
    def __init__(self, url = 'plate_detection:50053') -> None:
        channel = grpc.insecure_channel(url)
        self.client = plate_pb2_grpc.PlateServiceStub(channel = channel)
    def predict(self, image):
        image = cv2.imencode('.jpg', image)[1].tobytes()
        request = plate_pb2.PlateRequest(image=image)
        responses = self.client.predict(request)
        data = []
        for response in responses.Plates:
            data.append({
                "score" : float(response.score),
                "rect" : {
                    "left" : float(response.rect.left),
                    "top" : float(response.rect.top),
                    "right" : float(response.rect.right),
                    "bottom" : float(response.rect.bottom)
                },
                "point" : {
                    "topleft" :
                    {
                        "x" : float(response.points.topleft.x),
                        "y" : float(response.points.topleft.y)
                    } ,
                    "topright" :
                    {
                        "x" : float(response.points.topright.x),
                        "y" : float(response.points.topright.y)
                    } ,
                    "bottomleft" :
                    {
                        "x" : float(response.points.bottomleft.x),
                        "y" : float(response.points.bottomleft.y)
                    } ,
                    "bottomright" :
                    {
                        "x" : float(response.points.bottomright.x),
                        "y" : float(response.points.bottomright.y)
                    } ,
                }
            })
        return data