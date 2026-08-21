
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize embedding model."""
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Model loaded. Dimensions: {self.model.get_sentence_embedding_dimension()}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Turn text into a vector."""
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Turn multiple texts into vectors."""
        return [e for e in self.model.encode(texts, convert_to_numpy=True)]