# 🧠 Multimodal Fake News Detection System

This project implements a **multimodal fake news detection system** capable of analyzing **text, images, videos, and web links**.  
It extracts verifiable claims, retrieves evidence from trusted sources, evaluates semantic similarity, and produces an explainable credibility verdict.

The system is designed as an **academic MCA-level project**, focusing on modularity, explainability, and real NLP techniques.

---

## 📌 System Overview

The system follows a unified verification pipeline:

**Input → Claim Extraction → Claim Normalization → Evidence Retrieval → Verification → Explanation → Verdict**

Supported input types:
- 📝 Text
- 🖼️ Image
- 🎥 Video
- 🔗 News / social media links


---

## 🔁 Processing Pipeline

### 1️⃣ Input Handling
- Handled via **FastAPI** (`app/main.py`)
- Accepts text, file uploads, or URLs
- Routes input based on modality

---

### 2️⃣ Claim Extraction
| Modality | Method |
|--------|--------|
| Text | Abstractive summarization using transformer models |
| Image | OCR → summarized claim |
| Video | Audio extraction → speech-to-text → summarized claim |
| Link | Web scraping → summarized claim |

Goal: extract a **short, factual, verifiable claim**.

---

### 3️⃣ Claim Normalization
- Removes noise and extra clauses
- Keeps claims within API length limits
- Relaxes queries when evidence retrieval fails

---

### 4️⃣ Evidence Retrieval
- Queries Wikipedia and trusted sources
- Extracts multiple evidence snippets
- Assigns trust scores per source

---

### 5️⃣ Claim Verification
- Uses **semantic similarity** (Sentence Transformers)
- Compares extracted claim with retrieved evidence
- Outputs similarity score and verdict label

Possible labels:
- **Supported**
- **Refuted**
- **Uncertain**

---

### 6️⃣ Explanation Generation
- Selects the strongest evidence
- Produces a human-readable explanation
- Explains why a claim is real, fake, or uncertain

---

### 7️⃣ Final Output
json
{
  "claim": "Narendra Modi is President of Bihar",
  "verdict": "Fake",
  "confidence": 0.23,
  "explanation": "Evidence contradicts the claim..."
}
###🚀 How to Run the Project
-#1️⃣ Install dependencies
-bash
-Copy code
-pip install -r requirements.txt
-#2️⃣ Start the FastAPI server
-bash
-Copy code
-uvicorn app.main:app --reload
-#3️⃣ Access the API
-cpp
-Copy code
-http://127.0.0.1:8000
###🎯 Key Features
Multimodal fake news analysis

Modular and extensible architecture

Semantic (meaning-based) verification

Explainable AI outputs

Academic-project friendly design

###⚠️ Limitations
Evidence retrieval mainly relies on Wikipedia

OCR and speech-to-text accuracy depends on input quality

No social media metadata analysis

Claim extraction uses summarization instead of fine-tuned claim models

###🔮 Future Enhancements
Zero-shot and NLI-based verification

Source credibility and social context scoring

Multilingual support

Knowledge graph integration

Fine-tuned claim extraction models

###🎓 Intended Use
This project is intended for:

MCA / academic final-year projects

Research demonstrations

Learning multimodal NLP pipelines

It is not intended for production deployment.
