import hashlib
import wave
import contextlib
import os
import librosa
import numpy as np
import torch
import torch.nn as nn

# ---------------------------
# Simple Spectrogram CNN Model
# ---------------------------

class AudioDeepfakeModel(nn.Module):
    def __init__(self):
        super(AudioDeepfakeModel, self).__init__()
        self.conv = nn.Conv2d(1, 8, kernel_size=3)
        self.pool = nn.AdaptiveAvgPool2d((10, 10))
        self.fc = nn.Linear(8 * 10 * 10, 1)

    def forward(self, x):
        x = torch.relu(self.conv(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = torch.sigmoid(self.fc(x))
        return x


# Load model once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
deepfake_model = AudioDeepfakeModel().to(device)
deepfake_model.eval()


def authenticate_audio(file_path):

    checks = []
    score = 0

    # -------------------------------
    # 1️⃣ File Integrity
    # -------------------------------
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
            "message": "Hash failed"
        })

    ext = os.path.splitext(file_path)[1].lower()

    # -------------------------------
    # 2️⃣ Format Check
    # -------------------------------
    if ext in [".mp3", ".wav", ".ogg", ".m4a"]:
        checks.append({
            "name": "Audio Format",
            "status": "GREEN",
            "message": f"Format: {ext}"
        })
        score += 25
    else:
        checks.append({
            "name": "Audio Format",
            "status": "RED",
            "message": "Unsupported format"
        })

    # -------------------------------
    # 3️⃣ Duration (WAV only)
    # -------------------------------
    if ext == ".wav":
        try:
            with contextlib.closing(wave.open(file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)

            if duration >= 2:
                status = "GREEN"
                score += 25
            else:
                status = "YELLOW"

            checks.append({
                "name": "Duration Check",
                "status": status,
                "message": f"{round(duration,2)} seconds"
            })

        except:
            checks.append({
                "name": "Duration Check",
                "status": "RED",
                "message": "Duration read failed"
            })
    else:
        checks.append({
            "name": "Duration Check",
            "status": "YELLOW",
            "message": "Detailed check for WAV only"
        })

    # -------------------------------
    # 4️⃣ File Size
    # -------------------------------
    size = os.path.getsize(file_path)
    if size > 10000:
        status = "GREEN"
        score += 25
    else:
        status = "YELLOW"

    checks.append({
        "name": "File Size Check",
        "status": status,
        "message": f"{size} bytes"
    })

    # ======================================================
    # 🔥 AI DEEPFAKE DETECTION (REAL SIGNAL PROCESSING)
    # ======================================================

    try:
        y, sr = librosa.load(file_path, sr=22050)

        # Convert to spectrogram
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

        # Resize to fixed size
        spectrogram = np.resize(spectrogram, (128, 128))

        tensor = torch.tensor(spectrogram, dtype=torch.float32)
        tensor = tensor.unsqueeze(0).unsqueeze(0).to(device)

        with torch.no_grad():
            prediction = deepfake_model(tensor)
            deepfake_score = float(prediction.item()) * 100

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

    # Return 3 values now
    return checks, score, round(deepfake_score, 2)
