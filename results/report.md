# Retrieval Benchmark Report

## 1. System Overview

We evaluate three retrieval systems:
- BM25 (lexical baseline)
- Dense retrieval (semantic embeddings)
- Hybrid + cross-encoder reranking (two-stage system)

## 2. Key Results

### BM25
- Recall@5: 0.750
- MRR: 0.408
- p95 Latency: 0.000s


### DENSE
- Recall@5: 0.650
- MRR: 0.402
- p95 Latency: 0.016s


### HYBRID_k20
- Recall@5: 0.800
- MRR: 0.600
- p95 Latency: 4.123s


### HYBRID_k10
- Recall@5: 0.750
- MRR: 0.558
- p95 Latency: 2.135s


### HYBRID_k5
- Recall@5: 0.750
- MRR: 0.543
- p95 Latency: 0.426s

## 3. Key Insight

The best performing system is **HYBRID_k20** in terms of ranking quality (MRR).

However, latency-performance tradeoff shows that:
- BM25 is fastest but less semantically accurate
- Dense retrieval improves semantic matching
- Hybrid + reranking improves ranking quality but increases latency

## 4. Failure Analysis Summary

Common failure modes:
- Paraphrased queries reduce BM25 effectiveness
- Multi-hop queries reduce dense recall
- Hybrid improves ranking but depends heavily on candidate retrieval quality
