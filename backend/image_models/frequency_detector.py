import cv2
import numpy as np

class FrequencyDetector:

    def analyze(self, image_path):
        img = cv2.imread(image_path, 0)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude = 20 * np.log(np.abs(fshift) + 1)

        score = np.mean(magnitude) / 100
        score = min(score, 1.0)

        return float(score)
