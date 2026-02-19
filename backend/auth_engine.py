from utils import detect_media_type
from image_auth import authenticate_image
from video_auth import authenticate_video
from audio_auth import authenticate_audio


def calculate_final_status(score):
    """
    Convert score into authenticity level
    """
    if score >= 60:
        return "HIGH AUTHENTICITY"
    elif score >= 40:
        return "MODERATE AUTHENTICITY"
    else:
        return "LOW AUTHENTICITY"


def calculate_deepfake_risk(deepfake_score):
    """
    Convert deepfake score into readable level
    """
    if deepfake_score >= 70:
        return "HIGH DEEPFAKE RISK"
    elif deepfake_score >= 40:
        return "MODERATE DEEPFAKE RISK"
    else:
        return "LOW DEEPFAKE RISK"


def authenticate_media(file_path):

    media_type = detect_media_type(file_path)

    if media_type == "image":
        checks, score, deepfake_score = authenticate_image(file_path)

    elif media_type == "video":
        checks, score, deepfake_score = authenticate_video(file_path)

    elif media_type == "audio":
        checks, score, deepfake_score = authenticate_audio(file_path)

    else:
        return {
            "error": "Unsupported media type"
        }

    final_status = calculate_final_status(score)
    deepfake_status = calculate_deepfake_risk(deepfake_score)

    result = {
        "media_type": media_type,
        "total_auth_score": score,
        "authenticity_level": final_status,
        "deepfake_score": deepfake_score,
        "deepfake_risk": deepfake_status,
        "checks": checks
    }

    return result
