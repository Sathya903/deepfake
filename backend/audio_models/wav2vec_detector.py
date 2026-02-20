import torch
import librosa
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification


class Wav2VecDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
            "superb/wav2vec2-base-superb-ks"
        )

        self.model = AutoModelForAudioClassification.from_pretrained(
            "superb/wav2vec2-base-superb-ks"
        ).to(self.device)

        self.model.eval()

    def analyze(self, audio_path):

        # ✅ Load audio safely (NO torchaudio, NO torchcodec)
        waveform, sr = librosa.load(audio_path, sr=16000)

        # Convert to torch tensor
        waveform = torch.tensor(waveform)

        inputs = self.feature_extractor(
            waveform.numpy(),
            sampling_rate=16000,
            return_tensors="pt",
            padding=True
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.softmax(logits, dim=1)
        score = probs.max().item()

        return float(score)