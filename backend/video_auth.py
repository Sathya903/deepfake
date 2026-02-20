import hashlib
import cv2
from multimodal_engine import MultiModalEngine


def authenticate_video(file_path):

    checks = []
    score = 0
    deepfake_score = 0

    # -------------------------
    # 1️⃣ File Integrity
    # -------------------------
    try:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        checks.append({
            "name": "File Integrity",
            "status": "GREEN",
            "message": "Hash generated successfully"
        })
        score += 25
    except Exception as e:
        checks.append({
            "name": "File Integrity",
            "status": "RED",
            "message": "Hash failed"
        })

    # -------------------------
    # 2️⃣ Open Video
    # -------------------------
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        checks.append({
            "name": "Video Structure",
            "status": "RED",
            "message": "Cannot open video"
        })
        return checks, score, deepfake_score

    # -------------------------
    # 3️⃣ Frame Count
    # -------------------------
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count > 10:
        status = "GREEN"
        score += 25
    else:
        status = "YELLOW"

    checks.append({
        "name": "Frame Count",
        "status": status,
        "message": f"{frame_count} frames"
    })

    # -------------------------
    # 4️⃣ FPS
    # -------------------------
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps >= 15:
        status = "GREEN"
        score += 25
    else:
        status = "YELLOW"

    checks.append({
        "name": "FPS Check",
        "status": status,
        "message": f"{fps:.2f} FPS"
    })

    # -------------------------
    # 5️⃣ Resolution
    # -------------------------
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if width >= 640:
        status = "GREEN"
        score += 25
    else:
        status = "YELLOW"

    checks.append({
        "name": "Resolution Check",
        "status": status,
        "message": f"{int(width)}x{int(height)}"
    })

    # -------------------------
    # 6️⃣ Deepfake Detection (Frame Sampling)
    # -------------------------
    engine = MultiModalEngine()

    sample_scores = []
    sample_interval = max(1, frame_count // 5)  # sample 5 frames

    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % sample_interval == 0:
            temp_frame_path = "temp_frame.jpg"
            cv2.imwrite(temp_frame_path, frame)

            result = engine.process_image(temp_frame_path)
            sample_scores.append(result.get("confidence", 0))

        current_frame += 1

    cap.release()

    if sample_scores:
        deepfake_score = round(sum(sample_scores) / len(sample_scores), 2)

    checks.append({
        "name": "AI Deepfake Risk",
        "status": "RED" if deepfake_score > 60 else "GREEN",
        "message": f"{deepfake_score}%"
    })

    return checks, score, deepfake_score
