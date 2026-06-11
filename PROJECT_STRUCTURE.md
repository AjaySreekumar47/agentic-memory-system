# Project Structure

This document explains the main folders and files in the repository.

## Top-Level Files

### `README.md`
Main project overview. Explains the motivation, implemented memory systems, current results, and how to run the project.

### `EXPERIMENT_LOG.md`
Tracks completed experiments, benchmark results, interpretations, and limitations.

### `requirements.txt`
Python dependencies required to run the project.

### `.env`
Local environment configuration. This file is not committed to GitHub.

### `run_demo.ps1`
Convenience script that resets memory, adds demo memories, and runs retrieval.

---

## `memory_system/`

Core implementation of the memory systems.

### `schemas.py`
Defines the main data structures used across the project, including `MemoryNote`, retrieval outputs, and structured LLM outputs.

### `config.py`
Loads environment variables and central settings such as model names, data paths, and retrieval parameters.

### `llm_client.py`
Local Ollama-backed LLM client. Used for structured note construction, link generation, and memory evolution.

### `embedding_client.py`
Loads the sentence-transformer embedding model and converts text into vector embeddings.

### `memory_store.py`
Simple JSON-based persistent memory storage.

### `vector_store.py`
Implements cosine similarity search over stored memory embeddings.

### `note_builder.py`
Converts raw interactions into structured memory notes with keywords, tags, context, and embeddings.

### `linker.py`
Generates links between related memory notes.

### `evolver.py`
Applies conservative memory evolution by appending clarifying metadata while preserving original memory content.

### `retriever.py`
Retrieves memories using vector search, keyword-overlap reranking, and intent-aware reranking.

### `agentic_memory.py`
Main orchestrator for the A-MEM-inspired memory system.

### `raw_vector_memory.py`
Pure baseline system that stores raw text and retrieves using embedding similarity only.

---

## `evals/`

Evaluation and comparison scripts.

### `synthetic_cases.py`
Small synthetic benchmark containing memory events, queries, expected keywords, and expected target memories.

### `metrics.py`
Retrieval metrics including keyword hit rate, keyword hit rate at rank 1, and reciprocal rank.

### `run_eval.py`
Runs evaluation for the agentic memory system.

### `compare_systems.py`
Compares raw vector memory against the agentic memory system and saves detailed and summary CSVs.

---

## `scripts/`

Small scripts for manual testing.

### `reset_memory.py`
Clears the local memory database.

### `demo_add_memory.py`
Adds example memories to the memory store.

### `demo_retrieve_memory.py`
Retrieves memories for a sample query and prints formatted context.

---

## `data/`

Generated local data.

### `data/memory_db/`
Stores local memory JSON files. Ignored by Git.

### `data/results/`
Stores evaluation CSV outputs. These may be kept if small and useful for documentation.

---

## `papers/`

Research papers used as references for implementation and future baselines.