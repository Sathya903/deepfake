from image_models.cnn_detector import ImageCNNDetector
from image_models.frequency_detector import FrequencyDetector
from image_models.face_landmark_detector import FaceLandmarkDetector

from video_models.frame_detector import FrameDetector
from video_models.temporal_detector import TemporalDetector

from audio_models.spectrogram_detector import SpectrogramCNNDetector
from audio_models.mfcc_detector import MFCCDetector

from fusion.meta_classifier import MetaClassifier

import cv2


class MultiModalEngine:

    def __init__(self):

        # Image models
        self.cnn = ImageCNNDetector()
        self.freq = FrequencyDetector()
        self.landmark = FaceLandmarkDetector()

        # Video models
        self.frame_model = FrameDetector()
        self.temporal_model = TemporalDetector()

        # Audio models
        self.spec_model = SpectrogramCNNDetector()
        self.mfcc_model = MFCCDetector()

        self.meta = MetaClassifier()

    # -------------------------
    # IMAGE
    # -------------------------
    def process_image(self, image_path):
        cnn_score = self.cnn.predict(image_path)
        freq_score = self.freq.analyze(image_path)
        landmark_score = self.landmark.analyze(image_path)

        scores = {
            "cnn": cnn_score,
            "frequency": freq_score,
            "landmark": landmark_score
        }

        fused_score = self.meta.fuse(scores)

        return {
            "cnn": cnn_score,
            "frequency": freq_score,
            "landmark": landmark_score,
            "fused": fused_score
        }


    # -------------------------
    # VIDEO
    # -------------------------
    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_scores = []
        while len(frames) < 5:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            frame_scores.append(self.frame_model.analyze_frame(frame))
        cap.release()

        temporal_score = self.temporal_model.analyze_sequence(frames)

        frame_avg = sum(frame_scores) / len(frame_scores) if frame_scores else 0

        scores = {
            "frame_model": frame_avg,
            "temporal_model": temporal_score
        }

        fused_score = self.meta.fuse(scores)
        return {
            "cnn": frame_avg,            # mapped to compression
            "frequency": temporal_score, # mapped to lighting
            "landmark": temporal_score,  # reuse if needed
            "fused": fused_score
        }


    # -------------------------
    # AUDIO
    # -------------------------
    def process_audio(self, audio_path):

        spec_score = self.spec_model.analyze(audio_path)
        mfcc_score = self.mfcc_model.analyze(audio_path)

        scores = {
            "spectrogram": spec_score,
            "mfcc": mfcc_score
        }
 
        fused_score = self.meta.fuse(scores)

        return {
            "cnn": spec_score,
            "frequency": mfcc_score,
            "landmark": mfcc_score,
            "fused": fused_score
        }

