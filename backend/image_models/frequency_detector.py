import cv2
import numpy as np

class FrequencyDetector:

    def analyze(self, image_path):
        img = cv2.imread(image_path, 0)

        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude = np.log(np.abs(fshift) + 1)

        mean_val = np.mean(magnitude)

        score = mean_val / np.max(magnitude)
        score = np.clip(score, 0, 1)

        return float(score)
