from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class EmbeddingGenerator:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print(
            f"Embedding model loaded. Dimensions: "
            f"{self.model.get_embedding_dimension()}"
        )

    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )