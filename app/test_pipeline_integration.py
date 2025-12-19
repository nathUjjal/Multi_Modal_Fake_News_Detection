import json
import importlib
import sys, os
# ensure project root is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Import the pipeline module by file path to avoid loading the Streamlit app
from importlib import util
pipeline_path = os.path.join(os.path.dirname(__file__), "pipeline.py")
spec = util.spec_from_file_location("pipeline", pipeline_path)
pipeline = util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

# --- Mock the evidence retriever to keep test deterministic ---

def fake_retrieve_evidence(claim):
    return {
        "claim": claim,
        "claim_type": "static_fact",
        "evidence": [
            {
                "source": "wikipedia",
                "text": "The Sun is the star at the center of the Solar System.",
                "trust_score": 0.9,
            }
        ]
    }

pipeline.retrieve_evidence = fake_retrieve_evidence

# --- Run pipeline with advanced verifier ---

payload = {
    "type": "text",
    "input": "The Sun is a star.",
    "verifier": "advanced"  # explicit choice
}

result = pipeline.process_request(payload)
print(json.dumps(result, indent=2))

# Basic assertions
assert "claim" in result
assert "verdict" in result
assert "confidence" in result
assert "explanation" in result
print("Integration test passed: response contains expected keys.")
