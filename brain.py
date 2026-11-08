import json
from pathlib import Path

# Locate our agriculture knowledge file
BASE_DIR = Path(__file__).parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "agriculture.json"


def load_knowledge():
    """Load agricultural information from JSON."""

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_agriculture_answer(question):
    """Find an agricultural answer using keyword matching."""

    knowledge = load_knowledge()

    question = question.lower()

    best_match = None
    highest_score = 0

    for item in knowledge:

        score = 0
        matched_keywords = []

        for keyword in item["keywords"]:

            if keyword.lower() in question:
                score += 1
                matched_keywords.append(keyword)

        if score > highest_score:
            highest_score = score
            best_match = item

    # Require at least two matching keywords
    if best_match and highest_score >= 2:

        return {
            "success": True,
            "crop": best_match["crop"],
            "answer_te": best_match["answer_te"],
            "answer_en": best_match["answer_en"],
            "source": best_match.get("source", "Source not specified"),
            "matched_keywords": highest_score
        }

    return {
        "success": False,
        "answer_te": "క్షమించండి. మీ ప్రశ్నకు సంబంధించిన సమాచారం ప్రస్తుతం నా దగ్గర లేదు. దయచేసి సమీప వ్యవసాయ అధికారిని సంప్రదించండి.",
        "answer_en": "Sorry, I don't currently have reliable information for this question. Please consult a local agricultural officer."
    }