# Multi-Modal-Fake-News-Detection
# 📰 Fake News Detection System  

A **multimodal AI-powered system** that detects fake news from **text, images, and videos**.  
Built as an **MCA Minor Project** using **Transformers, OpenAI Whisper, ImageHash, and Streamlit**.  

---

## 📌 Project Overview
Fake news is a growing problem in today’s world, especially with the rapid spread of misinformation through social media.  
This project aims to build an **automated system** that can analyze **text, photos, and videos** to classify whether the news content is **real or fake**.  

---

## 🎯 Features
- ✅ **Text Fake News Detection** using NLP & Transformers (DistilBERT)  
- ✅ **Image Verification** using perceptual hashing & reverse search APIs  
- ✅ **Video Analysis** by extracting audio → speech-to-text → text classifier  
- ✅ **User-Friendly Web App** built with Streamlit  
- ✅ **Confidence Score** for prediction results  

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Libraries & Tools:**  
  - Pandas, Scikit-learn  
  - HuggingFace Transformers (DistilBERT)  
  - OpenCV, PIL, ImageHash  
  - OpenAI Whisper (speech-to-text)  
  - Streamlit (Web UI)  

---

## 👥 Team Members & Responsibilities
- **Member 1:** Dataset collection & preprocessing (text news data)  
- **Member 2:** Text fake news detection (Transformer-based model)  
- **Member 3:** Image verification (ImageHash & reverse search)  
- **Member 4:** Video analysis (frame extraction + Whisper)  
- **Member 5:** Integration & Streamlit app development  

---

## 📂 Project Structure
fake-news-detection/
│── data/ # Datasets
│ ├── fake_news.csv
│ └── sample_video.mp4
│
│── models/ # Saved ML models
│ └── text_model/
│
│── notebooks/ # Jupyter notebooks for experiments
│ ├── preprocessing.ipynb
│ ├── text_model.ipynb
│ └── video_analysis.ipynb
│
│── app/ # Streamlit app
│ ├── app.py
│ └── utils.py
│
│── requirements.txt # Dependencies
│── README.md # Project documentation


---

## ⚙️ Installation & Setup


###3️⃣ Install dependencies
pip install -r requirements.txt

###4️⃣ Run the Streamlit app
cd app
streamlit run app.py
