import os
import re
import csv
import json
import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

# ================= CONFIG =================

GNEWS_API_KEY = "a760ff580ed4f66bb108fc6e734cb08a"
NEWSDATA_API_KEY = "pub_444e5f779b4f47e2bc9cbfac5dde1b84"

LOCAL_CSV = "local_evidence.csv"
HEADERS = {"User-Agent": "evidence-retriever/3.0"}

TOP_N_EVENT = 4
TOP_N_FACT = 3

# ================= CLAIM CLASSIFICATION =================

def classify_claim(claim: str) -> str:
    c = claim.lower()
    if any(w in c for w in ["died", "killed", "shot", "murdered"]):
        return "death_claim"
    if any(w in c for w in ["visited", "launched", "elected", "arrested"]):
        return "current_event"
    if any(w in c for w in ["worst", "best", "failure"]):
        return "opinion"
    return "static_fact"

# ================= TEXT HELPERS =================

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def relevance_score(claim, text):
    return len(set(clean_text(claim).split()) & set(clean_text(text).split()))

def extract_entities(claim):
    return re.findall(r"\b[A-Z][a-z]+\b", claim)

# ================= GNEWS =================

def fetch_gnews(claim):
    try:
        query = " ".join(extract_entities(claim))
        r = requests.get(
            "https://gnews.io/api/v4/search",
            params={"q": query, "lang": "en", "max": 5, "token": GNEWS_API_KEY},
            timeout=10
        )
        r.raise_for_status()
        return [
            {
                "source": a["source"]["name"],
                "text": a.get("description","") + " " + a.get("content",""),
                "trust_score": 0.85
            }
            for a in r.json().get("articles", [])
        ]
    except Exception as e:
        print("[GNEWS ERROR]", e)
        return []

# ================= NEWSDATA (NewsIO) =================

def fetch_newsdata(claim):
    try:
        url = (
            f"https://newsdata.io/api/1/latest"
            f"?apikey={NEWSDATA_API_KEY}"
            f"&q={urllib.parse.quote(claim)}"
            f"&language=en"
            f"&removeduplicate=1"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return [
            {
                "source": i.get("source_id","newsdata"),
                "text": f"{i.get('title','')} {i.get('description','')}",
                "trust_score": 0.85
            }
            for i in r.json().get("results", [])
        ]
    except Exception as e:
        print("[NEWSDATA ERROR]", e)
        return []

# ================= WIKIPEDIA =================

def fetch_wikipedia(claim):
    evidences = []
    r = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action":"query","list":"search","srsearch":claim,"format":"json"},
        headers=HEADERS
    )
    r.raise_for_status()
    for res in r.json()["query"]["search"][:2]:
        title = res["title"].replace(" ","_")
        page = requests.get(f"https://en.wikipedia.org/wiki/{title}", headers=HEADERS)
        soup = BeautifulSoup(page.text,"html.parser")
        evidences.append({
            "source": "wikipedia",
            "text": soup.get_text(" ",strip=True)[:2000],
            "trust_score": 0.75
        })
    return evidences

# ================= PROVENANCE =================

def detect_provenance(claim, claim_type, text):
    t = text.lower()

    if claim_type == "death_claim":
        if any(w in t for w in ["died","killed","shot"]):
            return {"type":"supporting","score":1.0}
        return {"type":"contradicting","score":0.0}

    ents = extract_entities(claim)
    if all(e.lower() in t for e in ents):
        return {"type":"neutral","score":0.4}

    return {"type":"neutral","score":0.2}

# ================= LOCAL CSV =================

def store_csv(claim, ev):
    exists = os.path.exists(LOCAL_CSV)
    with open(LOCAL_CSV,"a",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["claim","source","trust_score","prov_type","prov_score","timestamp"]
        )
        if not exists:
            writer.writeheader()
        writer.writerow({
            "claim": claim,
            "source": ev["source"],
            "trust_score": ev["trust_score"],
            "prov_type": ev["provenance"]["type"],
            "prov_score": ev["provenance"]["score"],
            "timestamp": datetime.utcnow().isoformat()
        })

# ================= MAIN ENTRY =================

def retrieve_evidence(claim):
    claim_type = classify_claim(claim)
    evidences = []

    if claim_type == "current_event":
        evidences += fetch_gnews(claim)
        evidences += fetch_newsdata(claim)
        top_n = TOP_N_EVENT

    elif claim_type == "static_fact":
        evidences += fetch_newsdata(claim)
        evidences += fetch_wikipedia(claim)
        top_n = TOP_N_FACT

    elif claim_type == "death_claim":
        evidences += fetch_gnews(claim)
        evidences += fetch_newsdata(claim)
        evidences += fetch_wikipedia(claim)
        top_n = TOP_N_EVENT

    else:
        return {"claim":claim,"claim_type":claim_type,"evidence":[]}

    # relevance filtering
    for e in evidences:
        e["relevance"] = relevance_score(claim, e["text"])

    evidences = sorted(evidences, key=lambda x: x["relevance"], reverse=True)[:top_n]

    # provenance + store
    for e in evidences:
        e["provenance"] = detect_provenance(claim, claim_type, e["text"])
        store_csv(claim, e)

    return {
        "claim": claim,
        "claim_type": claim_type,
        "evidence": evidences
    }

# ================= DEMO =================

if __name__ == "__main__":
    c = " Lionel Messi arrived in Kolkata on December 13, 2025, to kick off the GOAT India Tour 2025."
    print(json.dumps(retrieve_evidence(c), indent=2))
