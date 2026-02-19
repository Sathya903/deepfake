import os
import mimetypes


def detect_media_type(file_path):

    if not os.path.exists(file_path):
        return "unknown"

    ext = os.path.splitext(file_path)[1].lower().strip()

    # Primary detection via extension
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return "image"

    elif ext in [".mp4", ".avi", ".mov", ".webm"]:
        return "video"

    elif ext in [".mp3", ".wav", ".ogg", ".m4a"]:
        return "audio"

    # Fallback detection via MIME type
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        if mime_type.startswith("image"):
            return "image"
        elif mime_type.startswith("video"):
            return "video"
        elif mime_type.startswith("audio"):
            return "audio"

    return "unknown"
