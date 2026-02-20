import torch
import torch.nn as nn
import timm
import librosa
import numpy as np
from PIL import Image
from torchvision import transforms

class SpectrogramCNNDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Pretrained EfficientNet
        self.model = timm.create_model("efficientnet_b0", pretrained=True)
        self.model.classifier = nn.Linear(
            self.model.classifier.in_features, 1
        )

        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def audio_to_spectrogram(self, audio_path):
        y, sr = librosa.load(audio_path, sr=16000)

        # Mel Spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_mels=128
        )

        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Normalize 0–255
        mel_spec_db -= mel_spec_db.min()
        mel_spec_db /= mel_spec_db.max()
        mel_spec_db *= 255.0

        mel_spec_db = mel_spec_db.astype(np.uint8)

        # Convert to PIL Image
        image = Image.fromarray(mel_spec_db)

        # Convert grayscale to RGB (3 channels)
        image = image.convert("RGB")

        return image

    def analyze(self, audio_path):

        spec_image = self.audio_to_spectrogram(audio_path)

        img = self.transform(spec_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(img)
            prob = torch.sigmoid(output).item()

        return float(prob)
