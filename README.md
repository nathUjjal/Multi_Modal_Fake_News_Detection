# 📰 Fake News Detection System

A **multimodal AI-powered system** that detects fake news from **text, images, and videos**.
Built as an **MCA Minor Project** using **Transformers, OpenAI Whisper, ImageHash, and Streamlit**.

---

## 📌 Project Overview

Fake news is a growing problem in today’s world, especially with the rapid spread of misinformation through social media.
This project aims to build an **automated system** that can analyze **text, photos, and videos** to classify whether the news content is **real or fake**.

---

## 🎯 Features

* ✅ **Text Fake News Detection** using NLP & Transformers (DistilBERT)
* ✅ **Image Verification** using perceptual hashing & reverse search APIs
* ✅ **Video Analysis** by extracting audio → speech-to-text → text classifier
* ✅ **User-Friendly Web App** built with Streamlit
* ✅ **Confidence Score** for prediction results

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Libraries & Tools:**

  * Pandas, Scikit-learn
  * HuggingFace Transformers (DistilBERT)
  * OpenCV, PIL, ImageHash
  * OpenAI Whisper (speech-to-text)
  * Streamlit (Web UI)

---

## 👥 Team Members & Responsibilities

* **Member 1:** Dataset collection & preprocessing (text news data)
* **Member 2:** Text fake news detection (Transformer-based model)
* **Member 3:** Image verification (ImageHash & reverse search)
* **Member 4:** Video analysis (frame extraction + Whisper)
* **Member 5:** Integration & Streamlit app development

---

## 📂 Project Structure

```
fake-news-detection/
│── data/                        # Datasets
│   ├── fake_news.csv
│   └── sample_video.mp4
│
│── models/                      # Saved ML models
│   └── text_model/
│
│── notebooks/                   # Jupyter notebooks for experiments
│   ├── preprocessing.ipynb
│   ├── text_model.ipynb
│   └── video_analysis.ipynb
│
│── app/                         # Streamlit app
│   ├── app.py
│   └── utils.py
│
│── requirements.txt             # Dependencies
│── README.md                    # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/fake-news-detection.git
cd fake-news-detection
```

### 2️⃣ Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app

```bash
cd app
streamlit run app.py
```

---

## 🚀 How It Works

1. **Text Input:** User enters news text → NLP model classifies as Fake/Real.
2. **Image Input:** User uploads an image → System checks perceptual hash & verifies authenticity.
3. **Video Input:** System extracts audio → converts to text using Whisper → passes transcript to NLP model.

---

## 📸 Screenshots (To be added)

* [ ] App Homepage
* [ ] Text Fake News Detection Example
* [ ] Image Verification Example
* [ ] Video Transcript Classification

---

## 📊 Expected Outcomes

* Higher accuracy in detecting fake vs real news.
* Multimodal analysis for **text + image + video** news content.
* A usable **Streamlit app** that demonstrates fake news detection in real time.

---

## 🌍 Applications

* Fake news detection for social media posts
* Academic research on misinformation
* Integration with fact-checking APIs
* Awareness tool for the public

---

## 🔮 Future Scope

* Improve accuracy with fine-tuned models on larger datasets
* Integrate real-time **Fact-Check APIs** (e.g., Google Fact Check API)
* Expand to **multilingual fake news detection**
* Deploy as a cloud-based web service

---

## 📚 References

* [Kaggle Fake News Dataset](https://www.kaggle.com/c/fake-news/data)
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
* [OpenAI Whisper](https://github.com/openai/whisper)
* [Streamlit](https://docs.streamlit.io/)
* [ImageHash](https://pypi.org/project/ImageHash/)

---

👨‍💻 **Developed by MCA Students as part of Minor Project**

---
