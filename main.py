import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(
    title="Nebius x NVIDIA AI Agent API",
    description="Backend API running NVIDIA Nemotron on Nebius infrastructure"
)

# Load variables from .env file
load_dotenv()

# Retrieve API token from environment
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

class PromptRequest(BaseModel):
    user_prompt: str

@app.post("/hackathon-agent")
async def run_agent(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="nvidia/Nemotron-Mini-4B-Instruct",
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert AI Data Science & Backend Engineering Assistant for the Nebius x NVIDIA Hackathon. Provide crisp, technically precise answers."
                },
                {"role": "user", "content": request.user_prompt}
            ],
            max_tokens=1000
        )
        return {
            "status": "success",
            "provider": "Nebius Infrastructure (NVIDIA Nemotron)",
            "model_used": "nvidia/Nemotron-Mini-4B-Instruct",
            "agent_response": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
