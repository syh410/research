import grpc
from .protos import face_recognition_pb2_grpc, face_recognition_pb2

def readfile(image):
    with open(image, 'rb') as f:
        return f.read()


class FaceRecognitionClient:
    def __init__(self, url='face_recognition:7552') -> None:
        channel = grpc.insecure_channel(url)
        self.client = face_recognition_pb2_grpc.FaceRecognitionEngineStub(channel)
    
    def search(self, image, repoid):
        request = face_recognition_pb2.SearchRequest()
        request.image = image
        request.repoId = repoid
        reply = self.client.Search(request)
        rtn = reply.rtn
        result = []
        if rtn != 0:
            return rtn, result
        for similarFace in reply.similarFaces:
            result.append({
                "faceId": similarFace.faceId,
                "score": similarFace.score,
            })
        return 0, result
    
    def upload(self, image, faceid, repoid):
        request = face_recognition_pb2.UploadRequest()
        request.image = image
        request.faceId = faceid
        request.repoId = repoid
        reply = self.client.Upload(request)
        return reply.rtn

    def compare(self, image1, image2):
        request = face_recognition_pb2.CompareRequest()
        request.image1 = image1
        request.image2 = image2
        reply = self.client.Compare(request)
        return reply.rtn, reply.score
