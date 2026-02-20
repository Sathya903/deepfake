import cv2
import numpy as np

class TemporalDetector:

    def analyze(self, video_path):

        cap = cv2.VideoCapture(video_path)

        prev_gray = None
        motion_scores = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_gray is not None:
                flow = cv2.calcOpticalFlowFarneback(
                    prev_gray, gray, None,
                    0.5, 3, 15, 3, 5, 1.2, 0
                )

                magnitude = np.mean(np.sqrt(flow[...,0]**2 + flow[...,1]**2))
                motion_scores.append(magnitude)

            prev_gray = gray

        cap.release()

        if not motion_scores:
            return 0.5

        score = np.std(motion_scores)
        score = np.clip(score / 10, 0, 1)

        return float(score)
