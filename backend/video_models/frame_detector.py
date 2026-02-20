import cv2
import numpy as np

class FrameDetector:

    def analyze(self, video_path, image_cnn):
        cap = cv2.VideoCapture(video_path)
        scores = []

        while len(scores) < 20:
            ret, frame = cap.read()
            if not ret:
                break

            temp_path = "temp_frame.jpg"
            cv2.imwrite(temp_path, frame)

            score = image_cnn.predict(temp_path)
            scores.append(score)

        cap.release()

        return sum(scores) / len(scores)
