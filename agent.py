from google import genai
from google.genai import types
import os
import json

# -----------------------------
# Safe Gemini Client Factory
# -----------------------------

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")

    return genai.Client(api_key=api_key)


# -----------------------------
# Learning Agent
# -----------------------------

class LearningAgent:

    def __init__(self):
        self.model = "gemini-2.0-flash"

    def generate_lesson(self, section: str):

        client = get_gemini_client()

        prompt = f"""
You are an AWS certification tutor.

Teach the section: {section}

Respond using:
- Concept
- Real World Example
- Exam Tips
- Common Mistakes
"""

        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )

        return response.text


# -----------------------------
# Assessment Agent
# -----------------------------

class AssessmentAgent:

    def generate_quiz(self, section: str):

        client = get_gemini_client()

        prompt = f"""
Generate 5 AWS certification MCQs for section: {section}

Return ONLY valid JSON in this format:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "Correct Option Text"
    }}
  ]
}}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=800
            )
        )

        try:
            return json.loads(response.text)
        except:
            return {"questions": []}

# -----------------------------
# Feedback Agent
# -----------------------------

class FeedbackAgent:

    def evaluate(self, score: int):

        if score >= 90:
            return "Excellent performance! Move to next section."

        elif score >= 70:
            return "Good job! Reinforce weak areas and continue."

        else:
            return "Score below 70%. Re-teaching simplified explanation recommended."
