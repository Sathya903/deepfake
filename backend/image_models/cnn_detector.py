import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

class ImageCNNDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.processor = AutoImageProcessor.from_pretrained(
            "prithivMLmods/Deep-Fake-Detector-Model"
        )

        self.model = AutoModelForImageClassification.from_pretrained(
            "prithivMLmods/Deep-Fake-Detector-Model"
        ).to(self.device)

        self.model.eval()

    def predict(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)
        fake_prob = probs[0][1].item()

        return float(fake_prob)
