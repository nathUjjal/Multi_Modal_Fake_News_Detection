from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from pipeline import process_request

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

@app.post("/analyze/link")
async def analyze_link(url: str = Form(...)):
    # 1. Scrape text from URL
    scraped_text = scrape_article(url)

    if not scraped_text:
        return {
            "claim": "",
            "verdict": "Error",
            "confidence": 0.0,
            "explanation": "Failed to scrape text from URL"
        }

    # 2. Forward to claim_from_text
    result = extract_claims_from_text(scraped_text)

    return result

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
