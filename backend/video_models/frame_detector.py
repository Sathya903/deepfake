import cv2

class FrameDetector:

    def analyze(self, video_path, image_cnn):
        cap = cv2.VideoCapture(video_path)
        scores = []

        count = 0
        while cap.isOpened() and count < 10:
            ret, frame = cap.read()
            if not ret:
                break

            # Save temporary frame
            temp_path = "temp.jpg"
            cv2.imwrite(temp_path, frame)

            score = image_cnn.predict(temp_path)
            scores.append(score)
            count += 1

        cap.release()

        return sum(scores) / len(scores)
