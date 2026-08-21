# llm_services.py
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from .prompts import SYSTEM_PROMPT


load_dotenv()


class LLMService:
    """Handles LLM configuration and MAA response generation."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Add it to the .env file."
            )

        self.llm = ChatGroq(
            # model="llama-3.3-70b-versatile",
            model="openai/gpt-oss-20b",
            temperature=0.2,
            max_tokens=512,
            groq_api_key=api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "{question}"),
            ]
        )

        self.chain = self.prompt | self.llm

    def generate_response(
        self,
        question: str,
        context: str,
        memories: str = "",
    ) -> str:
        """
        Generate an MAA response using the provided
        knowledge-base context and optional memories.
        """

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not context.strip():
            raise ValueError("Context cannot be empty.")

        response = self.chain.invoke(
            {
                "question": question,
                "context": context,
                "memories": memories,
            }
        )

        answer = response.content.strip()

        if not answer:
            raise RuntimeError("LLM returned an empty response.")

        return answer