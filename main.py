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

# --- Pydantic Models ---
class UserPromptRequest(BaseModel):
    prompt: str

class StructuredPromptResponse(BaseModel):
    original_prompt: str
    structured_prompt: str

# --- Load Environment Variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in the .env file.")

# --- Initialize Gemini API ---
try:
    genai.configure(
        api_key=GOOGLE_API_KEY,
        client_options={'api_endpoint': 'v1alpha-generativelanguage.googleapis.com'}
    )
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    raise

# --- FastAPI App ---
app = FastAPI(
    title="AI Prompt Structuring Backend",
    description="Processes user prompts using Google Gemini.",
    version="1.0.0"
)

# --- CORS Config ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)

# --- Health Check Endpoints ---
@app.get("/")
@app.head("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# --- Prompt Enhancement Endpoint ---
@app.post("/structure-prompt", response_model=StructuredPromptResponse)
async def structure_prompt(request: UserPromptRequest):
    """Enhanced prompt generation endpoint"""
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Construct prompt template
        instruction = (
            "Take the following user query and rephrase it into a more detailed, "
            "specific, and structured prompt. Make it clear and actionable.\n\n"
            f'User Query: "{request.prompt.strip()}"\n\n'
            "Structured Prompt:"
        )
        
        # Generate enhanced prompt
        response = await model.generate_content_async(
            instruction,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=256,
                temperature=0.7
            )
        )
        
        enhanced_prompt = response.text.strip()
        if not enhanced_prompt:
            raise ValueError("Empty response from Gemini API")
            
        return StructuredPromptResponse(
            original_prompt=request.prompt,
            structured_prompt=enhanced_prompt
        )
            
    except Exception as e:
        logger.error(f"Error in prompt enhancement: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate structured prompt: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)