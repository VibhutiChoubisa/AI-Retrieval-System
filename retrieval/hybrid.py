import time

from retrieval.dense import load_model, build_dense, search as dense_search
from retrieval.reranker import Reranker


class HybridRetriever:
    def __init__(self, bm25, docs):
        """
        True Hybrid Retrieval System

        Pipeline:
        1. BM25 retrieval
        2. Dense retrieval
        3. Merge candidate pools
        4. Cross-encoder reranking
        """

        self.bm25 = bm25
        self.docs = docs

        # -----------------------------
        # Dense retrieval components
        # -----------------------------
        self.dense_model = load_model()

        self.dense_index, _, self.dense_docs = build_dense(
            docs,
            self.dense_model
        )

        # -----------------------------
        # Cross-encoder reranker
        # -----------------------------
        self.reranker = Reranker()

    # -----------------------------------
    # BM25 retrieval
    # -----------------------------------
    def bm25_search(self, query, k=20):

        tokens = query.split()

        results = self.bm25.get_top_n(
            tokens,
            self.docs,
            n=k
        )

        return results

    # -----------------------------------
    # Dense retrieval
    # -----------------------------------
    def dense_search(self, query, k=20):

        results = dense_search(
            query,
            self.dense_model,
            self.dense_index,
            self.dense_docs,
            k=k
        )

        return results

    # -----------------------------------
    # Merge retrieval pools
    # -----------------------------------
    def merge_results(self, bm25_results, dense_results):

        merged = {}

        # BM25 results
        for doc in bm25_results:
            merged[doc["url"]] = doc

        # Dense results
        for doc in dense_results:
            merged[doc["url"]] = doc

        return list(merged.values())

    # -----------------------------------
    # Cross-encoder reranking
    # -----------------------------------
    def rerank(self, query, candidates, top_k=5):

        return self.reranker.rerank(
            query,
            candidates,
            top_k=top_k
        )

    # -----------------------------------
    # Main retrieval API
    # -----------------------------------
    def search(self, query, k=5, candidate_k=20):

        total_start = time.time()

        # -----------------------------------
        # Step 1: BM25 retrieval
        # -----------------------------------
        bm25_start = time.time()

        bm25_results = self.bm25_search(
            query,
            k=candidate_k
        )

        bm25_end = time.time()

        # -----------------------------------
        # Step 2: Dense retrieval
        # -----------------------------------
        dense_start = time.time()

        dense_results = self.dense_search(
            query,
            k=candidate_k
        )

        dense_end = time.time()

        # -----------------------------------
        # Step 3: Merge pools
        # -----------------------------------
        merge_start = time.time()

        candidates = self.merge_results(
            bm25_results,
            dense_results
        )

        merge_end = time.time()

        if not candidates:
            return []

        # -----------------------------------
        # Step 4: Cross-encoder reranking
        # -----------------------------------
        rerank_start = time.time()

        final_results = self.rerank(
            query,
            candidates,
            top_k=k
        )

        rerank_end = time.time()

        total_end = time.time()

        # -----------------------------------
        # Timing breakdown
        # -----------------------------------
        print("\n--- HYBRID TIMING BREAKDOWN ---")
        print(f"BM25 retrieval:   {bm25_end - bm25_start:.4f}s")
        print(f"Dense retrieval:  {dense_end - dense_start:.4f}s")
        print(f"Merge stage:      {merge_end - merge_start:.4f}s")
        print(f"Reranking stage:  {rerank_end - rerank_start:.4f}s")
        print(f"TOTAL:            {total_end - total_start:.4f}s")

        return final_results