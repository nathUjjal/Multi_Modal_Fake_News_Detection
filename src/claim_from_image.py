import cv2
import pytesseract
import torch
import re
from transformers import BartTokenizer, BartForConditionalGeneration
from src.claim_from_text import summarize_text

# --------------------------------------------------
# TESSERACT PATH (Windows)
# --------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --------------------------------------------------
# OCR
# --------------------------------------------------
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray, lang="eng")
    return text.strip()

# --------------------------------------------------
# CONDITION-1: TEXT VS NON-TEXT
# --------------------------------------------------
def is_text_image(text):
    if not text:
        return False

    clean = re.sub(r'[^A-Za-z ]', '', text)
    words = clean.split()

    if len(clean) < 40:
        return False
    if len(words) < 6:
        return False

    return True

# --------------------------------------------------
# LOAD BART
# --------------------------------------------------
MODEL_NAME = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

device = torch.device("cpu")
model.to(device)

# --------------------------------------------------
# 20–25 WORD BART SUMMARY
# --------------------------------------------------
def summarize_20_25_words(text):
    inputs = tokenizer(
        text,
        max_length=1024,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=45,
        max_length=70,
        length_penalty=2.0,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    words = summary.split()

    if len(words) > 25:
        summary = " ".join(words[:25])
    elif len(words) < 20:
        summary = " ".join(words[:20])

    return summary

# --------------------------------------------------
# FALLBACK SUMMARY (NON-TEXT IMAGE)
# --------------------------------------------------
def non_text_fallback_summary():
    return (
        "The provided image does not contain readable textual information, "
        "and therefore no meaningful text could be extracted or summarized "
        "from the visual content available."
    )

# --------------------------------------------------
# FULL PIPELINE (ALWAYS RETURNS OUTPUT)
# --------------------------------------------------
def image_to_text_summary(image_path):
    text = extract_text_from_image(image_path)

    if is_text_image(text):
        summary = summarize_text(text)
        status = "text_image"
    else:
        summary = non_text_fallback_summary()
        status = "non_text_image"

    print("\nStatus:", status)
    print("\nSummary:")
    print(summary)
    print("\nWord Count:", len(summary.split()))

    return {
        "status": status,
        "summary": summary
    }

# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    image_to_text_summary("data/image/news2.jpg")
