import json

def explain_result(claim: str, verdict: str, confidence: float, evidence: str):
    """
    Creates contextual explanation for a single modality.
    """

    if verdict == "Real":
        explanation = (
            f"The claim '{claim}' is likely true because "
            f"supporting evidence aligns with it: {evidence}"
        )
    elif verdict == "Fake":
        explanation = (
            f"The claim '{claim}' appears false. The evidence contradicts it: "
            f"{evidence}"
        )
    else:
        explanation = (
            f"The claim '{claim}' cannot be fully verified. Evidence is "
            f"inconclusive or insufficient: {evidence}"
        )

    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation
    })

if __name__ == "__main__":
    claim = "WHO approved herbal cure for COVID-19."
    evidence = ["WHO denies approving any herbal cure for COVID-19."]

    from verification import verify_claim
    #from explain_result import explain_result

    result = verify_claim(claim, evidence)
    output = explain_result(
        claim=claim,
        verdict=result["verdict"],
        confidence=result["confidence_score"],
        evidence=result["top_evidence"]
    )

    print(output)

