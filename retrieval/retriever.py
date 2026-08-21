import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
llm
from typing import List, Dict


class EmbeddingGenerator:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        print(f"Loading model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print(
            f"✅ Model loaded. Dimensions: "
            f"{self.model.get_sentence_embedding_dimension()}"
        )

    def embed_text(self, text: str) -> np.ndarray:
        """Convert text into an embedding vector."""
        return self.model.encode(
            text,
            convert_to_numpy=True
        )


class Retriever:
    """Search the ChromaDB database for relevant chunks."""

    def __init__(
        self,
        persist_dir: str = "../embeddings/chroma_db"
    ):
        print("Initializing Retriever...")

        self.embedder = EmbeddingGenerator()

        self.client = chromadb.PersistentClient(
            path=persist_dir
        )

        self.collection = self.client.get_or_create_collection(
            name="maa_knowledge"
        )

        print("✅ Retriever ready")

    def _detect_category(self, query: str) -> str:
        """
        Detect the main MAA service category from the query.
        """

        query_lower = query.lower()

        category_keywords = {
            "medicine": [
                "medicine",
                "medicines",
                "medication",
                "medications",
                "drug",
                "drugs",
                "health",
                "tablet",
                "tablets",
                "prescription",
                "prescriptions",
                "paracetamol",
                "vitamin",
                "cetirizine"
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
                "restaurant"
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
                "destinations",
                "tour"
            ],

            "emergency": [
                "emergency",
                "urgent",
                "urgently",
                "crisis",
                "help now"
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

        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return category

        return ""



class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Model loaded. Dimensions: {self.model.get_sentence_embedding_dimension()}")
    
    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)
from typing import List, Dict

class Retriever:
    """Search the ChromaDB database for relevant chunks."""
    
    def __init__(self, persist_dir: str = "../embeddings/chroma_db"):
        """
        Initialize retriever.
        """
        print("Initializing Retriever...")
        self.embedder = EmbeddingGenerator()
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="maa_knowledge")
        print("✅ Retriever ready")
    
 main
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.3
    ) -> List[Dict]:
        """
 llm
        Retrieve relevant chunks using semantic similarity
        plus category-aware boosting.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        # --------------------------------------------------
        # Step 1: Embed query
        # --------------------------------------------------

        query_embedding = self.embedder.embed_text(query)
        query_embedding_list = query_embedding.tolist()

        # --------------------------------------------------
        # Step 2: Retrieve candidates
        # --------------------------------------------------

        results = self.collection.query(
            query_embeddings=[query_embedding_list],
            n_results=10
        )

        # --------------------------------------------------
        # Step 3: Detect service category
        # --------------------------------------------------

        category = self._detect_category(query)

        # --------------------------------------------------
        # Step 4: Build matched chunks
        # --------------------------------------------------

        matched_chunks = []

        for i in range(len(results["ids"][0])):

            chunk_id = results["ids"][0][i]
            distance = results["distances"][0][i]

            similarity = 1 - distance

            metadata = results["metadatas"][0][i]

            doc_id = metadata.get(
                "doc_id",
                ""
            )

            # --------------------------------------------------
            # Category boost
            # --------------------------------------------------

            boosted_similarity = similarity

            if category:
                expected_doc_id = f"{category}_001"

                if doc_id == expected_doc_id:
                    boosted_similarity += 0.20

            # --------------------------------------------------
            # Threshold applies to original similarity
            # --------------------------------------------------

            if similarity >= similarity_threshold:

                matched_chunks.append({
                    "chunk_id": chunk_id,
                    "text": results["documents"][0][i],
                    "source": metadata.get(
                        "source",
                        "unknown"
                    ),
                    "section": metadata.get(
                        "section",
                        "general"
                    ),
                    "similarity": float(similarity),
                    "score": float(boosted_similarity)
                })

        # --------------------------------------------------
        # Step 5: Sort by boosted score
        # --------------------------------------------------

        matched_chunks.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # --------------------------------------------------
        # Step 6: Return top results
        # --------------------------------------------------

        return matched_chunks[:top_k]


if __name__ == "__main__":

    retriever = Retriever()

    test_queries = [
        "How do I plan a trip?",
        "What food services are available?",
        "I need medicine",
        "Can MAA help me with emergency travel?"
    ]

    for q in test_queries:

        print(f"\n🔍 Query: '{q}'")

        results = retriever.retrieve(
            q,
            top_k=3
        )

        for r in results:

            print(
                f"  - {r['chunk_id']} "
                f"(similarity: {r['similarity']:.2f}, "
                f"score: {r['score']:.2f})"
            )
        Search for chunks similar to the query.    ]
        """
        
        # Embed the query
        query_embedding = self.embedder.embed_text(query)
        query_embedding_list = query_embedding.tolist()
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding_list],
            n_results=top_k
        )
        
    
        matched_chunks = []
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            similarity = 1 - distance
            
            if similarity >= similarity_threshold:
                matched_chunks.append({
                    'chunk_id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'source': results['metadatas'][0][i].get('source', 'unknown'),
                    'section': results['metadatas'][0][i].get('section', 'general'),
                    'similarity': float(similarity)
                })
        
        return matched_chunks


if __name__ == "__main__":
    retriever = Retriever()
    
    test_queries = [
        "How do I plan a trip?",
        "What food services are available?",
        "I need medicine"
    ]
    
    for q in test_queries:
        print(f"\n🔍 Query: '{q}'")
        results = retriever.retrieve(q, top_k=2)
        for r in results:
            print(f"  - {r['chunk_id']} (similarity: {r['similarity']:.2f})")
