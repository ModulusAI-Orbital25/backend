from flask import request, jsonify
from models import db
from models import Academics
from models.timetable import Timetable
from flask_login import current_user, login_required
from chat import bp
from os import environ
import requests

GROQ_API_KEY = environ.get("GROQ_API_KEY")


@bp.route("/groq", methods=["POST", "OPTIONS"])
@login_required
def chat():
    if request.method == "OPTIONS":  # wasn't being handled by flask-cors
        return "", 200
    data = request.get_json()

    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    user_id = current_user.id
    user_message = data.get("message")

    user = db.session.get(Academics, user_id)
    timetable = Timetable.query.filter_by(user_id=user_id).first()
    if not user:
        print("User not found")
        return jsonify({"error": "User not found"}), 404

    user_context = f"""
    - Primary Major: {user.primaryMajor}
    - Secondary Major: {user.secondaryMajor or 'None'}
    - Minor 1: {user.minor1 or 'None'}
    - Minor 2: {user.minor2 or 'None'}
    - Completed Modules: {timetable.serialize() if timetable else 'None'}
    - Current Semester: {user.currentSemester}
    - Internship Semester: {user.internshipSem or 'Not set'}
    """

    prompt = f"""
You are ModulusAI, an expert advisor for NUS students helping them plan
their academic journey and discover/recommend modules based on their likes and interests
Keep your answers concise and avoid using bolds or lists

This response may be part of a response of a series of messages and if so here's the history:
{data.get("history")}

Here is the student's academic profile:
{user_context}

Based on the above information, respond to this query:
\"{user_message}\"
"""

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer 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"},
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful academic advisor for NUS.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        },
    )

    if res.status_code != 200:
        print("Groq API error:", res.status_code, res.text)
        return jsonify({"error": "LLM API failed"}), 500

    reply = res.json()["choices"][0]["message"]["content"]
    print("grok error")
    return jsonify({"reply": reply})