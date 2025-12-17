import os
import warnings
import json


# --- Clean startup (no warnings) ---
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=FutureWarning)

from transformers import BartForConditionalGeneration, BartTokenizer
import torch

# --- Load BART model ---
MODEL_NAME = "facebook/bart-large-cnn"

tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

# Use CPU explicitly
device = torch.device("cpu")
model.to(device)


def summarize_text(text, max_len=130, min_len=40):
    """
    Summarizes input text using BART.
    """
    inputs = tokenizer(
        text,
        max_length=1024,
        return_tensors="pt",
        truncation=True
    ).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        length_penalty=2.0,
        min_length=18,
        max_length=60,
        early_stopping=True
    )

    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary


# -------------------------
# 🧪 Example usage
# -------------------------
if __name__ == "__main__":
    text = """
    There are times when the night sky glows with bands of color. The bands may
begin as cloud shapes and then spread into a great arc across the entire sky. They
may fall in folds like a curtain drawn across the heavens. The lights usually grow
brighter, then suddenly dim. During this time the sky glows with pale yellow, pink,
green, violet, blue, and red. These lights are called the Aurora Borealis. Some
people call them the Northern Lights. Scientists have been watching them for
hundreds of years. They are not quite sure what causes them. In ancient time people were afraid of the Lights. They imagined that they saw fiery dragons in the
sky. Some even concluded that the heavens were on fire.
    """

    result = summarize_text(text)
    print("\n--- ORIGINAL TEXT ---\n")
    print(text)

    print("\n--- BART SUMMARY ---\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))