# Experiment Log

## Experiment 1: Raw Vector Memory vs Agentic Memory

### Goal
Compare a pure raw-vector memory baseline against an A-MEM-inspired agentic memory system.

### Systems Compared

#### Raw Vector Memory
- Stores raw memory text
- Embeds raw content
- Retrieves using cosine similarity
- No LLM-generated metadata
- No link generation
- No memory evolution
- No reranking

#### Agentic Memory
- Converts raw interactions into structured memory notes
- Generates keywords, tags, and contextual descriptions
- Uses embeddings for candidate retrieval
- Generates links between related memories
- Applies conservative memory evolution
- Uses intent-aware reranking

### Metrics
- Keyword Hit Rate
- Keyword Hit Rate @ 1
- Mean Reciprocal Rank

### Results

| System | Keyword Hit Rate | Keyword Hit Rate @ 1 | MRR |
|---|---:|---:|---:|
| raw_vector | 1.000 | 0.500 | 0.708 |
| agentic_memory | 1.000 | 1.000 | 1.000 |

> Note: This was the initial smaller benchmark. The expanded benchmark below is the current headline result.

### Interpretation
Both systems retrieved relevant information somewhere in the top-k results, but the raw vector baseline struggled with ranking precision.

The agentic memory system ranked the exact expected memory first for every query in the first synthetic benchmark.

### Key Finding
Raw vector memory provides strong recall, but agentic memory improves exact-memory ranking through structured notes, conservative evolution, and intent-aware reranking.

### Limitation
This is a small synthetic benchmark. Future experiments should add more queries, contradiction cases, stale memories, and multi-session conversations.

## Experiment 2: Expanded Benchmark with Failure-Mode Queries

### Goal
Test whether the memory systems can retrieve not only basic project facts, but also critique-oriented and future-design memories.

### Added Cases
The benchmark was expanded with memories about:
- stale memories
- changing user preferences
- A-MEM metadata drift
- memory boundary blur

### Results

| System | Keyword Hit Rate | Keyword Hit Rate @ 1 | MRR |
|---|---:|---:|---:|
| raw_vector | 1.000 | 0.667 | 0.792 |
| agentic_memory | 1.000 | 1.000 | 1.000 |

### Interpretation
Both systems maintained perfect broad recall, but the raw vector baseline still made ranking mistakes.

The agentic memory system retrieved the exact expected memory at rank 1 across all expanded benchmark queries.

### Key Finding
Intent-aware reranking helped distinguish between project-goal, technical-detail, environment, paper-choice, and failure-mode queries.

### Limitation
The benchmark is still synthetic and small. Future work should add multi-turn conversation traces, contradictory memories, stale preferences, and larger memory collections.