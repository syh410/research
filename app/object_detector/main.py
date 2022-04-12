import torch
from .detectron2.demo.object_detection import ObjectDetection
from .typename import TypeName
import cv2

import os

class ObjectDetector:

    def __init__(self,         
        config_file = None,
        model_file = None,
        opts = [],
        threshold = 0.8):
        if not config_file:
            path = os.path.dirname(__file__)
            config_file = path + "/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        if not model_file:
            path = os.path.dirname(__file__)
            model_file = path + "/detectron2/demo/models/mask_rcnn_R_50_FPN_3x.pkl"
        self.objectdetection = ObjectDetection(
            config_file=config_file,
            model_file=model_file,
            opts=opts,
            confidence_threshold=threshold
        )
    
    def detection(self, image):
        predictions, visualized_output = self.objectdetection.inference(image)
        if len(predictions["instances"]) == 0:
            return []
        classes = predictions["instances"].pred_classes
        boxes = predictions["instances"].pred_boxes
        scores = predictions["instances"].scores
        result = []
        for i, box in enumerate(boxes):        
            result.append({
                "type": TypeName(classes[i].item()).name,
                "rect": {
                    "left": float(box[0].item()),
                    "right": float(box[2].item()),
                    "top": float(box[1].item()),
                    "bottom": float(box[3].item()),
                },
                "score": float(scores[i].item())
            })
        return result

# def main():
#     image = cv2.imread("./detectron2/demo/image/dog.jpg")
#     objectDetector = ObjectDetector()
#     objectDetector.detection(image) 

# if __name__ == "__main__":
#     main()