from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.pipeline import process_request

app = FastAPI(title="Multimodal Fake News Detection API")

# CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------
# TEXT API
# ---------------------------
@app.post("/analyze/text")
async def analyze_text(text: str = Form(...)):
    payload = {
        "type": "text",
        "input": text
    }
    return process_request(payload)


# ---------------------------
# IMAGE API
# ---------------------------
@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    payload = {
        "type": "image",
        "input": file_path
    }
    return process_request(payload)


# ---------------------------
# VIDEO API
# ---------------------------
@app.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    payload = {
        "type": "video",
        "input": file_path
    }
    return process_request(payload)
