import os
import json
from flask import Flask, render_template, request, jsonify

try:
    from google import genai
except ImportError:
    genai = None

app = Flask(__name__)

SYSTEM_PROMPT = """
You are The Blind Spot, an AI critical-thinking assistant.

Your job is NOT to decide for the user. Analyze the user's decision and reasoning
to help them notice what they may have overlooked.

Return valid JSON with exactly these keys:
{
  "summary": "short neutral summary of what the user is focusing on",
  "blind_spots": ["...", "..."],
  "assumptions": ["...", "..."],
  "questions": ["...", "..."],
  "conflicts": ["...", "..."],
  "verify": ["...", "..."]
}

Rules:
- Never tell the user what decision to make.
- Never output a recommendation such as "you should accept/reject/buy/not buy".
- Identify possibilities, not facts you cannot know.
- Be neutral, practical, and concise.
- Distinguish assumptions from verified facts.
- Encourage the user to investigate important missing information.
- If information is insufficient, say what information is missing.
"""

def local_fallback(decision, reasoning):
    return {
        "summary": f"You are mainly focusing on the reasons you provided for: {decision}.",
        "blind_spots": [
            "What important costs, risks, or constraints have not been considered?",
            "Could there be information about the situation that you have not verified?",
            "Have you considered how this decision affects your longer-term goals?"
        ],
        "assumptions": [
            "Some benefits mentioned may be assumed rather than confirmed.",
            "You may be giving more weight to the most visible factors."
        ],
        "questions": [
            "What evidence would change your current thinking?",
            "What is the strongest argument against your current reasoning?",
            "What would the decision look like from another person's perspective?"
        ],
        "conflicts": [
            "A short-term benefit may need to be compared with possible long-term effects."
        ],
        "verify": [
            "Check the important facts, costs, constraints, and alternatives before deciding."
        ]
    }

def analyze_with_ai(decision, reasoning):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or genai is None:
        return local_fallback(decision, reasoning)

    client = genai.Client(api_key=api_key)
    prompt = f"""{SYSTEM_PROMPT}

Decision:
{decision}

User's reasoning:
{reasoning}

Analyze only the reasoning supplied above."""
    try:
        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        return data
    except Exception:
        return local_fallback(decision, reasoning)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    decision = (data.get("decision") or "").strip()
    reasoning = (data.get("reasoning") or "").strip()

    if not decision or not reasoning:
        return jsonify({"error": "Please enter both the decision and your reasoning."}), 400

    result = analyze_with_ai(decision, reasoning)
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
