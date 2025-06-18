import streamlit as st
import requests
import os

# --- Configuration ---
BASE_URL = os.getenv("BACKEND_URL", "http://0.0.0.0:8000").rstrip('/')
API_ENDPOINT = f"{BASE_URL}/structure-prompt"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# --- Health Check Function ---
def check_backend_health():
    """Check if backend is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/", headers=HEADERS, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# --- Page Setup ---
st.set_page_config(
    page_title="AI Prompt Enhancer",
    page_icon="✨",
    layout="wide"
)

# --- Backend Health Check ---
if not check_backend_health():
    st.error(f"⚠️ Backend service is not accessible. Please try again later.")
    st.stop()

# --- UI Components ---
st.title("✨ AI Prompt Enhancer")
st.markdown(
    "Enter your initial prompt, and our AI agent will help you refine it "
    "into a more structured and effective version using Google Gemini."
)

with st.sidebar:
    st.header("How it Works")
    st.info(
        "1. Enter your basic prompt or question\n"
        "2. Our AI processes your input\n"
        "3. Get back an enhanced, structured version\n"
        "4. Use the improved prompt with any AI system"
    )

# --- Main Interface ---
user_prompt = st.text_area(
    "Enter your initial prompt:",
    height=100,
    key="user_prompt"
)

if st.button("Enhance My Prompt", type="primary"):
    if not user_prompt:
        st.warning("Please enter a prompt to enhance.")
        st.stop()
        
    with st.spinner("🧠 Enhancing your prompt..."):
        try:
            response = requests.post(
                API_ENDPOINT,
                headers=HEADERS,
                json={"prompt": user_prompt}
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Prompt Enhanced!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original Prompt")
                    st.text_area(
                        "",
                        value=result["original_prompt"],
                        height=150,
                        disabled=True
                    )
                
                with col2:
                    st.subheader("Enhanced Prompt")
                    st.text_area(
                        "",
                        value=result["structured_prompt"],
                        height=150,
                        key="enhanced"
                    )
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Please check if the backend service is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.caption("Powered by Streamlit + FastAPI + Google Gemini")