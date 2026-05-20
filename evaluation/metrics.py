import numpy as np


def normalize(url):
    if not isinstance(url, str):
        return ""
    return url.strip().lower().rstrip("/")


def recall_at_k(retrieved, relevant, k=5):

    retrieved_k = [normalize(x) for x in retrieved[:k]]
    relevant = [normalize(x) for x in relevant]

    return int(any(doc in relevant for doc in retrieved_k))


def reciprocal_rank(retrieved, relevant):

    retrieved = [normalize(x) for x in retrieved]
    relevant = [normalize(x) for x in relevant]

    for i, doc in enumerate(retrieved):
        if doc in relevant:
            return 1 / (i + 1)

    return 0.0


def evaluate_all(results, queries):

    recall_scores = []
    mrr_scores = []

    for q in queries:

        retrieved = results[q["query"]]

        relevant = (
            q.get("relevant")
            or q.get("relevant_urls")
            or []
        )

        recall_scores.append(
            recall_at_k(retrieved, relevant, k=5)
        )

        mrr_scores.append(
            reciprocal_rank(retrieved, relevant)
        )

    return {
        "Recall@5": np.mean(recall_scores),
        "MRR": np.mean(mrr_scores)
    }