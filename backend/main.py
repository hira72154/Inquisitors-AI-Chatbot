from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="MAA Chatbot Backend",
    description="Backend for MAA AI Companion Chatbot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    sources: list = []
    memory_updated: bool = False

def get_relevant_memories(user_id: str, message: str) -> list:
    return []

def retrieve_context(query: str, top_k: int = 3) -> list:
    return []

def get_llm_response(user_message: str, context: list, memories: list) -> str:
    return f"MAA received your message: '{user_message}'"

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MAA Backend"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        memories = get_relevant_memories(request.user_id, request.message)
        context = retrieve_context(request.message)
        reply_text = get_llm_response(request.message, context, memories)
        
        return ChatResponse(
            reply=reply_text,
            session_id=request.session_id,
            sources=[c.get("source", "unknown") for c in context] if context else [],
            memory_updated=False
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Backend error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)