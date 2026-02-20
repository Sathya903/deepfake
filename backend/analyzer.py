import os

from image_models.cnn_detector import ImageCNNDetector
from image_models.frequency_detector import FrequencyDetector

from audio_models.wav2vec_detector import Wav2VecDetector
from audio_models.spectrogram_detector import SpectrogramCNNDetector

from video_models.frame_detector import FrameDetector
from video_models.temporal_detector import TemporalDetector

from fusion.meta_classifier import MetaClassifier


# -------------------------
# Initialize ALL models once
# -------------------------

cnn_detector = ImageCNNDetector()
frequency_detector = FrequencyDetector()

wav2vec_detector = Wav2VecDetector()
spectrogram_detector = SpectrogramCNNDetector()

frame_detector = FrameDetector()
temporal_detector = TemporalDetector()

meta_classifier = MetaClassifier()


# =========================
# IMAGE PIPELINE
# =========================

def analyze_image(image_path):

    cnn_score = cnn_detector.predict(image_path)
    freq_score = frequency_detector.analyze(image_path)

    scores = {
        "CNN Deepfake Model": cnn_score,
        "Frequency Domain Analysis": freq_score
    }

    fusion_result = meta_classifier.fuse(scores)

    return {
        "media_type": "image",
        "decision": fusion_result["decision"],
        "confidence": fusion_result["confidence"],
        "model_breakdown": fusion_result["model_breakdown"]
    }


# =========================
# AUDIO PIPELINE
# =========================

def analyze_audio(audio_path):

    wav2vec_score = wav2vec_detector.analyze(audio_path)
    spec_score = spectrogram_detector.analyze(audio_path)

    scores = {
        "Wav2Vec2 Anti-Spoof Model": wav2vec_score,
        "Spectrogram CNN Model": spec_score
    }

    fusion_result = meta_classifier.fuse(scores)

    return {
        "media_type": "audio",
        "decision": fusion_result["decision"],
        "confidence": fusion_result["confidence"],
        "model_breakdown": fusion_result["model_breakdown"]
    }


# =========================
# VIDEO PIPELINE
# =========================

def analyze_video(video_path):

    frame_score = frame_detector.analyze(video_path, cnn_detector)
    temporal_score = temporal_detector.analyze(video_path)

    scores = {
        "Frame-level CNN Aggregation": frame_score,
        "Temporal Consistency Model": temporal_score
    }

    fusion_result = meta_classifier.fuse(scores)

    return {
        "media_type": "video",
        "decision": fusion_result["decision"],
        "confidence": fusion_result["confidence"],
        "model_breakdown": fusion_result["model_breakdown"]
    }


# =========================
# AUTO MEDIA ROUTER
# =========================

def analyze_media(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    image_ext = [".jpg", ".jpeg", ".png"]
    audio_ext = [".wav", ".mp3", ".ogg", ".m4a", ".flac"]
    video_ext = [".mp4", ".avi", ".mov", ".mkv"]

    if ext in image_ext:
        return analyze_image(file_path)

    elif ext in audio_ext:
        return analyze_audio(file_path)

    elif ext in video_ext:
        return analyze_video(file_path)

    else:
        return {
            "error": "Unsupported file type"
        }
