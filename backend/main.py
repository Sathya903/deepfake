
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import UploadFile, File
import shutil
import uuid
from dotenv import load_dotenv
import os
load_dotenv()
from security.encryption import save_encrypted_file,load_encrypted_file
from auth_engine import authenticate_media
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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_bytes = await file.read()

    ext = os.path.splitext(file.filename)[1]
    unique_name = str(uuid.uuid4()) + ext
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    save_encrypted_file(file_bytes, file_path)

    return {"message": "File saved securely"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Step 1: Read uploaded file
    file_bytes = await file.read()

    ext = os.path.splitext(file.filename)[1]
    unique_name = str(uuid.uuid4()) + ext
    encrypted_path = os.path.join(UPLOAD_FOLDER, unique_name)

    # Step 2: Save encrypted
    save_encrypted_file(file_bytes, encrypted_path)

    # Step 3: Decrypt for model processing
    decrypted_data =load_encrypted_file(encrypted_path)

    temp_path = os.path.join(UPLOAD_FOLDER, "temp_" + unique_name)

    with open(temp_path, "wb") as f:
        f.write(decrypted_data)

    # Step 4: Send to model
    result = analyze_media(temp_path)  # or your model function

    os.remove(temp_path)

    return {"result": result}

# -------------------------
# AUTHENTICATION API
# -------------------------

@app.post("/authenticate")
async def authenticate(file: UploadFile = File(...)):

    ext = os.path.splitext(file.filename)[1]
    unique_name = str(uuid.uuid4()) + ext
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    file_bytes = await file.read()
    save_encrypted_file(file_bytes, file_path)

    last_uploaded_file["path"] = file_path

    decrypted_data =load_encrypted_file(file_path)

    temp_path = os.path.join(UPLOAD_FOLDER, "temp_" + unique_name)

    with open(temp_path, "wb") as f:
        f.write(decrypted_data)

    result = authenticate_media(temp_path)

    os.remove(temp_path)

    return result

    



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
    decrypted_data = load_encrypted_file(file_path)

    name, ext = os.path.splitext(file_path)
    temp_path = name + "_temp" + ext
    with open(temp_path, "wb") as f:
        f.write(decrypted_data)

    result = analyze_media(temp_path)
    os.remove(temp_path)

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