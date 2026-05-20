import json
import re
import numpy as np
from rank_bm25 import BM25Okapi

DATA_PATH = "data/processed/documents.json"

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return text.split()

def load_docs():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_bm25(docs):
    corpus = [tokenize(d["text"]) for d in docs]
    bm25 = BM25Okapi(corpus)
    return bm25, corpus

def search(query, bm25, docs, k=5):
    scores = bm25.get_scores(tokenize(query))
    top_idx = np.argsort(scores)[::-1][:k]
    return [docs[i] for i in top_idx]

if __name__ == "__main__":
    docs = load_docs()
    bm25 = build_bm25(docs)

    results = search("ros2 node tutorial", bm25, docs)

    for r in results:
        print(r["title"])