from src.datafusionandexplanation import fuse_and_explain

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
print(fuse_and_explain([text_result,image_result,video_result]))
