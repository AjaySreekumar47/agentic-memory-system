SYNTHETIC_MEMORY_EVENTS = [
    {
        "id": "m1",
        "content": "The user is building an efficient memory system for an LLM chatbot.",
    },
    {
        "id": "m2",
        "content": "The user wants to compare four research papers on LLM memory systems.",
    },
    {
        "id": "m3",
        "content": "The user decided to start with the A-MEM paper.",
    },
    {
        "id": "m4",
        "content": "A-MEM uses note construction, link generation, memory evolution, and memory retrieval.",
    },
    {
        "id": "m5",
        "content": "The user prefers local VS Code development for this project rather than Colab.",
    },
        {
        "id": "m6",
        "content": "The user wants the final memory system to avoid stale memories and handle changing user preferences.",
    },
    {
        "id": "m7",
        "content": "The user wants to critique A-MEM because memory evolution can cause metadata drift or boundary blur.",
    },
    {
        "id": "m8",
        "content": "The user originally preferred local VS Code over Colab for this memory-system project because they wanted a lightweight local development workflow."
    },
    {
        "id": "m9",
        "content": "The user later decided that Colab is acceptable for GPU-heavy experiments, while still preferring VS Code for normal local development."
    },
]

SYNTHETIC_QUERIES = [
    {
        "query": "What project is the user building?",
        "expected_keywords": ["memory system", "LLM chatbot"],
        "expected_memory_content": "The user is building an efficient memory system for an LLM chatbot.",
    },
    {
        "query": "Which paper approach is the user implementing first?",
        "expected_keywords": ["A-MEM"],
        "expected_memory_content": "The user decided to start with the A-MEM paper.",
    },
    {
        "query": "Where does the user want to build the project?",
        "expected_keywords": ["VS Code", "local"],
        "expected_memory_content": "The user prefers local VS Code development for this project rather than Colab.",
    },
    {
        "query": "What are the main modules in the first memory system?",
        "expected_keywords": ["note construction", "link generation", "memory evolution", "retrieval"],
        "expected_memory_content": "A-MEM uses note construction, link generation, memory evolution, and memory retrieval.",
    },
        {
        "query": "What failure modes does the user want to watch for in A-MEM?",
        "expected_keywords": ["metadata drift", "boundary blur"],
        "expected_memory_content": "The user wants to critique A-MEM because memory evolution can cause metadata drift or boundary blur.",
    },
    {
        "query": "What should the final memory system avoid?",
        "expected_keywords": ["stale memories", "changing user preferences"],
        "expected_memory_content": "The user wants the final memory system to avoid stale memories and handle changing user preferences.",
    },
    {
        "query": "What development environment should the user use now?",
        "expected_keywords": ["Colab", "GPU-heavy", "VS Code", "normal local development"],
        "expected_memory_content": "The user later decided that Colab is acceptable for GPU-heavy experiments, while still preferring VS Code for normal local development.",
    },
]