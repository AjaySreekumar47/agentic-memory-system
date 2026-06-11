from memory_system.config import TOP_K_CANDIDATES, TOP_K_RETRIEVAL
from memory_system.embedding_client import EmbeddingClient
from memory_system.evolver import Evolver
from memory_system.linker import Linker
from memory_system.llm_client import LLMClient
from memory_system.memory_store import MemoryStore
from memory_system.note_builder import NoteBuilder
from memory_system.retriever import Retriever
from memory_system.schemas import MemoryNote, RetrievedMemory
from memory_system.vector_store import SimpleVectorStore


class AgenticMemorySystem:
    def __init__(self):
        self.llm_client = LLMClient()
        self.embedding_client = EmbeddingClient()
        self.memory_store = MemoryStore()
        self.vector_store = SimpleVectorStore()

        self.note_builder = NoteBuilder(self.llm_client, self.embedding_client)
        self.linker = Linker(self.llm_client)
        self.evolver = Evolver(self.llm_client)
        self.retriever = Retriever(
            self.memory_store,
            self.embedding_client,
            self.vector_store,
        )

    def add_memory(self, content: str) -> MemoryNote:
        # 1. Build enriched memory note
        new_note = self.note_builder.build(content)

        # 2. Retrieve similar existing memories
        existing_notes = self.memory_store.all()

        if existing_notes:
            candidate_results = self.vector_store.search(
                query_embedding=new_note.embedding,
                notes=existing_notes,
                top_k=TOP_K_CANDIDATES,
            )
            candidates = [note for note, _ in candidate_results]
        else:
            candidates = []

        # 3. Generate links
        linked_ids = self.linker.generate_links(new_note, candidates)
        new_note.links = linked_ids

        # 4. Add backlinks from old memories to new memory
        for linked_id in linked_ids:
            linked_note = self.memory_store.get(linked_id)

            if linked_note and new_note.id not in linked_note.links:
                linked_note.links.append(new_note.id)
                self.memory_store.update(linked_note)

        # 5. Evolve candidate memories
        for candidate in candidates:
            old_version = candidate.metadata_version

            evolved = self.evolver.evolve_memory(
                existing_note=candidate,
                new_note=new_note,
                nearby_notes=candidates,
            )

            if evolved.metadata_version != old_version:
                evolved.embedding = self.embedding_client.embed_text(
                    "\n".join(
                        [
                            f"Content: {evolved.content}",
                            f"Keywords: {', '.join(evolved.keywords)}",
                            f"Tags: {', '.join(evolved.tags)}",
                            f"Context: {evolved.context}",
                        ]
                    )
                )
                self.memory_store.update(evolved)

        # 6. Store new note
        self.memory_store.add(new_note)

        return new_note

    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> list[RetrievedMemory]:
        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
            expand_links=True,
        )

    def retrieve_context(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> str:
        memories = self.retrieve(query=query, top_k=top_k)
        return self.retriever.format_for_prompt(memories)

    def clear(self) -> None:
        self.memory_store.clear()