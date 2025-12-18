# pipeline.py

import json
from src.claim_from_text import image_to_text_summary
from src.claim_from_image import summarize_text
from src.claim_from_video import extract_claim_from_video

from src.evidence_retrieval import retrieve_evidence
from src.verification import verify_claim
from src.explanation import explain_result


def process_request(payload: dict) -> dict:
    """
    Main entry point of the system.
    Accepts JSON-like dict:
        {
          "type": "text" | "image" | "video",
          "input": "string text or file path"
        }
    """

    modality = payload.get("type")
    user_input = payload.get("input")

    if modality not in ["text", "image", "video"]:
        raise ValueError("Invalid modality. Must be text, image, or video.")

    # --------------------------------------------------
    # STAGE 1 — CLAIM EXTRACTION
    # --------------------------------------------------
    if modality == "text":
        claims = extract_claims_from_text(user_input)

    elif modality == "image":
        claims = extract_claims_from_image(user_input)

    elif modality == "video":
        claims = extract_claims_from_video(user_input)

    # For now we assume one claim per modality
    claim = claims[0]

    # --------------------------------------------------
    # STAGE 2 — EVIDENCE RETRIEVAL
    # --------------------------------------------------
    evidence_list = retrieve_evidence(claim)

    # --------------------------------------------------
    # STAGE 3 — VERIFICATION (Zero-Shot / stance)
    # --------------------------------------------------
    verification = verify_claim(claim, evidence_list)

    verdict = verification["verdict"]
    confidence = verification["confidence"]
    evidence = verification["top_evidence"]

    # --------------------------------------------------
    # STAGE 4 — EXPLANATION
    # --------------------------------------------------
    explained = explain_result(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        evidence=evidence
    )

    # `explained` is JSON string, convert back to dict
    return json.loads(explained)


if __name__ == "__main__":
    # Example tests
    sample_text = {
        "type": "text",
        "input": "WHO approved herbal cure for COVID-19."
    }

    sample_image = {
        "type": "image",
        "input": "sample_image.jpg"
    }

    sample_video = {
        "type": "video",
        "input": "sample_video.mp4"
    }

    # Run pipeline for sample
    print(process_request(sample_text))
