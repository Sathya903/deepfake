import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image

class CNNDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Pretrained EfficientNet
        self.model = timm.create_model("efficientnet_b0", pretrained=True)
        self.model.classifier = nn.Linear(self.model.classifier.in_features, 1)
        
        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def predict(self, image_path):
        image = Image.open(image_path).convert("RGB")
        img = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(img)
            prob = torch.sigmoid(output).item()

        return float(prob)
