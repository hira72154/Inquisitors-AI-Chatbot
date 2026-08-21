# test_llm.py
from llm.llm_services import LLMService


SAMPLE_CONTEXT = """
MAA is an AI companion designed to provide helpful assistance across
different areas of everyday life.

MAA's website supports areas including food, medicine, travel,
and general assistance.

For food-related assistance, MAA can help users with food-related
information and suggestions based on the information available in
its knowledge base.

For travel-related assistance, MAA can provide travel information
and help users with travel-related questions when the relevant
information is available.

For medicine-related questions, MAA should provide information only
when it is supported by the available knowledge base and should be
careful about uncertainty.

MAA is designed to communicate in a warm, caring, friendly,
respectful, concise, and helpful manner.
"""


questions = [
    "What areas can MAA help with?",
    "Can MAA help me with travel-related questions?",
    "How should MAA handle medicine-related questions?",
    "Who created MAA?",
    "What is MAA's subscription price?",
    "I'm really excited about using MAA!",
    "I'm worried and frustrated. Can you help me?",
]


def main():
    llm = LLMService()

    for question in questions:
        print("\n" + "=" * 70)
        print(f"Question: {question}")

        try:
            answer = llm.generate_response(
                question=question,
                context=SAMPLE_CONTEXT,
                memories="",
            )

            print(f"Answer: {answer}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()