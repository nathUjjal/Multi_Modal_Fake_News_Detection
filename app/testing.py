from src.datafusionandexplanation import fuse_and_explain
from src.trans import verify_claim

text_result = {
    "modality": "text",
    "claim": "WHO approved herbal cure for COVID-19.",
    "verdict": "Fake",
    "confidence": 0.25,
    "evidence": ["WHO has not approved any herbal cure for COVID-19."]
  }

image_result = {
    "modality": "image",
    "claim": "WHO approved herbal cure for COVID-19.",
    "verdict": "Fake",
    "confidence": 0.35,
    "evidence": ["Official sources show WHO denied herbal cure claims."]
}

video_result = {
    "modality": "video",
    "claim": "WHO approved herbal cure for COVID-19.",
    "verdict": "Uncertain",
    "confidence": 0.55,
    "evidence": ["No official WHO announcement found."]
}
claim = "Gemini is a large language model created by Google."
evidences = [
    "Google's latest AI is a multimodal model called Gemini.",
    "The Eiffel Tower is in Paris, France.",
    "According to official sources, Google developed the Gemini family of models."
]
def run_nlp(text):
    # claim=extract_claim_from_text(text)
    # evidence=retrieve_evidence(claim)
    
    result=verify_claim(claim, evidences)
    final=fuse_and_explain(result)