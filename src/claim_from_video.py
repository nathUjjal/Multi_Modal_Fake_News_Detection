# -----------------------------
# SYSTEM SETUP (MUST BE FIRST)
# -----------------------------
import os
import uuid
import shutil
import json

# Ensure ffmpeg is visible to Whisper (adjust path if needed)
FFMPEG_PATH = r"C:\ffmpeg\bin"
if FFMPEG_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# Optional sanity check (comment out after first run)
assert shutil.which("ffmpeg"), "FFmpeg not found in PATH"

# -----------------------------
# IMPORTS
# -----------------------------
import whisper
import nltk
import re

from moviepy.video.io.VideoFileClip import VideoFileClip
from transformers import pipeline

nltk.download("punkt", quiet=True)

# -----------------------------
# CONFIGURATION
# -----------------------------
WHISPER_MODEL_SIZE = "base"     # base / small / medium
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"

# -----------------------------
# LOAD MODELS (ONCE)
# -----------------------------
whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)

summarizer = pipeline(
    "summarization",
    model=SUMMARIZATION_MODEL,
    device=-1  # CPU
)

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def extract_audio_from_video(video_path):
    """Extract audio from video using MoviePy"""
    audio_path = f"temp_audio_{uuid.uuid4().hex}.wav"

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

    return audio_path


def clean_transcript(text):
    """Normalize transcript text"""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9., ]", "", text)
    return text.strip()


def summarize_to_claim(text, max_length=40):
    """Summarize transcript into a concise factual claim"""
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=15,
        do_sample=False
    )[0]["summary_text"]

    return summary.strip()


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def extract_claim_from_video(video_path):
    """
    Extracts a meaningful factual claim from a video.
    Returns a structured dictionary.
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found.")

    # Step 1: Audio extraction
    audio_path = extract_audio_from_video(video_path)

    # Step 2: Speech-to-text (Whisper)
    transcription = whisper_model.transcribe(audio_path)
    raw_transcript = transcription["text"]

    # Cleanup temp audio
    os.remove(audio_path)

    # Step 3: Clean transcript
    cleaned_transcript = clean_transcript(raw_transcript)

    if len(cleaned_transcript.split()) < 20:
        return {
            "status": "failed",
            "reason": "Insufficient spoken content",
            "raw_transcript": raw_transcript
        }

    # Step 4: Claim extraction
    extracted_claim = summarize_to_claim(cleaned_transcript)

    # Step 5: Structured output
    return {
        "status": "success",
        "input_type": "video",
        "extracted_claim": extracted_claim,
        "transcript_snippet": cleaned_transcript[:300],
        "confidence_hint": "medium",
        "ready_for_evidence_search": True
    }


# -----------------------------
# DEMO RUN
# -----------------------------
if __name__ == "__main__":
    video_path = "input.mp4"  # change to your video file

    result = extract_claim_from_video(video_path)
    print(json.dumps(result, indent=4, ensure_ascii=False))