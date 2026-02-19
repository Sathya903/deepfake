import librosa
import numpy as np

class SpectrogramDetector:

    def analyze(self, audio_path):
        y, sr = librosa.load(audio_path)
        spec = librosa.stft(y)
        magnitude = np.abs(spec)

        score = np.mean(magnitude) / 100
        score = min(score, 1.0)

        return score
