from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import shutil
import uuid

from image_auth import authenticate_image
from multimodal_engine import MultiModalEngine
from utils import detect_media_type

app = FastAPI()

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_HTML = os.path.join(BASE_DIR, "../frontend/html")
FRONTEND_STATIC = os.path.join(BASE_DIR, "../frontend/static")
app.mount("/static", StaticFiles(directory=FRONTEND_STATIC), name="static")


UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount CSS + JS as static
app.mount("/static", StaticFiles(directory=FRONTEND_STATIC), name="static")

# Templates
templates = Jinja2Templates(directory=FRONTEND_HTML)

last_uploaded_file = {"path": None}

# -------------------------
# PAGE ROUTES
# -------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/page2", response_class=HTMLResponse)
async def page2(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})


@app.get("/page3", response_class=HTMLResponse)
async def page3(request: Request):
    return templates.TemplateResponse("page3.html", {"request": request})


@app.get("/page4", response_class=HTMLResponse)
async def page4(request: Request):
    return templates.TemplateResponse("page4.html", {"request": request})


@app.get("/page5", response_class=HTMLResponse)
async def page5(request: Request):
    return templates.TemplateResponse("page5.html", {"request": request})


# -------------------------
# AUTHENTICATION API
# -------------------------

@app.post("/authenticate")
async def authenticate(file: UploadFile = File(...)):

    ext = os.path.splitext(file.filename)[1]
    unique_name = str(uuid.uuid4()) + ext
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    last_uploaded_file["path"] = file_path

    checks, score, deepfake_score = authenticate_image(file_path)

    return {
        "checks": checks,
        "authenticity_score": score,
        "deepfake_risk": deepfake_score
    }


# -------------------------
# DEEPFAKE API
# -------------------------



@app.post("/deepfake")
async def deepfake():

    start_time = time.time()

    file_path = last_uploaded_file["path"]

    if not file_path:
        return {"error": "No file uploaded"}

    engine = MultiModalEngine()
    media_type = detect_media_type(file_path)

    if media_type == "image":
        raw_result = engine.process_image(file_path)
    elif media_type == "video":
        raw_result = engine.process_video(file_path)
    elif media_type == "audio":
        raw_result = engine.process_audio(file_path)
    else:
        return {"error": "Unsupported type"}

    """
    EXPECTED raw_result format from engine:
    {
        "cnn": 0.72,
        "frequency": 0.65,
        "landmark": 0.81
    }
    """

    # Safe extraction
    cnn_score = raw_result.get("cnn", 0)
    freq_score = raw_result.get("frequency", 0)
    landmark_score = raw_result.get("landmark", 0)

    # Calculate deepfake probability
    deepfake_probability = (cnn_score + freq_score + landmark_score) / 3

    confidence_score = 1 - deepfake_probability
    risk_score = deepfake_probability

    processing_time = round(time.time() - start_time, 2)
    file_size = round(os.path.getsize(file_path) / (1024 * 1024), 2)

    status = "deepfake" if deepfake_probability > 0.5 else "authentic"

    return {
        "status": status,
        "confidence": round(confidence_score * 100),
        "risk": round(risk_score * 100),
        "metrics": {
            "facial": round(landmark_score * 100),
            "lighting": round(freq_score * 100),
            "compression": round(cnn_score * 100)
        },
        "processing_time": processing_time,
        "file_size": file_size
    }

