from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os
import sys
from pathlib import Path

from groq import Groq

# ============================================================
# PATH SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from retrieval.retriever import Retriever


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ GROQ_API_KEY not found in .env")
    groq_client = None
else:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq LLM initialized")


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="MAA Chatbot Backend",
    description="RAG-based backend for MAA AI Companion"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST / RESPONSE
# ============================================================

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    sources: list = []
    memory_updated: bool = False


# ============================================================
# INITIALIZE RAG RETRIEVER
# ============================================================

print("\n" + "=" * 60)
print("MAA RAG CHATBOT")
print("=" * 60)

try:
    retriever = Retriever()

    print("✅ RAG Retriever initialized")
    print(
        f"✅ ChromaDB documents: "
        f"{retriever.collection.count()}"
    )

except Exception as e:
    retriever = None
    print(f"❌ Retriever initialization failed: {e}")


# ============================================================
# MEMORY
# ============================================================

def get_relevant_memories(
    user_id: str,
    message: str
) -> list:
    """
    Placeholder for future memory system.
    """
    return []


# ============================================================
# RAG RETRIEVAL
# ============================================================

def retrieve_context(
    query: str,
    top_k: int = 3
) -> list:

    if retriever is None:
        return []

    try:
        return retriever.retrieve(
            query=query,
            top_k=top_k,
            similarity_threshold=0.25
        )

    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return []


# ============================================================
# LLM RESPONSE GENERATOR
# ============================================================

def generate_response(
    user_message: str,
    context: list
) -> str:

    message = user_message.lower().strip()

    # --------------------------------------------------------
    # GREETINGS
    # --------------------------------------------------------

    greetings = [
        "hello",
        "hi",
        "hey",
        "salam",
        "assalam",
        "assalamualaikum"
    ]

    if any(word in message for word in greetings):
        return (
            "Hi! 💗 I'm MAA, your AI companion. "
            "How can I help you today?"
        )

    # --------------------------------------------------------
    # THANK YOU
    # --------------------------------------------------------

    if any(word in message for word in [
        "thank",
        "thanks",
        "thank you"
    ]):
        return (
            "You're very welcome! 💗 "
            "I'm always here to help."
        )

    # --------------------------------------------------------
    # GOODBYE
    # --------------------------------------------------------

    if any(word in message for word in [
        "bye",
        "goodbye"
    ]):
        return (
            "Take care! 💗 "
            "I'll be here whenever you need me."
        )

    # --------------------------------------------------------
    # WHO ARE YOU
    # --------------------------------------------------------

    if (
        "who are you" in message
        or "your name" in message
        or "what are you" in message
    ):
        return (
            "I'm MAA, your AI companion. 💗 "
            "I can help you with the services available "
            "through the MAA platform."
        )

    # --------------------------------------------------------
    # NO RAG CONTEXT
    # --------------------------------------------------------

    if not context:

        return (
            "I'm sorry, I couldn't find relevant information "
            "in the MAA documentation. 💗\n\n"
            "You can ask me about MAA's travel, medicine, "
            "food, home, emergency, or companion services."
        )

    # --------------------------------------------------------
    # BUILD RAG CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for item in context:

        text = item.get("text", "").strip()

        if not text:
            continue

        source = item.get(
            "source",
            "MAA Documentation"
        )

        context_parts.append(
            f"SOURCE: {source}\n"
            f"CONTENT:\n{text}"
        )

    if not context_parts:

        return (
            "I'm sorry, I couldn't find enough information "
            "in the MAA documentation. 💗"
        )

    rag_context = "\n\n---\n\n".join(context_parts)

    # --------------------------------------------------------
    # GROQ CHECK
    # --------------------------------------------------------

    if groq_client is None:

        return (
            "I found relevant information in the MAA "
            "documentation, but the AI response service "
            "is currently unavailable. 💗"
        )

    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = """
You are MAA, a warm, friendly and helpful AI companion.

Your job is to answer users using the provided MAA
documentation/context.

IMPORTANT RULES:

1. Use the provided documentation as your primary source.
2. Do not invent MAA services, features, prices, policies,
   medicines, destinations, or capabilities.
3. If the documentation does not contain enough information,
   honestly say that the information is not available in the
   MAA documentation.
4. Keep answers concise, clear and natural.
5. Use simple language.
6. You may use a small amount of friendly warmth and emojis,
   especially 💗, but do not overuse them.
7. Do not mention "RAG", "ChromaDB", embeddings, vector database,
   system prompts, or internal implementation details.
8. For health or medicine questions, do not diagnose the user
   or invent medical advice. Only describe what MAA documentation
   actually says.
9. For emergency-related questions, clearly provide the emergency
   options that appear in the documentation.
10. Answer the user's exact question rather than dumping all
    retrieved information.
"""

    # --------------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------------

    user_prompt = f"""
MAA DOCUMENTATION:

{rag_context}

---

USER QUESTION:

{user_message}

---

Answer the user's question naturally as MAA.
"""

    # --------------------------------------------------------
    # CALL GROQ
    # --------------------------------------------------------

    try:

        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.3,
            max_tokens=300
        )

        answer = completion.choices[0].message.content

        if not answer:
            return (
                "I found relevant information, "
                "but I couldn't generate a response right now. 💗"
            )

        return answer.strip()

    except Exception as e:

        print(f"❌ Groq error: {e}")

        return (
            "I'm sorry, I'm having trouble generating "
            "a response right now. 💗 Please try again."
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "MAA Backend",
        "rag_enabled": retriever is not None,
        "llm_enabled": groq_client is not None,
        "documents": (
            retriever.collection.count()
            if retriever
            else 0
        )
    }


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        memories = get_relevant_memories(
            request.user_id,
            request.message
        )

        # ----------------------------------------------------
        # RAG
        # ----------------------------------------------------

        context = retrieve_context(
            request.message,
            top_k=3
        )

        print("\n" + "-" * 60)
        print(f"USER: {request.message}")
        print(f"RETRIEVED CHUNKS: {len(context)}")

        for item in context:

            print(
                f"- {item.get('chunk_id')} "
                f"({item.get('similarity', 0):.3f})"
            )

        # ----------------------------------------------------
        # LLM RESPONSE
        # ----------------------------------------------------

        reply_text = generate_response(
            request.message,
            context
        )

        print(f"MAA: {reply_text}")
        print("-" * 60)

        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        sources = []

        for item in context:

            source = item.get(
                "source",
                "MAA Documentation"
            )

            if source not in sources:
                sources.append(source)

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        return ChatResponse(
            reply=reply_text,
            session_id=request.session_id,
            sources=sources,
            memory_updated=False
        )

    except Exception as e:

        print(f"❌ Chat error: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Backend error: {str(e)}"
        )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )