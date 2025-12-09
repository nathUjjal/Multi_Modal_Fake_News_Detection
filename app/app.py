# import streamlit as st
# from transformers import pipeline
# from utils import check_image

# pipe = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# st.title("📰 Fake News Detection System")

# option = st.radio("Choose Input Type", ["Text", "Image", "Video"])

# if option == "Text":
#     user_input = st.text_area("Enter news text")
#     if st.button("Check"):
#         result = pipe(user_input)[0]
#         st.write("Prediction:", result['label'], "| Confidence:", round(result['score'], 2))

# elif option == "Image":
#     img_file = st.file_uploader("Upload image", type=["jpg","png"])
#     if img_file and st.button("Check"):
#         st.write(check_image(img_file))

# elif option == "Video":
#     st.write("For demo, transcript → text model (developed by Member 4)")



import streamlit as st
# from src.datafusionandexplanation import fuse_and_explain
import json

st.set_page_config(layout="wide")

# Use columns to center the components
left_space, main_content, right_space = st.columns([1, 2, 1])

with main_content:
    st.title("What's on the agenda today?")

    # Create the 3-column layout for the components
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        # --- 1. The "Add file" button ---
        # This IS the file browse function.
        # We cannot change its icon to a "+".
        # We add the "Add files" hover text.
        uploaded_file = st.file_uploader(
            "Upload",
            help="Add files",
            label_visibility="collapsed" # Hides the "Upload" label
        )

    with col2:
        # --- 2. The Search Bar ---
        text_query = st.text_input(
            "Query",
            placeholder="Ask anything",
            label_visibility="collapsed" # Hides the "Query" label
        )

    with col3:
        # --- 3. The Submit Button ---
        submit_button = st.button(
            "Enter",
            help="Submit",
            use_container_width=True
        )

    # --- 4. Logic to make them work ---
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")

    if submit_button and text_query:
        st.success(f"Query submitted: '{text_query}'")


json_str = '{"verdict": "Uncertain", "confidence": 0.34, "explanation": "The Claim WHO approved herbal cure for COVID-19. is marked as Uncertain because The supporting sources indicates : No official WHO announcement found."}'

# 2. Parse string into a Python Dictionary
data = json.loads(json_str)

st.subheader("Analysis Result")

# 3. Create columns for key metrics
col1, col2 = st.columns(2)

with col1:
    # Display the verdict clearly
    st.metric(label="Verdict", value=data["verdict"])

with col2:
    # Format confidence as a percentage
    st.metric(label="Confidence Score", value=f"{data['confidence'] * 100:.0f}%")

# 4. Use dynamic alerts based on the verdict
explanation = data["explanation"]
verdict = data["verdict"].lower()

if "uncertain" in verdict:
    st.warning(f"**Explanation:** {explanation}")
elif "fake" in verdict or "false" in verdict:
    st.error(f"**Explanation:** {explanation}")
else:
    st.success(f"**Explanation:** {explanation}")