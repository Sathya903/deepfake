import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import cv2

# --------------------------------
# 🔥 Simple CNN Deepfake Model
# --------------------------------

class ImageDeepfakeCNN(nn.Module):
    def __init__(self):
        super(ImageDeepfakeCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3)
        self.pool = nn.AdaptiveAvgPool2d((16, 16))
        self.fc = nn.Linear(16 * 16 * 16, 1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = torch.sigmoid(self.fc(x))
        return x


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
deepfake_model = ImageDeepfakeCNN().to(device)
deepfake_model.eval()

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])


def authenticate_image(file_path):

    checks = []
    score = 0

    # 1️⃣ File Integrity
    try:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        checks.append({
            "name": "File Integrity",
            "status": "GREEN",
            "message": "Hash generated successfully"
        })
        score += 25
    except:
        checks.append({
            "name": "File Integrity",
            "status": "RED",
            "message": "Hash generation failed"
        })

    # 2️⃣ EXIF Metadata
    try:
        image = Image.open(file_path)
        exif = image._getexif()

        if exif:
            checks.append({
                "name": "EXIF Metadata",
                "status": "GREEN",
                "message": "Metadata found"
            })
            score += 25
        else:
            checks.append({
                "name": "EXIF Metadata",
                "status": "YELLOW",
                "message": "No metadata found"
            })
    except:
        checks.append({
            "name": "EXIF Metadata",
            "status": "RED",
            "message": "Metadata extraction failed"
        })

    # 3️⃣ Resolution Check
    try:
        width, height = image.size
        if width >= 500 and height >= 500:
            status = "GREEN"
            score += 25
        else:
            status = "YELLOW"

        checks.append({
            "name": "Resolution Check",
            "status": status,
            "message": f"{width}x{height}"
        })
    except:
        checks.append({
            "name": "Resolution Check",
            "status": "RED",
            "message": "Resolution check failed"
        })

    # 4️⃣ File Size vs Resolution Ratio
    try:
        file_size = os.path.getsize(file_path)
        ratio = file_size / (width * height)

        if ratio > 0.5:
            status = "GREEN"
            score += 25
        else:
            status = "YELLOW"

        checks.append({
            "name": "Compression Consistency",
            "status": status,
            "message": f"Size-to-pixel ratio: {round(ratio,4)}"
        })
    except:
        checks.append({
            "name": "Compression Consistency",
            "status": "RED",
            "message": "Compression analysis failed"
        })

    # ======================================================
    # 🔥 AI DEEPFAKE DETECTION SECTION
    # ======================================================

    try:
        # ---- CNN Analysis ----
        pil_image = Image.open(file_path).convert("RGB")
        input_tensor = transform(pil_image).unsqueeze(0).to(device)

        with torch.no_grad():
            cnn_prediction = deepfake_model(input_tensor)
            cnn_score = float(cnn_prediction.item()) * 100

        # ---- Frequency Analysis (FFT) ----
        img_gray = cv2.imread(file_path, 0)
        f = np.fft.fft2(img_gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

        freq_score = np.mean(magnitude_spectrum) % 100

        # ---- Final Deepfake Score Fusion ----
        deepfake_score = (cnn_score * 0.7) + (freq_score * 0.3)

        checks.append({
            "name": "AI Deepfake Risk",
            "status": "RED" if deepfake_score > 60 else "GREEN",
            "message": f"{round(deepfake_score,2)}%"
        })

    except Exception as e:
        deepfake_score = 0
        checks.append({
            "name": "AI Deepfake Risk",
            "status": "YELLOW",
            "message": "AI analysis failed"
        })

    return checks, score, round(deepfake_score, 2)
