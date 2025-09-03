import streamlit as st
from transformers import pipeline
from utils import check_image

pipe = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

st.title("📰 Fake News Detection System")

option = st.radio("Choose Input Type", ["Text", "Image", "Video"])

if option == "Text":
    user_input = st.text_area("Enter news text")
    if st.button("Check"):
        result = pipe(user_input)[0]
        st.write("Prediction:", result['label'], "| Confidence:", round(result['score'], 2))

elif option == "Image":
    img_file = st.file_uploader("Upload image", type=["jpg","png"])
    if img_file and st.button("Check"):
        st.write(check_image(img_file))

elif option == "Video":
    st.write("For demo, transcript → text model (developed by Member 4)")
