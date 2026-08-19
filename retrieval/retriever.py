import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

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
    
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.3
    ) -> List[Dict]:
        """
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