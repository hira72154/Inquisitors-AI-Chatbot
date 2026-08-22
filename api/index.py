# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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
    description="RAG + LLM based backend for MAA AI Companion"
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
    sources: list = Field(default_factory=list)
    memory_updated: bool = False


# ============================================================
# INITIALIZE RAG
# ============================================================

print("\n" + "=" * 60)
print("MAA AI COMPANION")
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

    print(
        f"❌ Retriever initialization failed: {e}"
    )


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
# QUERY TYPE DETECTION
# ============================================================

def detect_query_type(message: str) -> str:

    text = message.lower().strip()

    # --------------------------------------------------------
    # Normalize common punctuation
    # --------------------------------------------------------

    normalized = (
        text
        .replace("-", " ")
        .replace("_", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("!", "")
        .replace("?", "")
    )

    normalized = " ".join(normalized.split())

    # --------------------------------------------------------
    # GREETINGS
    # --------------------------------------------------------

    greeting_patterns = [
        "hello",
        "helo",
        "helloo",
        "hellooo",
        "hlo",
        "hy",
        "hyy",
        "hi",
        "hii",
        "hiii",
        "hey",
        "heyy",
        "heyyy",
        "salam",
        "salaam",
        "salam alaikum",
        "salaam alaikum",
        "assalamualaikum",
        "assalam o alaikum",
        "assalam o alikum",
        "asalamualaikum",
        "aslam o alaikum",
        "aoa",
        "a o a"
    ]

    if normalized in greeting_patterns:
        return "greeting"

    # --------------------------------------------------------
    # THANK YOU
    # --------------------------------------------------------

    thank_patterns = [
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "ty",
        "shukriya",
        "shukria"
    ]

    if normalized in thank_patterns:
        return "thanks"

    # --------------------------------------------------------
    # GOODBYE
    # --------------------------------------------------------

    goodbye_patterns = [
        "bye",
        "goodbye",
        "good bye",
        "allah hafiz",
        "khuda hafiz",
        "see you",
        "see ya"
    ]

    if normalized in goodbye_patterns:
        return "goodbye"

    # --------------------------------------------------------
    # URDU / ROMAN URDU
    # --------------------------------------------------------

    urdu_patterns = [
        "kia tmhy urdu ati ha",
        "kya tmhy urdu ati hai",
        "kya tumhein urdu aati hai",
        "kya tumhe urdu aati hai",
        "urdu ati hai",
        "urdu aati hai",
        "can you speak urdu",
        "do you speak urdu"
    ]

    if normalized in urdu_patterns:
        return "urdu"

    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------

    identity_patterns = [
        "who are you",
        "what are you",
        "what is your name",
        "your name",
        "who is maa",
        "what is maa",
        "tum kon ho",
        "aap kon hain"
    ]

    if any(
        phrase in normalized
        for phrase in identity_patterns
    ):
        return "identity"

    # --------------------------------------------------------
    # EMOTIONAL / WELLNESS
    # --------------------------------------------------------

    emotional_keywords = [
        "sad",
        "sadness",
        "unhappy",
        "upset",
        "crying",
        "cry",
        "lonely",
        "loneliness",
        "alone",
        "stressed",
        "stress",
        "anxious",
        "anxiety",
        "worried",
        "worry",
        "overwhelmed",
        "depressed",
        "feeling low",
        "feel low",
        "feeling bad",
        "not feeling good",
        "not okay",
        "not ok",
        "bad day",
        "hurt",
        "tired",
        "exhausted",
        "udaas",
        "pareshan",
        "tension",
        "tanha",
        "akela",
        "dukhi",
        "fever",
        "temperature",
        "i feel sick",
        "i am sick",
        "im sick"
    ]

    if any(
        word in normalized
        for word in emotional_keywords
    ):
        return "wellness"

    # --------------------------------------------------------
    # MAA SERVICE / DOCUMENTATION QUERY
    # --------------------------------------------------------

    service_keywords = [
        "maa service",
        "maa services",
        "maa provide",
        "maa offers",
        "maa offer",
        "maa help",
        "maa feature",
        "maa features",

        "service",
        "services",
        "provide",
        "provides",
        "offers",
        "offer",
        "available",

        "travel assistance",
        "travel",
        "trip",
        "flight",
        "hotel",
        "destination",
        "destinations",

        "food services",
        "food service",
        "food",
        "meal",
        "meals",
        "grocery",
        "groceries",
        "home made food",
        "homemade food",

        "medicine",
        "medicines",
        "medication",
        "health service",
        "health services",
        "health assistance",

        "emergency",
        "emergency support",
        "assistance",
        "account",
        "registration",
        "login",
        "profile"
    ]

    if any(
        keyword in normalized
        for keyword in service_keywords
    ):
        return "maa_service"

    # --------------------------------------------------------
    # GENERAL CONVERSATION
    # --------------------------------------------------------

    return "general"


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

        results = retriever.retrieve(
            query=query,
            top_k=top_k,
            similarity_threshold=0.30
        )

        filtered_results = []

        for item in results:

            similarity = float(
                item.get("similarity", 0)
            )

            if similarity >= 0.30:
                filtered_results.append(item)

        return filtered_results

    except Exception as e:

        print(
            f"❌ Retrieval error: {e}"
        )

        return []


# ============================================================
# DIRECT CONVERSATION
# ============================================================

def direct_response(message: str):

    """
    Handles simple conversational messages before RAG.
    """

    message_lower = message.lower().strip()

    # ========================================================
    # GREETINGS
    # ========================================================

    greeting_patterns = [
        "hello",
        "helo",
        "helloo",
        "hellooo",
        "hlo",
        "hy",
        "hyy",
        "hi",
        "hii",
        "hiii",
        "hey",
        "heyy",
        "heyyy",
        "salam",
        "salaam",
        "assalamualaikum",
        "assalam o alaikum",
        "assalam o alikum",
        "asalamualaikum",
        "aslam o alaikum",
        "aoa"
    ]

    if message_lower in greeting_patterns:

        return (
            "Hello! 💗 I'm MAA, your AI companion. "
            "How are you doing today?"
        )

    # ========================================================
    # THANK YOU
    # ========================================================

    thank_you_patterns = [
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "shukriya",
        "shukria",
        "ty"
    ]

    if message_lower in thank_you_patterns:

        return (
            "You're very welcome! 💗 "
            "I'm always happy to help."
        )

    # ========================================================
    # GOODBYE
    # ========================================================

    goodbye_patterns = [
        "bye",
        "goodbye",
        "good bye",
        "allah hafiz",
        "khuda hafiz",
        "see you",
        "see ya"
    ]

    if message_lower in goodbye_patterns:

        return (
            "Take care! 💗 "
            "I'll be here whenever you need me."
        )

    # ========================================================
    # URDU
    # ========================================================

    urdu_patterns = [
        "kia tmhy urdu ati ha",
        "kya tmhy urdu ati hai",
        "kya tumhein urdu aati hai",
        "kya tumhe urdu aati hai",
        "urdu ati hai",
        "urdu aati hai",
        "can you speak urdu",
        "do you speak urdu"
    ]

    if message_lower in urdu_patterns:

        return (
            "جی ہاں! 💗 میں اردو، رومن اردو اور انگریزی "
            "سمجھ سکتا ہوں۔ آپ جس زبان میں بات کرنا چاہیں، "
            "اسی میں مجھ سے بات کر سکتے ہیں۔"
        )

    # ========================================================
    # WHO ARE YOU
    # ========================================================

    if (
        "who are you" in message_lower
        or "what are you" in message_lower
        or "your name" in message_lower
        or "tum kon ho" in message_lower
        or "aap kon hain" in message_lower
    ):

        return (
            "I'm MAA, your AI companion. 💗 "
            "You can talk to me about MAA's services, "
            "ask questions, or simply chat with me."
        )

    return None


# ============================================================
# CONVERSATIONAL LLM
# ============================================================

def generate_conversational_response(
    user_message: str
) -> str:

    if groq_client is None:

        return (
            "I'm here with you. 💗 "
            "My AI service is temporarily unavailable."
        )

    system_prompt = """
You are MAA, a warm, friendly and intelligent AI companion.

This is CASUAL CONVERSATION mode.

You can naturally respond to:

- greetings
- typos
- short messages
- casual conversation
- emotional messages
- small talk
- Roman Urdu
- Urdu
- English
- statements such as "I am good"
- statements such as "I am tired"
- statements such as "I want to eat something"
- "favorite"
- "I love you"
- "I don't want to study"

IMPORTANT:

Do NOT use MAA documentation for ordinary conversation.

Do NOT invent MAA services during casual conversation.

Be natural and concise.

If the user says they are tired, sad, stressed, lonely,
worried or upset, respond with empathy.

If the user mentions a health problem such as fever:

- do not diagnose
- do not prescribe medicine
- do not provide dosage
- do not give treatment instructions
- respond empathetically
- say that you cannot provide medical guidance from
  the available MAA information

Never claim to be human.

Do not mention RAG, ChromaDB, embeddings,
vector databases or internal implementation.

If the user uses Roman Urdu, you may reply in Roman Urdu.

Keep the response warm and conversational.
"""

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
                    "content": user_message
                }
            ],

            temperature=0.7,
            max_tokens=250
        )

        answer = completion.choices[0].message.content

        if not answer:

            return (
                "I'm here with you. 💗 "
                "Tell me what's on your mind."
            )

        return answer.strip()

    except Exception as e:

        print(
            f"❌ Conversational LLM error: {e}"
        )

        return (
            "I'm here with you. 💗 "
            "Tell me what's on your mind."
        )


# ============================================================
# RAG + LLM RESPONSE
# ============================================================

def generate_rag_response(
    user_message: str,
    context: list
) -> str:

    # --------------------------------------------------------
    # GROQ CHECK
    # --------------------------------------------------------

    if groq_client is None:

        return (
            "I'm sorry, my AI service is temporarily "
            "unavailable. Please try again. 💗"
        )

    # --------------------------------------------------------
    # NO CONTEXT
    # --------------------------------------------------------

    if not context:

        return (
            "I'm sorry, I couldn't find relevant information "
            "about that in the MAA documentation. 💗"
        )

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for item in context:

        text = item.get(
            "text",
            ""
        ).strip()

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
            "about that in the MAA documentation. 💗"
        )

    rag_context = "\n\n---\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = """
You are MAA, a warm, friendly and helpful AI companion.

This is MAA KNOWLEDGE mode.

The user is asking about an actual MAA service,
feature or documented capability.

The provided documentation is the ONLY source of truth.

RULES:

1. Answer the exact user question.

2. Use ONLY the provided MAA documentation for
   MAA-specific factual claims.

3. Paraphrase naturally.

4. Do not copy documentation word-for-word.

5. NEVER invent:

   - services
   - features
   - prices
   - fees
   - doctors
   - medicines
   - destinations
   - emergency numbers
   - policies
   - bookings
   - capabilities

6. If the documentation does not answer the question,
   clearly say that the information is not available
   in the MAA documentation.

7. Do not add unrelated information.

8. If the user asks:
   "What services does MAA provide?"
   summarize the documented MAA services.

9. If the user asks:
   "Tell me about Travel Assistance"
   summarize ONLY the documented Travel Assistance
   information.

10. If the user asks about food services, use ONLY
    documented food-service information.

11. If the user asks a medical question, do not diagnose,
    prescribe medicine or invent treatment.

12. Keep answers concise.

13. Use simple language.

14. A small number of emojis is okay.

15. Never mention:

    - RAG
    - ChromaDB
    - embeddings
    - vector database
    - retrieval
    - system prompt
    - internal implementation
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

Answer the user's question using ONLY the
MAA documentation above.

If the documentation does not contain the answer,
say that the information is not available in the
MAA documentation.

Do not invent information.
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
            max_tokens=350
        )

        answer = completion.choices[0].message.content

        if not answer:

            return (
                "I found information about that, "
                "but I couldn't generate a response right now. 💗"
            )

        return answer.strip()

    except Exception as e:

        print(
            f"❌ Groq RAG error: {e}"
        )

        return (
            "I'm sorry, I'm having trouble generating "
            "a response right now. 💗 Please try again."
        )


# ============================================================
# MAIN RESPONSE ROUTER
# ============================================================

def generate_response(
    user_message: str,
    context: list
) -> str:

    # ========================================================
    # 1. DIRECT RESPONSE
    # ========================================================

    direct = direct_response(
        user_message
    )

    if direct:

        return direct

    # ========================================================
    # 2. QUERY TYPE
    # ========================================================

    query_type = detect_query_type(
        user_message
    )

    print(
        f"QUERY TYPE: {query_type}"
    )

    # ========================================================
    # 3. CASUAL / EMOTIONAL CONVERSATION
    # ========================================================

    if query_type in [
        "greeting",
        "thanks",
        "goodbye",
        "urdu",
        "identity",
        "wellness",
        "general"
    ]:

        return generate_conversational_response(
            user_message
        )

    # ========================================================
    # 4. MAA KNOWLEDGE QUESTION
    # ========================================================

    if query_type == "maa_service":

        return generate_rag_response(
            user_message,
            context
        )

    # ========================================================
    # 5. FALLBACK
    # ========================================================

    return generate_conversational_response(
        user_message
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
        # QUERY TYPE
        # ----------------------------------------------------

        query_type = detect_query_type(
            request.message
        )

        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        print("\n" + "-" * 60)

        print(
            f"USER: {request.message}"
        )

        print(
            f"QUERY TYPE: {query_type}"
        )

        # ----------------------------------------------------
        # DIRECT RESPONSE
        # ----------------------------------------------------

        direct = direct_response(
            request.message
        )

        # ----------------------------------------------------
        # RAG ONLY FOR MAA QUESTIONS
        # ----------------------------------------------------

        context = []

        if (
            direct is None
            and query_type == "maa_service"
        ):

            context = retrieve_context(
                request.message,
                top_k=3
            )

        # ----------------------------------------------------
        # RETRIEVAL LOGS
        # ----------------------------------------------------

        print(
            f"RETRIEVED CHUNKS: {len(context)}"
        )

        for item in context:

            similarity = float(
                item.get(
                    "similarity",
                    0
                )
            )

            print(
                f"- {item.get('chunk_id')} "
                f"(similarity: {similarity:.3f})"
            )

        # ----------------------------------------------------
        # GENERATE RESPONSE
        # ----------------------------------------------------

        reply_text = generate_response(
            request.message,
            context
        )

        print(
            f"MAA: {reply_text}"
        )

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
        # RESPONSE
        # ----------------------------------------------------

        return ChatResponse(

            reply=reply_text,

            session_id=request.session_id,

            sources=sources,

            memory_updated=False
        )

    except Exception as e:

        print(
            f"❌ Chat error: {e}"
        )

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