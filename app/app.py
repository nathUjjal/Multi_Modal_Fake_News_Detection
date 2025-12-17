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
import json

st.set_page_config(layout="wide")

# ---------- PAGE TITLE (CENTERED) ----------
st.markdown(
    """
    <h1 style='text-align: center;'>
        What's on the agenda today?
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------- CENTERING CONTAINER ----------
center = st.container()
with center:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

    # Create spacing + a centered block width
    _, mid, _ = st.columns([1, 2, 1])
    with mid:

        # ---------- INPUT BAR IN ONE ROW ----------
        c1, c2, c3 = st.columns([1, 4, 1])

        with c1:
            uploaded_file = st.file_uploader(
                "",
                help="Add files",
                label_visibility="collapsed"
            )

        with c2:
            text_query = st.text_area(
                "",
                placeholder="Ask anything",
                label_visibility="collapsed",
                height=60
            )

        with c3:
            submit_button = st.button(
                "Enter",
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- LOGIC ----------
if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

if submit_button and text_query:
    st.success(f"Query submitted: '{text_query}'")


# ---------- SAMPLE JSON OUTPUT ----------
json_str = '{"verdict": "Uncertain", "confidence": 0.34, "explanation": "The Claim WHO approved herbal cure for COVID-19. is marked as Uncertain because The supporting sources indicates : No official WHO announcement found."}'
data = json.loads(json_str)

st.markdown(
    "<h3 style='text-align: center;'>Analysis Result</h3>",
    unsafe_allow_html=True
)

# Center results
r1, r2, r3 = st.columns([1, 2, 1])

with r2:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Verdict", value=data["verdict"])

    with col2:
        st.metric(label="Confidence Score", value=f"{data['confidence'] * 100:.0f}%")

    explanation = data["explanation"]
    verdict = data["verdict"].lower()

    if "uncertain" in verdict:
        st.warning(f"**Explanation:** {explanation}")
    elif "fake" in verdict or "false" in verdict:
        st.error(f"**Explanation:** {explanation}")
    else:
        st.success(f"**Explanation:** {explanation}")



# def text_output_generator(text):
#     extract_claim_from_text(text)


# def image_output_generator(image_path):
#     extract_claim_from_image(image_path)

# def video_output_generator(video_path):
#     extract_claim_from_video(video_path)