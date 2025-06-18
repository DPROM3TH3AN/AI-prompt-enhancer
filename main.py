import os
import logging
from dotenv import load_dotenv
import uvicorn
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Models for Request and Response ---
class UserPromptRequest(BaseModel):
    prompt: str

class StructuredPromptResponse(BaseModel):
    original_prompt: str
    structured_prompt: str

# --- Load Environment Variables ---
load_dotenv()

# --- Initialize API Clients ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in the .env file.")

try:
    genai.configure(
        api_key=GOOGLE_API_KEY,
        client_options={'api_endpoint': 'v1alpha-generativelanguage.googleapis.com'}
    )
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    raise

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Prompt Structuring Backend",
    description="Processes user prompts, stores them, and uses Gemini to generate a more structured version.",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# --- API Endpoints ---
@app.head("/")
@app.get("/")
async def read_root():
    return {"status": "AI Prompt Structuring Backend is running"}

@app.head("/structure-prompt")
@app.post("/structure-prompt", response_model=StructuredPromptResponse)
async def structure_prompt(request: UserPromptRequest = None):
    """
    Handles both HEAD requests and POST requests for prompt structuring.
    Returns enhanced version of the input prompt using Gemini AI.
    """
    if request is None:  # HEAD request
        return {}
    
    # 1. Input validation
    original_user_prompt_text = request.prompt
    if not original_user_prompt_text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # 2. Preprocessing
    processed_user_prompt_text = original_user_prompt_text.strip()

    # 3. Construct the prompt template
    gemini_instruction_prompt = (
        "Take the following user query and rephrase it into a more detailed, specific, and structured prompt.\n"
        "The goal is to make the user's original query more effective for an AI assistant.\n"
        "The rephrased prompt should be clear, actionable, and elaborate on the potential scope of the query.\n"
        "Do not answer the query, only rephrase it into a better prompt.\n\n"
        f'User Query: "{processed_user_prompt_text}"\n\n'
        "Structured Prompt:"
    )

    # 4. Generate enhanced prompt using Gemini
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = await model.generate_content_async(
            gemini_instruction_prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=256,
                temperature=0.7
            )
        )
        structured_prompt_text = response.text.strip()
        
        if not structured_prompt_text:
            raise ValueError("Empty response from Gemini API")
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate structured prompt: {str(e)}"
        )

    # 5. Return the response
    return StructuredPromptResponse(
        original_prompt=original_user_prompt_text,
        structured_prompt=structured_prompt_text
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)