from sentence_transformers import CrossEncoder
import numpy as np


class Reranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, candidates, top_k=5):
        if not candidates:
            return []

        texts = [c["text"] for c in candidates]
        pairs = [(query, t) for t in texts]

        # ⚡ batch inference (IMPORTANT FIX)
        scores = self.model.predict(pairs, batch_size=32)

        ranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [c for c, _ in ranked[:top_k]]