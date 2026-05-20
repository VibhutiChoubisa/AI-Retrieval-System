import pandas as pd


def analyze_failures(results, queries, k=5):
    """
    results: dict {query: [retrieved_urls]}
    queries: list of {query, relevant_docs}
    """

    rows = []

    for q in queries:
        query = q["query"]
        gold = set(q.get("relevant", []))

        retrieved = results.get(query, [])[:k]
        retrieved_set = set(retrieved)

        hit = len(gold.intersection(retrieved_set)) > 0

        rows.append({
            "query": query,
            "hit@5": int(hit),
            "retrieved": list(retrieved),
            "gold": list(gold),
            "miss_count": len(gold - retrieved_set)
        })

    df = pd.DataFrame(rows)

    return df


def categorize_failures(df):
    """
    Simple heuristics-based categorization
    """

    categories = []

    for _, row in df.iterrows():
        q = row["query"].lower()

        if "how" in q or "why" in q:
            categories.append("semantic / explanatory")
        elif len(q.split()) <= 3:
            categories.append("keyword / short query")
        elif "and" in q or "vs" in q:
            categories.append("multi-hop / compositional")
        else:
            categories.append("general")

    df["category"] = categories
    return df