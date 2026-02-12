# app.py - Streamlit Frontend
import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AWS Learning Agent", 
    page_icon="☁️", 
    layout="wide"
)

# Initialize session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.started = False

# Sidebar
with st.sidebar:
    st.title("☁️ AWS Learning Agent")
    st.caption("Powered by Google ADK + Gemini 2.0")
    st.markdown("---")
    
    if not st.session_state.started:
        st.subheader("Choose Certification")
        cert = st.selectbox(
            "Select your path:",
            ["AWS Cloud Practitioner", 
             "AWS Solutions Architect Associate",
             "AWS Developer Associate"]
        )
        
        if st.button("🚀 Start Learning", use_container_width=True):
            try:
                response = requests.post(
                    f"{API_URL}/start",
                    json={
                        "user_id": st.session_state.user_id,
                        "certification": cert
                    }
                )
                if response.status_code == 200:
                    st.session_state.started = True
                    st.session_state.certification = cert
                    st.success("Session started!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
    else:
        # Show progress
        try:
            progress = requests.get(
                f"{API_URL}/progress/{st.session_state.user_id}"
            ).json()
            
            st.success("🎓 Active Session")
            st.metric("Certification", progress.get("certification", "N/A"))
            st.metric("Current Section", progress.get("current_section", "N/A"))
            st.metric("Completed", f"{len(progress.get('completed_sections', []))} sections")
            
            if st.button("🔄 Reset Session", use_container_width=True):
                st.session_state.started = False
                st.session_state.messages = []
                st.rerun()
        except Exception as e:
            st.warning("Could not load progress")

# Main chat interface
st.title("💬 AWS Certification Tutor")

if not st.session_state.started:
    st.info("👈 Please select a certification from the sidebar to begin!")
else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question or type 'quiz' for a test..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "user_id": st.session_state.user_id,
                            "message": prompt
                        },
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        bot_response = result.get("response", "No response")
                        
                        st.markdown(bot_response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_response
                        })
                    else:
                        error_msg = f"API Error: {response.status_code}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
                        
                except Exception as e:
                    error_msg = f"Connection error: {str(e)}\n\nMake sure API is running: `python api.py`"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Footer
st.markdown("---")
st.caption("🤖 Powered by Google ADK • Gemini 2.0 Flash • Built for AWS Certification")