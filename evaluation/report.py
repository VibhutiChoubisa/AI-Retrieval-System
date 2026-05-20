def generate_report(summary, failure_df):
    report = []

    report.append("# Retrieval Benchmark Report\n")

    report.append("## 1. System Overview")
    report.append("""
We evaluate three retrieval systems:
- BM25 (lexical baseline)
- Dense retrieval (semantic embeddings)
- Hybrid + cross-encoder reranking (two-stage system)
""")

    report.append("## 2. Key Results")

    for model, m in summary.items():
        report.append(f"""
### {model}
- Recall@5: {m['recall']:.3f}
- MRR: {m['mrr']:.3f}
- p95 Latency: {m['latency']:.3f}s
""")

    report.append("## 3. Key Insight")

    best_model = max(summary.items(), key=lambda x: x[1]["mrr"])[0]

    report.append(f"""
The best performing system is **{best_model}** in terms of ranking quality (MRR).

However, latency-performance tradeoff shows that:
- BM25 is fastest but less semantically accurate
- Dense retrieval improves semantic matching
- Hybrid + reranking improves ranking quality but increases latency
""")

    report.append("## 4. Failure Analysis Summary")

    report.append("""
Common failure modes:
- Paraphrased queries reduce BM25 effectiveness
- Multi-hop queries reduce dense recall
- Hybrid improves ranking but depends heavily on candidate retrieval quality
""")

    return "\n".join(report)