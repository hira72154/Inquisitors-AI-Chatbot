import chromadb
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict


# ============================================================
# EMBEDDING GENERATOR
# ============================================================

class EmbeddingGenerator:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print(
            f"Embedding model loaded. "
            f"Dimensions: {self.model.get_embedding_dimension()}"
        )

    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(
            text,
            convert_to_numpy=True
        )


# ============================================================
# RETRIEVER
# ============================================================

class Retriever:

    def __init__(self, persist_dir: str | None = None):

        print("Initializing Retriever...")

        project_root = Path(__file__).resolve().parent.parent

        if persist_dir is None:
            persist_dir = (
                project_root
                / "embeddings"
                / "chroma_db"
            )

        self.persist_dir = str(persist_dir)

        print(
            f"ChromaDB path: {self.persist_dir}"
        )

        self.embedder = EmbeddingGenerator()

        self.client = chromadb.PersistentClient(
            path=self.persist_dir
        )

        self.collection = self.client.get_or_create_collection(
            name="maa_knowledge"
        )

        print(
            f"Retriever ready. "
            f"Documents in collection: "
            f"{self.collection.count()}"
        )

    # ========================================================
    # CATEGORY DETECTION
    # ========================================================

    def _detect_category(self, query: str) -> str:

        query_lower = query.lower()

        categories = {

            "medicine": [
                "medicine",
                "medicines",
                "medication",
                "medications",
                "drug",
                "drugs",
                "tablet",
                "tablets",
                "prescription",
                "paracetamol",
                "vitamin",
                "cetirizine",
                "pharmacy"
            ],

            "food": [
                "food",
                "meal",
                "meals",
                "cooking",
                "cook",
                "cooks",
                "homemade",
                "home-made",
                "restaurant",
                "dish",
                "dishes",
                "cuisine",
                "grocery",
                "groceries",
                "grocer",
                "shopping",
                "ingredients"
            ],

            "travel": [
                "travel",
                "trip",
                "trips",
                "flight",
                "flights",
                "hotel",
                "hotels",
                "destination",
                "tour",
                "journey",
                "airport",
                "booking"
            ],

            "emergency": [
                "emergency",
                "urgent",
                "urgently",
                "crisis",
                "danger",
                "help now",
                "immediate"
            ],

            "wellness": [
                "stress",
                "stressed",
                "anxiety",
                "anxious",
                "sad",
                "sadness",
                "overwhelmed",
                "worried",
                "worry",
                "lonely",
                "loneliness",
                "upset",
                "calm",
                "relax",
                "relaxation",
                "breathing",
                "breathe",
                "mental",
                "feeling",
                "feelings"
            ],

            "ai": [
                "ai",
                "assistant",
                "companion",
                "chat",
                "talk to maa",
                "conversation"
            ]
        }

        for category, keywords in categories.items():

            for keyword in keywords:

                if keyword in query_lower:
                    return category

        return ""

    # ========================================================
    # CATEGORY DOCUMENT MATCHING
    # ========================================================

    def _category_matches(
        self,
        metadata: Dict,
        category: str
    ) -> bool:

        if not category:
            return False

        doc_id = str(
            metadata.get("doc_id", "")
        ).lower()

        source = str(
            metadata.get("source", "")
        ).lower()

        section = str(
            metadata.get("section", "")
        ).lower()

        combined = (
            doc_id
            + " "
            + source
            + " "
            + section
        )

        # Direct category match
        if category in combined:
            return True

        # Wellness can be represented by health-related docs
        if category == "wellness":

            wellness_terms = [
                "wellness",
                "health",
                "mental",
                "mind",
                "emotional",
                "care",
                "support"
            ]

            return any(
                term in combined
                for term in wellness_terms
            )

        # Food can be represented by home-related docs
        if category == "food":

            food_terms = [
                "food",
                "home",
                "meal",
                "grocery",
                "cook"
            ]

            return any(
                term in combined
                for term in food_terms
            )

        return False

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 2,
        similarity_threshold: float = 0.35
    ) -> List[Dict]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if self.collection.count() == 0:
            return []

        # ----------------------------------------------------
        # 1. EMBED QUERY
        # ----------------------------------------------------

        query_embedding = self.embedder.embed_text(
            query
        )

        query_embedding_list = (
            query_embedding.tolist()
        )

        # ----------------------------------------------------
        # 2. SEARCH CHROMADB
        # ----------------------------------------------------

        n_results = min(
            10,
            self.collection.count()
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding_list
            ],
            n_results=n_results
        )

        if (
            not results.get("ids")
            or not results["ids"][0]
        ):
            return []

        # ----------------------------------------------------
        # 3. DETECT CATEGORY
        # ----------------------------------------------------

        category = self._detect_category(
            query
        )

        # ----------------------------------------------------
        # 4. QUERY WORDS
        # ----------------------------------------------------

        query_words = set(
            word.strip(".,!?;:'\"()[]{}")
            for word in query.lower().split()
        )

        query_words = {
            word
            for word in query_words
            if len(word) > 3
        }

        # ----------------------------------------------------
        # 5. BUILD CANDIDATES
        # ----------------------------------------------------

        candidates = []

        for i in range(
            len(results["ids"][0])
        ):

            chunk_id = results["ids"][0][i]

            distance = float(
                results["distances"][0][i]
            )

            similarity = 1 - distance

            metadata = (
                results["metadatas"][0][i]
                or {}
            )

            text = (
                results["documents"][0][i]
                or ""
            ).strip()

            if not text:
                continue

            # ------------------------------------------------
            # HARD SIMILARITY FILTER
            # ------------------------------------------------

            if similarity < similarity_threshold:
                continue

            # ------------------------------------------------
            # CATEGORY MATCH
            # ------------------------------------------------

            category_match = False

            if category:

                category_match = self._category_matches(
                    metadata,
                    category
                )

            # ------------------------------------------------
            # KEYWORD MATCH
            # ------------------------------------------------

            text_lower = text.lower()

            keyword_matches = sum(
                1
                for word in query_words
                if word in text_lower
            )

            keyword_boost = min(
                keyword_matches * 0.02,
                0.08
            )

            # ------------------------------------------------
            # FINAL SCORE
            # ------------------------------------------------

            score = similarity

            # Small category boost
            if category_match:
                score += 0.08

            # Small keyword boost
            score += keyword_boost

            # ------------------------------------------------
            # STORE
            # ------------------------------------------------

            candidates.append({

                "chunk_id": chunk_id,

                "text": text,

                "source": metadata.get(
                    "source",
                    "MAA Knowledge Base"
                ),

                "section": metadata.get(
                    "section",
                    "general"
                ),

                "doc_id": metadata.get(
                    "doc_id",
                    ""
                ),

                "similarity": float(
                    similarity
                ),

                "score": float(
                    score
                ),

                "category": category,

                "category_match": category_match,

                "keyword_matches": keyword_matches
            })

        # ----------------------------------------------------
        # 6. NO RELEVANT RESULTS
        # ----------------------------------------------------

        if not candidates:
            return []

        # ----------------------------------------------------
        # 7. SORT
        # ----------------------------------------------------

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # ----------------------------------------------------
        # 8. RETURN ONLY STRONGEST RESULTS
        # ----------------------------------------------------

        final_results = []

        for candidate in candidates:

            # Don't allow extremely weak matches
            if candidate["similarity"] < 0.35:
                continue

            final_results.append(candidate)

            if len(final_results) >= top_k:
                break

        # ----------------------------------------------------
        # 9. RETURN
        # ----------------------------------------------------

        return final_results


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    retriever = Retriever()

    test_queries = [

        "How do I plan a trip?",

        "What food services are available?",

        "I need medicine",

        "Can MAA help me with emergency travel?",

        "I am feeling stressed",

        "Can you help me with groceries?"
    ]

    for query in test_queries:

        print("\n" + "=" * 60)

        print(
            f"Query: {query}"
        )

        print("=" * 60)

        try:

            results = retriever.retrieve(
                query,
                top_k=2,
                similarity_threshold=0.35
            )

            if not results:

                print(
                    "No relevant documentation found."
                )

                continue

            for result in results:

                print(
                    f"\nChunk: "
                    f"{result['chunk_id']}"
                )

                print(
                    f"Category: "
                    f"{result['category']}"
                )

                print(
                    f"Category Match: "
                    f"{result['category_match']}"
                )

                print(
                    f"Similarity: "
                    f"{result['similarity']:.3f}"
                )

                print(
                    f"Score: "
                    f"{result['score']:.3f}"
                )

                print(
                    f"Keywords: "
                    f"{result['keyword_matches']}"
                )

                print(
                    f"Source: "
                    f"{result['source']}"
                )

                print(
                    f"Text: "
                    f"{result['text'][:250]}..."
                )

        except Exception as error:

            print(
                f"Retrieval error: {error}"
            )