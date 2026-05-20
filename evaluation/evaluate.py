import json
import time
import os

from retrieval.bm25_baseline import load_docs, build_bm25, search as bm25_search
from retrieval.dense import load_model, build_dense, search as dense_search
from retrieval.hybrid import HybridRetriever

from evaluation.metrics import evaluate_all
from evaluation.plots import plot_retrieval_tradeoff, plot_failure_distribution
from evaluation.failure_analysis import analyze_failures, categorize_failures
from evaluation.report import generate_report


QUERIES_PATH = "queries/benchmark_queries.json"


# ----------------------------
# Utils
# ----------------------------
def load_queries():
    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(url):
    if not isinstance(url, str):
        return ""
    return url.strip().lower().rstrip("/")


def standardize_queries(queries):
    return [
        {
            "query": q["query"],
            "relevant": q.get("relevant", q.get("relevant_urls", []))
        }
        for q in queries
    ]


def compute_p95(latencies):
    if not latencies:
        return 0.0
    latencies = sorted(latencies)
    idx = int(0.95 * len(latencies))
    return latencies[min(idx, len(latencies) - 1)]


# ----------------------------
# Core evaluator
# ----------------------------
def run_retrieval(name, search_fn, queries):
    print(f"\n=== {name} EVALUATION ===")

    results = {}
    latencies = []

    for q in queries:
        start = time.time()
        retrieved = search_fn(q["query"])
        end = time.time()

        results[q["query"]] = [normalize(d["url"]) for d in retrieved]
        latencies.append(end - start)

    metrics = evaluate_all(results, queries)
    metrics["p95_latency"] = compute_p95(latencies)

    print(json.dumps(metrics, indent=2))

    return {
        "recall": metrics["Recall@5"],
        "mrr": metrics["MRR"],
        "latency": metrics["p95_latency"]
    }


# ----------------------------
# BM25
# ----------------------------
def run_bm25(docs, queries):
    bm25, _ = build_bm25(docs)

    def search(query):
        return bm25_search(query, bm25, docs, k=5)

    return run_retrieval("BM25", search, queries)


# ----------------------------
# DENSE
# ----------------------------
def run_dense(docs, model, queries):
    index, embeddings, dense_docs = build_dense(docs, model)

    def search(query):
        return dense_search(query, model, index, dense_docs, k=5)

    return run_retrieval("DENSE", search, queries)


# ----------------------------
# HYBRID progressive sweep
# ----------------------------
def run_hybrid_progressive(docs, bm25, queries, candidate_ks=(20, 10, 5)):
    results_summary = {}

    for candidate_k in candidate_ks:
        print("\n" + "=" * 60)
        print(f"HYBRID candidate_k = {candidate_k}")
        print("=" * 60)

        hybrid = HybridRetriever(bm25, docs)

        def search(query):
            return hybrid.search(query, k=5, candidate_k=candidate_k)

        results_summary[f"HYBRID_k{candidate_k}"] = run_retrieval(
            f"HYBRID (candidate_k={candidate_k})",
            search,
            queries
        )

    return results_summary


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    os.makedirs("results", exist_ok=True)

    print("\nLoading data...")
    docs = load_docs()
    queries = standardize_queries(load_queries())

    print("Loading BM25...")
    bm25, _ = build_bm25(docs)

    print("Loading Dense model...")
    model = load_model()

    # ----------------------------
    # Run baseline systems
    # ----------------------------
    bm25_res = run_bm25(docs, queries)
    dense_res = run_dense(docs, model, queries)

    # ----------------------------
    # Progressive hybrid evaluation
    # ----------------------------
    hybrid_res = run_hybrid_progressive(docs, bm25, queries)

    # Merge summary
    summary = {
        "BM25": bm25_res,
        "DENSE": dense_res,
        **hybrid_res
    }

    print("\n=== SUMMARY TABLE ===")
    print(json.dumps(summary, indent=2))

    # ----------------------------
    # Plot tradeoff
    # ----------------------------
    plot_retrieval_tradeoff(summary, save_path="results/tradeoff.png")

    # ----------------------------
    # Failure analysis (best hybrid = k5)
    # ----------------------------
    print("\n=== FAILURE ANALYSIS (HYBRID k=5) ===")

    hybrid = HybridRetriever(bm25, docs)
    results = {}

    for q in queries:
        retrieved = hybrid.search(q["query"], k=5, candidate_k=5)
        results[q["query"]] = [normalize(d["url"]) for d in retrieved]

    failure_df = analyze_failures(results, queries)
    failure_df = categorize_failures(failure_df)

    plot_failure_distribution(failure_df, "results/failure_dist.png")

    # ----------------------------
    # Report generation
    # ----------------------------
    report = generate_report(summary, failure_df)

    with open("results/report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n✅ Report saved to results/report.md")
    print("✅ Plots saved to results/")