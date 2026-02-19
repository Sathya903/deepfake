from facenet_pytorch import MTCNN
from PIL import Image

class FaceLandmarkDetector:

    def __init__(self):
        self.mtcnn = MTCNN(keep_all=True)

    def analyze(self, image_path):
        image = Image.open(image_path).convert("RGB")
        boxes, _ = self.mtcnn.detect(image)

        if boxes is None:
            return 0.8  # suspicious if no face

        return 0.2  # face detected normally
