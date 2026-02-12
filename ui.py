import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AWS Agentic Learning System",
    page_icon="☁️",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.started = False
    st.session_state.certification = None
    st.session_state.lesson = None
    st.session_state.quiz = None
    st.session_state.score_submitted = False


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:
    st.title("☁️ AWS Agentic Tutor")
    st.caption("Gemini + Google ADK")

    st.markdown("---")

    if not st.session_state.started:

        st.subheader("Choose Certification")

        cert = st.selectbox(
            "Select Path:",
            [
                "AWS Cloud Practitioner",
                "AWS Solutions Architect Associate",
                "AWS Developer Associate"
            ]
        )

        if st.button("🚀 Start Learning", use_container_width=True):
            try:
                r = requests.post(
                    f"{API_URL}/start",
                    json={
                        "user_id": st.session_state.user_id,
                        "certification": cert
                    }
                )

                if r.status_code == 200:
                    st.session_state.started = True
                    st.session_state.certification = cert
                    st.success("Session Started!")
                    st.rerun()
                else:
                    st.error("Failed to start session")

            except Exception as e:
                st.error(f"API Error: {e}")

    else:
        # Progress
        try:
            progress = requests.get(
                f"{API_URL}/progress/{st.session_state.user_id}"
            ).json()

            st.success("🎓 Active Session")

            st.metric("Certification", progress.get("certification"))
            st.metric("Current Section", progress.get("current_section"))
            st.metric(
                "Completed Sections",
                len(progress.get("completed_sections", []))
            )

        except:
            st.warning("Could not load progress")

        if st.button("🔄 Reset Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()


# -------------------------
# Main Interface
# -------------------------

st.title("📚 AWS Certification Learning System")

if not st.session_state.started:
    st.info("👈 Select certification to begin.")
    st.stop()


# -------------------------
# Teach Section
# -------------------------

if st.button("📖 Teach Current Section", use_container_width=True):

    try:
        r = requests.post(
            f"{API_URL}/teach",
            json={"user_id": st.session_state.user_id}
        )

        if r.status_code == 200:
            lesson = r.json().get("lesson")
            st.session_state.lesson = lesson
            st.session_state.quiz = None
            st.session_state.score_submitted = False

        else:
            st.error("Failed to load lesson")

    except Exception as e:
        st.error(str(e))


if st.session_state.lesson:
    st.markdown("### 🧠 Lesson")
    st.markdown(st.session_state.lesson)


# -------------------------
# Generate Quiz
# -------------------------

if st.button("📝 Take Assessment", use_container_width=True):

    try:
        r = requests.post(
            f"{API_URL}/assess",
            json={"user_id": st.session_state.user_id}
        )

        if r.status_code == 200:
            quiz = r.json().get("quiz")
            st.session_state.quiz = quiz
            st.session_state.score_submitted = False
        else:
            st.error("Failed to generate quiz")

    except Exception as e:
        st.error(str(e))


# -------------------------
# Display Quiz
# -------------------------

if st.session_state.quiz:

    st.markdown("### 🧪 Quiz")

    answers = []

    for i, q in enumerate(st.session_state.quiz.get("questions", [])):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        choice = st.radio(
            "Select answer:",
            q["options"],
            key=f"q{i}"
        )

        answers.append(choice)

    if st.button("✅ Submit Answers") and not st.session_state.score_submitted:

        correct_answers = [
            q["answer"] for q in st.session_state.quiz["questions"]
        ]

        score = sum(
            1 for a, c in zip(answers, correct_answers) if a == c
        )

        percent = int((score / len(correct_answers)) * 100)

        try:
            r = requests.post(
                f"{API_URL}/submit-score",
                json={
                    "user_id": st.session_state.user_id,
                    "score": percent
                }
            )

            feedback = r.json().get("feedback")

            st.session_state.score_submitted = True

            st.markdown("### 📊 Performance")
            st.success(f"Score: {percent}%")
            st.markdown(feedback)

        except Exception as e:
            st.error(str(e))


# -------------------------
# Footer
# -------------------------

st.markdown("---")
st.caption("🤖 Agentic AI • Google ADK • Gemini • Tavily • Performance Adaptive Learning")
