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
from analyzer import analyze_media
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

    # Decide authenticity level based on deepfake risk
    if score <= 30:
        authenticity_level = "Likely Deepfake"
    elif score <= 60:
        authenticity_level = "Suspicious"
    else:
        authenticity_level = "Authentic"

    total_score = score


    return {
        "checks": checks,
        "authenticity_level": authenticity_level,
        "total_score": deepfake_score
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

    # 🔥 Call new analyzer
    result = analyze_media(file_path)

    if "error" in result:
        return result

    processing_time = round(time.time() - start_time, 2)
    file_size = round(os.path.getsize(file_path) / (1024 * 1024), 2)

    

    return {
        "media_type": result["media_type"],
        "status": result["decision"].lower(),  # fake / real
        "confidence": result["confidence"],    # 0–100
        "risk": result["confidence"],          # same as fake probability
        "model_breakdown": result["model_breakdown"],
        "processing_time": processing_time,
        "file_size": file_size
    }