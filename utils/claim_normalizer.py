import re

WEAK_ENDINGS = {"from", "and", "with", "by", "of", "to"}

def normalize_claim_for_search(text, max_chars=95):
    """
    General event-focused normalization for evidence retrieval APIs.
    Keeps only the primary event.
    """

    # --- keep only first sentence / clause ---
    text = re.split(r"[.;]", text)[0]

    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()

    # remove trailing fragments
    while words and words[-1].lower() in WEAK_ENDINGS:
        words.pop()

    query = " ".join(words)

    # enforce API limit
    if len(query) > max_chars:
        query = query[:max_chars].rsplit(" ", 1)[0]

    return query

def relax_query(query):
    """
    General fallback: removes overly specific action phrases
    while keeping named entities.
    """

    WEAK_ACTIONS = [
        "presents", "presented", "gifted", "hands over",
        "signed", "jersey", "memento", "souvenir"
    ]

    words = query.split()
    relaxed = [w for w in words if w.lower() not in WEAK_ACTIONS]

    relaxed_query = " ".join(relaxed)

    # keep it reasonable length
    if len(relaxed_query) < 20:
        return query  # fallback safety

    return relaxed_query
