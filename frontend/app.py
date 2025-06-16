
import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Prompt Enhancer",
    page_icon="✨",
    layout="wide" # Using wide layout for more space
)

# --- Backend Configuration ---
BACKEND_URL = "http://0.0.0.0:8000/structure-prompt" # Updated endpoint

# --- UI Components ---
st.title("✨ AI Prompt Enhancer")
st.markdown(
    "Enter your initial prompt, and our AI agent will help you refine it "
    "into a more structured and effective version using Google Gemini. "
    "All interactions are logged in Supabase."
)

st.sidebar.header("How it Works")
st.sidebar.info(
    "1. You enter a basic idea or question.\n"
    "2. We preprocess it and send it to our backend.\n"
    "3. The backend securely logs your prompt.\n"
    "4. Google Gemini is then used to transform your input into a more detailed and structured prompt.\n"
    "5. The enhanced prompt is displayed back to you."
)


user_prompt = st.text_area("Enter your initial prompt here:", height=100, key="user_prompt_input")

if st.button("Enhance My Prompt", type="primary"):
    if user_prompt:
        with st.spinner("🧠 Let me think... Enhancing your prompt..."):
            try:
                payload = {"prompt": user_prompt}
                response = requests.post(BACKEND_URL, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Prompt Enhanced!")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Your Original Prompt:")
                        st.text_area("", value=result.get("original_prompt"), height=150, disabled=True, key="orig_prompt_display")

                    with col2:
                        st.subheader("AI Enhanced Prompt:")
                        st.text_area("", value=result.get("structured_prompt"), height=150, key="structured_prompt_display")
                        if result.get("structured_prompt", "").startswith("Error:"):
                            st.warning("There was an issue generating the enhanced prompt. The AI might have had trouble or an error occurred.")


                else:
                    try:
                        error_details = response.json().get("detail", "Unknown error from backend.")
                    except json.JSONDecodeError:
                        error_details = response.text
                    st.error(f"Error from backend (Status {response.status_code}): {error_details}")

            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend. Is it running at http://127.0.0.1:8000 ?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt to enhance.")

st.markdown("---")
st.caption("Powered by Streamlit, FastAPI, Supabase, and Google Gemini.")
