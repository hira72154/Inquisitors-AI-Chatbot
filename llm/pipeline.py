from llm.llm_services import LLMService
from retrieval.retriever import Retriever


class MAAPipeline:
    """Connects retrieval with the MAA LLM service."""

    def __init__(self):
        self.retriever = Retriever(
            persist_dir="embeddings/chroma_db"
        )
        self.llm = LLMService()

    def answer(self, question: str, top_k: int = 3) -> str:
        """Retrieve relevant knowledge and generate an MAA response."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        # Step 1: Retrieve relevant knowledge
        results = self.retriever.retrieve(
            question,
            top_k=top_k
        )

        # Step 2: Build context for the LLM
        if results:
            context_parts = []

            for result in results:
                context_parts.append(
                    f"[Source: {result['source']}]\n"
                    f"[Section: {result['section']}]\n"
                    f"{result['text']}"
                )

            context = "\n\n".join(context_parts)

        else:
            context = (
                "No relevant information was found in the "
                "knowledge base."
            )

        # Step 3: Generate grounded MAA response
        return self.llm.generate_response(
            question=question,
            context=context,
            memories=""
        )