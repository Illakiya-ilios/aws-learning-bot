from agent import LearningAgent, AssessmentAgent, FeedbackAgent
from config import CERTIFICATIONS


class Orchestrator:

    def __init__(self):
        self.learning_agent = LearningAgent()
        self.assessment_agent = AssessmentAgent()
        self.feedback_agent = FeedbackAgent()
        self.sessions = {}

    # ---------------------------------------------------
    # START SESSION
    # ---------------------------------------------------
    def start(self, user_id: str, certification: str):

        if certification not in CERTIFICATIONS:
            return {"error": "Invalid certification"}

        domains = CERTIFICATIONS[certification]["domains"]

        if not domains:
            return {"error": "No curriculum found"}

        first_section = domains[0]["name"]

        self.sessions[user_id] = {
            "certification": certification,
            "current_index": 0,
            "current_section": first_section,
            "completed_sections": [],
            "scores": [],
            "weak_topics": [],
            "learning_pace": "normal"
        }

        return {
            "message": f"Started {certification}",
            "current_section": first_section
        }

    # ---------------------------------------------------
    # TEACH CURRENT SECTION
    # ---------------------------------------------------
    def teach(self, user_id: str):

        session = self.sessions.get(user_id)

        if not session:
            return {"lesson": "Session not found"}

        section = session["current_section"]

        lesson = self.learning_agent.generate_lesson(section)

        return lesson

    # ---------------------------------------------------
    # GENERATE QUIZ
    # ---------------------------------------------------
    def assess(self, user_id: str):

        session = self.sessions.get(user_id)

        if not session:
            return {"quiz": {"questions": []}}

        section = session["current_section"]

        quiz = self.assessment_agent.generate_quiz(section)

        return quiz

    # ---------------------------------------------------
    # SUBMIT SCORE & PERFORMANCE LOGIC
    # ---------------------------------------------------
    def submit_score(self, user_id: str, score: int):

        session = self.sessions.get(user_id)

        if not session:
            return {"feedback": "Session not found"}

        session["scores"].append(score)

        feedback = self.feedback_agent.evaluate(score)

        certification = session["certification"]
        domains = CERTIFICATIONS[certification]["domains"]

        # --------------------------
        # PERFORMANCE-BASED FLOW
        # --------------------------

        if score >= 90:
            # Move to next section immediately
            return self._move_to_next_section(user_id, feedback)

        elif score >= 70:
            # Mark complete but suggest review
            session["completed_sections"].append(session["current_section"])
            return {
                "feedback": feedback,
                "next_action": "optional_review"
            }

        else:
            # Weak topic detected
            session["weak_topics"].append(session["current_section"])
            session["learning_pace"] = "slow"

            return {
                "feedback": feedback,
                "next_action": "reteach"
            }

    # ---------------------------------------------------
    # MOVE TO NEXT SECTION
    # ---------------------------------------------------
    def _move_to_next_section(self, user_id: str, feedback: str):

        session = self.sessions[user_id]
        certification = session["certification"]
        domains = CERTIFICATIONS[certification]["domains"]

        current_index = session["current_index"]
        session["completed_sections"].append(session["current_section"])

        next_index = current_index + 1

        if next_index >= len(domains):
            return {
                "feedback": feedback,
                "message": "🎉 Certification curriculum completed!",
                "completed": True
            }

        # Update session
        session["current_index"] = next_index
        session["current_section"] = domains[next_index]["name"]

        return {
            "feedback": feedback,
            "next_section": session["current_section"],
            "completed": False
        }

    # ---------------------------------------------------
    # PROGRESS
    # ---------------------------------------------------
    def get_progress(self, user_id: str):

        session = self.sessions.get(user_id)

        if not session:
            return {}

        return {
            "certification": session["certification"],
            "current_section": session["current_section"],
            "completed_sections": session["completed_sections"],
            "scores": session["scores"],
            "weak_topics": session["weak_topics"],
            "learning_pace": session["learning_pace"]
        }
