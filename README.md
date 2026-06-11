# Memory System Implementation for LLM Chatbots

This project implements and evaluates memory architectures for LLM-powered chatbots and agents.

The first implemented system is inspired by **A-MEM: Agentic Memory for LLM Agents**. It stores interactions as structured memory notes, generates memory metadata, links related memories, evolves older memories conservatively, and retrieves memories using intent-aware reranking.

## Documentation

- [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md): explains the repository layout and purpose of each major file.
- [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md): records experiments, benchmark results, interpretations, and limitations.

## Current Systems

### 1. Raw Vector Memory Baseline
A simple baseline that:
- stores raw memory text
- embeds raw content
- retrieves memories using cosine similarity

It does not use metadata, links, memory evolution, or reranking.

### 2. Agentic Memory System
An A-MEM-inspired system that:
- converts raw interactions into structured notes
- generates keywords, tags, and contextual descriptions
- creates links between related memories
- applies conservative memory evolution
- retrieves memories using vector search, keyword overlap, and intent-aware reranking

## Current Evaluation Metrics

- Keyword Hit Rate
- Keyword Hit Rate @ 1
- Mean Reciprocal Rank

## First Benchmark Result

| System | Keyword Hit Rate | Keyword Hit Rate @ 1 | MRR |
|---|---:|---:|---:|
| raw_vector | 1.000 | 0.667 | 0.792 |
| agentic_memory | 1.000 | 1.000 | 1.000 |

## Key Finding

The raw vector baseline achieved perfect broad recall but weaker exact-memory ranking.  
The agentic memory system achieved perfect recall and perfect exact-memory ranking on the expanded benchmark, including a preference-change case where the user later qualified an earlier VS Code vs Colab preference.


## Local Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Install Ollama

Install Ollama from:

```text
https://ollama.com/download
```

Then pull the local model used by this project:

```powershell
ollama pull qwen2.5:3b
```

### 4. Create local environment file

Copy `.env.example` to `.env`.

```powershell
copy .env.example .env
```

Current local model setting:

```text
OLLAMA_MODEL=qwen2.5:3b
```

### 5. Run from project root

Most commands should be run from the project root. If imports fail on Windows PowerShell, run:

```powershell
$env:PYTHONPATH="."
```

## Run Evaluation

```powershell
python evals/run_eval.py
```

## Compare Systems

```powershell
python evals/compare_systems.py
```

## Current Status

Completed:
- Raw vector memory baseline
- A-MEM-inspired agentic memory system
- Local Ollama-backed LLM client
- Structured note construction
- Link generation
- Conservative memory evolution
- Intent-aware reranking
- Synthetic evaluation benchmark
- CSV result logging
- Experiment log and project structure documentation

Current headline result:

| System | Keyword Hit Rate | Keyword Hit Rate @ 1 | MRR |
|---|---:|---:|---:|
| raw_vector | 1.000 | 0.643 | 0.702 |
| agentic_memory | 1.000 | 1.000 | 1.000 |

Next:
- Add contradiction and preference-change tests
- Add stale-memory handling
- Add additional paper-inspired memory approaches
- Build a Streamlit demo
- Expand beyond synthetic benchmark cases