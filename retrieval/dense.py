import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_model():
    return SentenceTransformer(MODEL_NAME)


def build_dense(docs, model):
    """
    Builds FAISS index from document embeddings.
    Returns: index, embeddings, docs
    """
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])  # cosine via normalized vectors
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    return index, embeddings, docs


def search(query, model, index, docs, k=5):
    q_emb = model.encode([query])
    q_emb = np.array(q_emb).astype("float32")

    faiss.normalize_L2(q_emb)

    scores, indices = index.search(q_emb, k)

    return [docs[i] for i in indices[0]]