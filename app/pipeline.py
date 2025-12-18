# pipeline.py
import json

from src.claim_from_text import extract_claims_from_text
from src.claim_from_image import extract_claims_from_image
from src.claim_from_video import extract_claims_from_video

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
        claims = extract_claims_from_text(user_input)

    elif modality == "image":
        claims = extract_claims_from_image(user_input)

    elif modality == "video":
        claims = extract_claims_from_video(user_input)

    claim = claims[0]

    # ---------------------------
    # STAGE 2 — EVIDENCE
    # ---------------------------
    evidence_list = retrieve_evidence(claim)

    # ---------------------------
    # STAGE 3 — VERIFICATION
    # ---------------------------
    verification = verify_claim(claim, evidence_list)

    verdict = verification["verdict"]
    confidence = verification["confidence"]
    evidence = verification["top_evidence"]

    # ---------------------------
    # STAGE 4 — EXPLANATION
    # ---------------------------
    explained = explain_result(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        evidence=evidence
    )

    return json.loads(explained)
