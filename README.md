# Retrieval Benchmark System (BM25 + Dense + Hybrid + Reranker)

## 🎯 Why I chose Assignment 1 (Retrieval Benchmarking)

I selected **Assignment 1: Retrieval, Honest Comparison** over the Agent (Assignment 2) and Context Compression (Assignment 3) because it best matches both the **engineering problem structure of real-world retrieval systems** and the **type of evaluation I wanted to demonstrate: measurable, controllable, and failure-driven comparison across architectures**.

---

### 🧠 Why not Assignment 2 (Agent + Tools)

While agent-based systems are powerful, they introduce multiple confounding variables:

- LLM-driven tool selection adds stochastic behavior unrelated to retrieval quality
- Failures often come from **prompting or tool routing**, not system design
- Evaluation becomes harder to isolate and less reproducible

I wanted a problem where:
> system differences are architectural, not prompt-dependent

Retrieval systems provide that clarity — BM25 vs Dense vs Hybrid is a **clean controlled comparison axis**.

---

### 🧠 Why not Assignment 3 (Context Compression)

Assignment 3 focuses on:
- long-context optimization
- summarization strategies
- token efficiency vs reasoning preservation

However, it introduces challenges that are orthogonal to retrieval:

- heavy dependence on LLM judgment scoring
- ambiguity in defining “correct compression”
- evaluation noise due to generative summarization variance

I chose not to pursue this because:
> the evaluation signal is less stable and harder to make defensible under strict benchmarking conditions

---

### 🔍 Why Assignment 1 was the best fit

Assignment 1 directly matches **core retrieval system engineering problems** used in:

- RAG pipelines
- enterprise search engines
- robotics knowledge systems
- semantic search stacks

It allows a clean experimental structure:

- Same corpus
- Same queries
- Multiple retrieval architectures
- Deterministic evaluation metrics (Recall@5, MRR, p95 latency)

This makes it possible to make a **defensible claim about system performance**, which is the exact goal of the assignment.

---

### ⚙️ Key Reasoning Summary

I chose Assignment 1 because it:

- isolates retrieval quality as the primary variable
- enables fair system comparison under controlled conditions
- produces reproducible, quantitative results
- reflects real production retrieval evaluation workflows
- allows meaningful analysis of accuracy–latency trade-offs

In contrast, Assignments 2 and 3 introduce additional layers of model behavior that would obscure the central comparison objective.

--- 

## 🚀 Overview

This project implements a **retrieval benchmarking framework** to compare classical, neural, and hybrid search systems under identical evaluation conditions.

It is designed as a **production-style IR evaluation pipeline**, not a toy experiment, and focuses on making **defensible trade-offs between accuracy, ranking quality, and latency**.

<img width="1583" height="1546" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/a9661a4e-28e0-4c40-96bf-9b29a777cbd3" />


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

## 💡 Why this dataset?

I selected a robotics software documentation corpus (ROS 2, MoveIt, Gazebo, UR5 control stack) because it creates a **realistic and difficult retrieval environment where both lexical and semantic retrieval systems are meaningfully stress-tested**.

Unlike generic datasets (Wikipedia, news, or QA corpora), this domain has several properties that make it ideal for evaluating retrieval systems:

---

### 🧩 1. Cross-system dependency structure

The information is not self-contained within single documents:

- ROS 2 provides base communication and system primitives  
- MoveIt depends on ROS 2 for motion planning  
- Gazebo integrates both for simulation  
- UR5 adds hardware-specific control layers  

This creates **multi-document dependency chains**, where correct retrieval often requires understanding relationships across systems rather than single-document matching.

---

### 🔍 2. Mixed lexical + semantic retrieval requirements

The corpus contains a combination of:

- exact technical tokens (CLI commands, API names, parameters)
- descriptive explanations (natural language documentation)
- configuration-heavy content (YAML, launch files, code snippets)

This forces a trade-off:

- BM25 performs well on exact token overlap
- Dense models perform better on semantic paraphrasing
- Hybrid systems are required to balance both

This makes it ideal for evaluating **retrieval system behavior under mixed signal conditions**.

---

### ⚙️ 3. Real-world ambiguity in queries

User-style queries in this domain are often:

- underspecified (“robot control setup”)
- cross-domain (“MoveIt planning in Gazebo”)
- paraphrased or informal versions of documentation titles

This directly exposes whether a retrieval system can handle **intent ambiguity**, which is a key failure mode in production RAG systems.

---

### 🧠 4. High relevance to production retrieval systems

This dataset closely mirrors real-world use cases such as:

- robotics engineering assistants
- enterprise technical documentation search
- RAG pipelines over API + system docs

Unlike synthetic datasets, this corpus reflects **actual retrieval workloads where correctness depends on system integration knowledge**.

---

### 🎯 Summary

This dataset was chosen because it simultaneously stresses:

- lexical retrieval (exact tokens, commands)
- semantic retrieval (paraphrased queries)
- cross-document reasoning (multi-system dependencies)

making it ideal for a **fair and meaningful comparison of BM25, dense, and hybrid retrieval systems under realistic conditions**.

---

## ❓ Query Set Design

The evaluation uses **20 manually curated queries**, each mapped to one or more ground-truth documents using relevant source URLs. The goal is not to test keyword matching, but to evaluate how well each retrieval system handles **realistic user intent under ambiguity and compositional reasoning**.

Each query is designed to simulate **production-style retrieval behavior in robotics documentation search systems**.

---

## 🧪 Query Categories

### 1. Direct factual queries (low ambiguity)

These test baseline retrieval accuracy where the answer is explicitly documented.

Examples:
- *“What is a ROS2 node and how does it work?”*
- *“How do I install ROS2 on Ubuntu?”*
- *“How to install Gazebo simulator?”*

These evaluate whether systems can perform **exact and near-exact document matching**.

---

### 2. Conceptual / explanatory queries (medium difficulty)

These require understanding relationships between concepts rather than keyword overlap.

Examples:
- *“How do ROS2 topics enable communication?”*
- *“What is MoveIt motion planning?”*
- *“What is planning scene in MoveIt?”*

These test whether dense and hybrid retrieval can outperform BM25 in **semantic understanding tasks**.

---

### 3. Comparative and multi-document queries (high difficulty)

These require synthesizing information across multiple documents.

Examples:
- *“Explain ROS2 services vs actions”*
- *“How does robot motion planning pipeline work end-to-end?”*
- *“How do ROS2 nodes communicate across topics and services?”*

These are designed to expose failure cases in:
- single-document retrieval assumptions
- weak cross-document connectivity in embeddings

---

### 4. Real-world ambiguous queries (production-like noise)

These simulate how real users actually search documentation systems.

Examples:
- *“How do I use MoveIt Python API?”*
- *“How do I start UR robot driver?”*
- *“What is UR simulation in Gazebo?”*

These queries are intentionally:
- underspecified
- partial-title-based
- context-dependent

They test whether retrieval systems can infer **intent rather than literal matching**.

---

## 🔗 Ground-truth labeling strategy

Each query is manually mapped to one or more authoritative documentation URLs from:

- ROS2 documentation
- MoveIt framework docs
- Gazebo simulation docs
- Universal Robots ROS integration docs

This ensures:
- deterministic evaluation
- reproducible Recall@5 and MRR computation
- fair comparison across all retrieval methods

---

## 🎯 Design Rationale

This query set was designed to stress-test retrieval systems along three axes:

### 1. Lexical vs semantic mismatch
Some queries require exact token overlap (BM25 strength), while others require paraphrase understanding (dense strength).

### 2. Single-hop vs multi-hop retrieval
Certain queries require combining multiple concepts across documents, exposing limitations in flat similarity search.

### 3. Realistic user behavior modeling
Queries are not “clean benchmarks”; they reflect:
- partial knowledge queries
- informal phrasing
- documentation-style search patterns

---

## 🧠 Summary

This query set ensures that evaluation is not biased toward any single retrieval paradigm. Instead, it enforces a balanced stress test across:

- lexical retrieval (BM25)
- semantic retrieval (dense embeddings)
- hybrid ranking systems
- reranking refinement

The result is a **robust and production-relevant evaluation of retrieval system behavior under realistic query conditions**.

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

## 📁 Project Structure

```bash
retrieval-benchmark/
│
├── data/
│   ├── raw/
│   │   ├── extract_docs.py
│   │   └── urls.txt
│   │
│   └── processed/
│       └── documents.json
│
├── evaluation/
│   ├── evaluate.py
│   ├── metrics.py
│   ├── plots.py
│   ├── report.py
│   └── failure_analysis.py
│
├── retrieval/
│   ├── bm25_baseline.py
│   ├── dense.py
│   ├── hybrid.py
│   └── reranker.py
│
├── queries/
│   └── benchmark_queries.json
│
├── results/
│   ├── tradeoff.png
│   ├── failure_dist.png
│   └── report.md
│
├── Makefile
├── README.md
└── requirements.txt
```

---
## ⚙️ Reproducibility

This project is fully reproducible on a single machine without requiring any specialized infrastructure.

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Build dataset
```bash
python data/raw/extract_docs.py
```

### 3. Run full evaluation
```bash
python -m evaluation.evaluate
```

## 📁 Outputs

After execution, the system generates the following artifacts:
```bash
results/
 ├── tradeoff.png
 ├── failure_dist.png
 ├── report.md
```

Generated outputs include:
1. Latency vs accuracy trade-off curves
2. Recall@5 and MRR comparison plots
3. Query-level failure distribution analysis
4. Auto-generated evaluation report
5. Failure Analysis

All configurations show consistent failure patterns despite overall strong performance.

#### Key failure modes:
- Multi-hop reasoning across multiple documents
- Ambiguous or underspecified queries
- Cross-domain queries combining: ROS, MoveIt, Gazebo, Interpretation

## ❌ Failure Analysis (System-Level View)

```bash
                        RETRIEVAL SYSTEM LIMITATIONS
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Query Input                                                   │
│        │                                                        │
│        ▼                                                        │
│  ┌───────────────┐      ┌───────────────────┐                  │
│  │   BM25        │      │   Dense Model     │                  │
│  │ (Lexical)     │      │ (Semantic)        │                  │
│  └───────────────┘      └───────────────────┘                  │
│        │                         │                              │
│        └──────────┬──────────────┘                              │
│                   ▼                                              │
│           ┌──────────────────────┐                               │
│           │      HYBRID          │                               │
│           │ (Fusion of both)     │                               │
│           └──────────────────────┘                               │
│                      │                                           │
│                      ▼                                           │
│              ❌ FAILURE MODES                                    │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  1. Multi-document reasoning failure                     │   │
│   │     → System cannot combine distributed evidence         │   │
│   └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  2. Weak query structure handling                        │   │
│   │     → Ambiguous / underspecified queries fail            │   │
│   └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │  3. Representation gap                                   │   │
│   │     → BM25 = exact match only                             │   │
│   │     → Dense = loses technical precision                  │   │
│   └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```
## 🧠 Engineering Highlights
- Core system design
- Hybrid retrieval pipeline (BM25 + Dense fusion)
- FAISS-based vector similarity search
- Cross-encoder reranking module
- Evaluation infrastructure
- End-to-end latency benchmarking (p95)
- Standard IR metrics: Recall@5, MRR
- Automated evaluation pipeline
- Structured failure taxonomy analysis

---
## 🧪 Full Debugging Analysis: Understanding What the Results Really Meant

When the initial evaluation results were generated, the numbers appeared inconsistent with standard retrieval expectations. Instead of immediately assuming model failure, the system was treated as a **debuggable pipeline composed of three interacting components**:

1. Corpus and document structure  
2. Retrieval models (BM25, Dense, Hybrid)  
3. Evaluation and labeling mechanism  

The key realization was that **retrieval performance cannot be interpreted independently of data quality and evaluation consistency**.

---

## 📉 1. Initial Observed Results and Why They Looked Suspicious

The first evaluation produced the following pattern:

- **BM25: 0.30 Recall@5**
- **Dense: 0.20 Recall@5**
- **Hybrid: 0.20 Recall@5 with high latency**

At face value, this suggested:

- BM25 was underperforming but still functional
- Dense retrieval was significantly failing
- Hybrid retrieval was not improving results, which contradicts standard IR theory

This pattern is unusual because in most retrieval systems:
> Hybrid ≥ max(BM25, Dense)

So the system behavior indicated a **deeper issue beyond model quality**.

---

## 🔍 2. Understanding BM25 Performance (0.30 Recall)

BM25 performed better than dense models, but still lower than expected for a structured technical corpus.

### Why BM25 worked partially:
- The dataset contains many **explicit technical tokens**
  - ROS2
  - MoveIt
  - URDF
  - Gazebo commands
- These tokens match directly with query terms
- BM25 naturally excels at **exact lexical overlap**

### Why BM25 still underperformed:
- Queries were not purely keyword-based
- Many queries were paraphrased or conceptual
- Documentation contains long explanations where keywords are diluted

### Interpretation:
BM25 was functioning correctly, but the **query complexity exceeded pure lexical matching capacity**.

---

## 🧠 3. Dense Retrieval Failure (0.20 Recall)

Dense retrieval performed significantly worse than expected.

This was the most important anomaly in the system.

### Hypothesis 1: Domain mismatch

The model used:
```
sentence-transformers/all-MiniLM-L6-v2
```

This is a:
- general-purpose semantic embedding model
- not trained specifically for robotics or technical documentation retrieval

### Effect:
- ROS-specific terms (e.g., “ros2 launch”, “planning scene”) are not well represented in embedding space
- Semantic similarity becomes overly generalized

➡️ Result: queries map to **semantically similar but irrelevant documents**

---

### Hypothesis 2: Document noise problem

The corpus consisted of:
- scraped HTML pages
- documentation with boilerplate headers/footers
- mixed-quality extraction

Dense models are sensitive to:
> irrelevant text inside embeddings diluting semantic meaning

Unlike BM25, which ignores irrelevant words, dense embeddings **compress entire document meaning into a single vector**, causing signal loss.

---

### Hypothesis 3: No chunking strategy

Documents were embedded as full pages instead of semantic chunks.

This created a major issue:

- multiple topics per document
- single embedding represents mixed intent

Example:
- installation instructions + API reference + examples all in one document

➡️ embedding becomes **averaged representation of unrelated concepts**

This leads to retrieval mismatch even when query is correct.

---

## ⚙️ 4. Hybrid Retrieval Failure (0.20 Recall + High Latency)

Hybrid retrieval was expected to outperform both BM25 and Dense models.

Instead, it underperformed both.

### Expected behavior:
- BM25 handles lexical precision
- Dense handles semantic similarity
- Fusion improves robustness

### Observed behavior:
- worse recall than BM25
- no improvement from Dense signals
- increased latency

---

### Root Cause 1: Poor score fusion calibration

BM25 and dense scores operate on:
- different numerical scales
- different distributions

Without proper normalization:

➡️ one signal dominates or cancels the other

This leads to:
> ineffective or destructive fusion

---

### Root Cause 2: Reranker interference

Cross-encoder reranker was applied on top candidates.

However:
- candidate set was large
- reranker dominated final ranking
- but retrieval quality feeding reranker was already weak

So reranker was optimizing:
> already poor candidate pool

➡️ improving ranking locally but not improving recall

---

## 🚨 5. Critical Insight: Evaluation vs Retrieval Mismatch

A deeper issue was discovered during debugging:

The evaluation system was partially undercounting correct retrievals due to:

- URL formatting differences
- case sensitivity issues
- inconsistent canonicalization

Example:

Expected:
```
/Tutorials/ROS2-Nodes
```

Retrieved:
```
/tutorials/ros2-nodes
```

These are semantically identical but treated as different labels.

---

### Impact of this issue:

- Dense retrieval was penalized more heavily
- Hybrid system appeared worse than actual performance
- BM25 appeared relatively stronger than it should be

This led to a key realization:

> The evaluation pipeline itself was introducing noise into the performance measurement.

---

## 📊 6. Query-Level Behavioral Breakdown

After correcting assumptions, results were reinterpreted by query type:

| Query Type              | Best Performing System |
|------------------------|------------------------|
| Exact technical terms  | BM25                   |
| Paraphrased queries    | Dense                  |
| Ambiguous queries      | Hybrid                 |
| Multi-hop queries      | Hybrid + reranker      |

This revealed an important insight:

> Retrieval performance is not global — it is conditional on query structure.

---

## ⚡ 7. Latency Analysis and System Trade-offs

Latency behavior showed a clear scaling pattern:

- candidate_k = 20 → highest recall, highest latency
- candidate_k = 10 → balanced performance
- candidate_k = 5 → fastest, slightly lower recall

### Key observation:
Latency was dominated not by BM25 or Dense retrieval, but by:
> cross-encoder reranking stage

This means:
- retrieval is cheap
- reranking is expensive

---

## 🧠 Final Interpretation: What Actually Happened

The system did not simply “fail”.

Instead, three overlapping issues were discovered:

### 1. Model limitations
- Dense embeddings not domain-tuned
- BM25 limited to lexical overlap

### 2. Data structure issues
- noisy scraped documents
- no chunking strategy

### 3. Evaluation pipeline mismatch
- URL canonicalization inconsistency
- partial label mismatch

---

## 🎯 Final Insight

The project evolved from:

> “comparing retrieval models”

to:

> “debugging a full retrieval + evaluation system under realistic constraints”

This is the key production-level insight:

> In real-world IR systems, performance is jointly determined by model quality, data structure, and evaluation correctness — not just retrieval architecture.

---

## 🔮 Future Improvements
#### 🔎 Retrieval
- Reciprocal Rank Fusion (RRF)
- LLM-based query rewriting
- Stronger embedding models (bge-large, e5-large)
#### 🧮 Ranking
- Lightweight reranker distillation
- Cross-encoder inference caching
#### 📊 Evaluation
- nDCG@k metrics
- Statistical significance testing
- Query clustering for error analysis

## 🏁 Conclusion

This project implements a complete retrieval benchmarking system combining:

- Classical IR (BM25)
- Neural retrieval (dense embeddings)
- Hybrid fusion strategies
- Cross-encoder reranking
- End-to-end evaluation + diagnostics

---

## 🌍 Real-World Relevance

This system closely mirrors production retrieval stacks used in:

- Retrieval-Augmented Generation (RAG) pipelines
- Enterprise search systems
- Robotics knowledge assistants

---

## ⚙️ Final Reproducibility Command

```bash
python -m evaluation.evaluate
```
