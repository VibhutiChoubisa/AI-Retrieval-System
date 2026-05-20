# Retrieval Benchmark System (BM25 + Dense + Hybrid + Reranker)

## 🚀 Overview

This project implements a **retrieval benchmarking framework** to compare classical, neural, and hybrid search systems under identical evaluation conditions.

It is designed as a **production-style IR evaluation pipeline**, not a toy experiment, and focuses on making **defensible trade-offs between accuracy, ranking quality, and latency**.

The system evaluates:

- BM25 (lexical retrieval baseline)
- Dense retrieval (Transformer embeddings + FAISS)
- Hybrid retrieval (BM25 + dense fusion)
- Hybrid + Cross-Encoder reranking

---

## 📂 Dataset

### 📄 Corpus
- 208 real-world technical documents
- Extracted from 210 source URLs

### Domains
- ROS 2 documentation
- MoveIt motion planning framework
- Gazebo simulation system
- Universal Robots (UR5) control stack

### 💡 Why this dataset?

This corpus was chosen because it:

- Contains **both structured and unstructured technical text**
- Requires **semantic + lexical matching**
- Includes **cross-system dependencies (ROS ↔ MoveIt ↔ Gazebo)**
- Reflects realistic **robotics + RAG workloads**

---

## ❓ Query Set

- 20 manually curated evaluation queries
- Includes:
  - Direct factual queries
  - Paraphrased queries
  - Multi-hop reasoning queries
  - Ambiguous “real user-like” queries

---

## 🧪 Retrieval Methods

### 1. BM25 (Baseline)
Classical lexical retrieval using token overlap scoring.

Strength:
- Fast
- Strong for keyword-heavy queries

---

### 2. Dense Retrieval
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- FAISS-based ANN index

Strength:
- Captures semantic similarity
- Handles paraphrasing better than BM25

---

### 3. Hybrid Retrieval
Weighted fusion of:
- BM25 lexical score
- Dense embedding similarity

Strength:
- Balances precision + semantic coverage
- More robust across query types

---

### 4. Hybrid + Cross-Encoder Reranker
- Candidate pool: top-20 hybrid results
- Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`

Strength:
- Significant precision improvement at top ranks

Trade-off:
- High computational latency

---

## 📊 Evaluation Metrics

All systems are evaluated using:

- Recall@5
- MRR (Mean Reciprocal Rank)
- p95 Latency

---

## 📈 Results Summary

| System                 | Recall@5 | MRR   | p95 Latency (s) |
|------------------------|----------|-------|-----------------|
| BM25                   | 0.75     | 0.407 | ~0.00           |
| Dense                  | 0.65     | 0.402 | 0.015–0.016     |
| Hybrid                 | 0.80     | 0.45  | ~0.01           |
| Hybrid + Reranker     | ↑ best   | 0.45+ | 0.8–0.9         |

---

## 🧠 Key Insights

- Hybrid retrieval provides the best **accuracy–latency trade-off**
- Dense retrieval struggles with **domain-specific tokens (ROS commands, UR scripts)**
- BM25 remains strong for **structured technical documentation**
- Reranking significantly improves MRR but **violates latency constraints**

---

## ⚙️ Reproducibility

This project is fully reproducible on a single machine.

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Build dataset
python data/raw/extract_docs.py
3. Run full evaluation
python -m evaluation.evaluate
📁 Outputs

After execution, the system generates:

results/
 ├── tradeoff.png
 ├── failure_dist.png
 ├── report.md
❌ Failure Analysis

The system still struggles with:

Multi-hop reasoning across documents
Ambiguous or underspecified queries
Cross-domain queries combining ROS + MoveIt + Gazebo

These highlight limitations of both lexical and embedding-based retrieval systems.

🧠 Engineering Highlights
Hybrid retrieval pipeline design
FAISS-based vector search
Cross-encoder reranking integration
Latency benchmarking (p95)
Automated evaluation framework
Failure taxonomy analysis
🔮 Future Improvements
Retrieval
Reciprocal Rank Fusion (RRF)
LLM-based query rewriting
Stronger embedding models (bge-large / e5-large)
Ranking
Lightweight reranker distillation
Caching cross-encoder inference
Evaluation
nDCG@k metrics
Statistical significance testing
Query clustering analysis
🏁 Conclusion

This project demonstrates a complete retrieval benchmarking pipeline combining:

Classical IR (BM25)
Neural retrieval (dense embeddings)
Hybrid fusion strategies
Cross-encoder reranking
Full evaluation + failure analysis

It closely mirrors real-world retrieval systems used in:

RAG pipelines
Enterprise search systems
Robotics knowledge assistants
⚙️ Reproducibility Note

All experiments can be reproduced using:

python -m evaluation.evaluate