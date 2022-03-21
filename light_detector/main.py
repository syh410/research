from statistics import mode
import torch
from yolox.tools.demo import Predictor
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
import os

class LightDetector:

    def __init__(self, model_file=None, use_gpu=True, threshold=0.6):
        path = os.path.dirname(__file__)
        exp = get_exp(path + "/light_YOLOX/exps/example/custom/yolox_s.py")
        exp.test_conf = threshold
        if not model_file:
            model_file = path + "/light.pth"
        ckpt = torch.load(model_file, map_location="cpu")
        model = exp.get_model()
        if use_gpu:
            model.cuda()
        model.eval()
        model.load_state_dict(ckpt["model"])
        self.predictor = Predictor(
            model=model,
            exp=exp,
            cls_names=COCO_CLASSES,
            device="gpu" if use_gpu else "cpu"
        )
    
    def detection(self, image):
        output, img_info = self.predictor.inference(image)
        if output[0] is None:
            return []
        output = output[0].cpu()
        bboxes = output[:, 0:4]
        bboxes /= img_info["ratio"]
        result = []
        for item in output:
            result.append({
                "rect": {
                    "left": float(item[0]),
                    "right": float(item[2]),
                    "top": float(item[1]),
                    "bottom": float(item[3]),
                },
                "score": float(item[4] * item[5])
            })
        return result