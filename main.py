import os
from dotenv import load_dotenv
import uvicorn
import google.generativeai as genai

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# --- Pydantic Models for Request and Response ---
class UserPromptRequest(BaseModel):
    prompt: str

class StructuredPromptResponse(BaseModel): # Renamed from IntentResponse
    original_prompt: str
    structured_prompt: str # Renamed from intent

# --- Load Environment Variables ---
load_dotenv()

# --- Initialize API Clients ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not (GOOGLE_API_KEY):
    raise ValueError("API keys  must be set in the .env file.")

    genai.configure(
        api_key=GOOGLE_API_KEY,
        client_options={'api_endpoint': 'v1alpha-generativelanguage.googleapis.com'}
    )

# ---astAPI App Initialization ---
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
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "AI Prompt Structuring Backend is running"}

@app.post("/structure-prompt", response_model=StructuredPromptResponse) # Endpoint name changed
async def structure_prompt(request: UserPromptRequest):
    """
    Receives a user prompt, preprocesses it, stores it,
    gets a structured version from Gemini, updates storage,
    and returns both prompts.
    """
    original_user_prompt_text = request.prompt
    if not original_user_prompt_text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # 1. Preprocessing
    processed_user_prompt_text = original_user_prompt_text.strip().lower()


    # 3. Construct the prompt for Gemini to restructure the user's prompt
    gemini_instruction_prompt = f"""
    Take the following user query and rephrase it into a more detailed, specific, and structured prompt.
    The goal is to make the user's original query more effective for an AI assistant.
    The rephrased prompt should be clear, actionable, and elaborate on the potential scope of the query.
    Do not answer the query, only rephrase it into a better prompt.

    User Query: "{processed_user_prompt_text}"

    Structured Prompt:
    """

    # 4. Send to Gemini API
    structured_prompt_text = ""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        # For this task, we want a direct generation, not a chat usually.
        # You might need to adjust generation_config for more control.
        response = await model.generate_content_async(
            gemini_instruction_prompt,
            generation_config=genai.types.GenerationConfig(
                  candidate_count=1, # We only need one good suggestion
                  max_output_tokens=256,
                  temperature=0.7 # Adjust for creativity vs. directness
            )
        )
        structured_prompt_text = response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Even if Gemini fails, we might still want to proceed without the structured prompt
        # or return an error. For now, let's allow it to proceed and log an empty string.
        # Alternatively, raise HTTPException:
        # raise HTTPException(status_code=500, detail=f"Failed to get structured prompt from AI model: {e}")
        structured_prompt_text = "Error: Could not generate structured prompt from AI."



    # 6. Return the response to the frontend
    return StructuredPromptResponse(
        original_prompt=original_user_prompt_text,
        structured_prompt=structured_prompt_text
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
