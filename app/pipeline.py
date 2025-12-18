# pipeline.py
import json

from src.claim_from_text import summarize_text
from src.claim_from_image import image_to_text_summary
from src.claim_from_video import extract_claim_from_video

from src.evidence_retrieval import retrieve_evidence
from src.verification import verify_claim
from src.explanation import explain_result


def process_request(payload: dict) -> dict:
    modality = payload.get("type")
    user_input = payload.get("input")

    if modality not in ["text", "image", "video"]:
        raise ValueError("Invalid modality. Must be text, image, or video.")

    # ---------------------------
    # STAGE 1 — CLAIM EXTRACTION
    # ---------------------------
    if modality == "text":
        # summarize_text returns a single string
        claim = summarize_text(user_input)

    elif modality == "image":
        # image_to_text_summary returns a dict with a 'summary' field
        img_out = image_to_text_summary(user_input)
        claim = img_out.get("summary", "")

    elif modality == "video":
        # extract_claim_from_video returns a dict
        vid_out = extract_claim_from_video(user_input)
        if vid_out.get("status") == "success":
            claim = vid_out.get("extracted_claim", "")
        else:
            return {
                "claim": "",
                "verdict": "Error",
                "confidence": 0.0,
                "explanation": vid_out.get("reason", "Failed to extract claim from video")
            }

    if not claim:
        return {
            "claim": "",
            "verdict": "Error",
            "confidence": 0.0,
            "explanation": "Failed to extract a claim from the provided input"
        }

    # ---------------------------
    # STAGE 2 — EVIDENCE
    # ---------------------------
    evidence_resp = retrieve_evidence(claim)
    evidence_items = evidence_resp.get("evidence", [])
    evidence_texts = [e.get("text", "") for e in evidence_items]

    # ---------------------------
    # STAGE 3 — VERIFICATION
    # ---------------------------
    verification = verify_claim(claim, evidence_texts)

    verdict = verification.get("verdict", "⚠️ Uncertain")
    confidence = verification.get("confidence_score", 0.0)

    top_evidence_text = evidence_items[0]["text"] if evidence_items else ""

    # ---------------------------
    # STAGE 4 — EXPLANATION
    # ---------------------------
    explained = explain_result(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        evidence=top_evidence_text
    )

    return json.loads(explained)
