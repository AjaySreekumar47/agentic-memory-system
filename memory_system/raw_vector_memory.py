from uuid import uuid4

from memory_system.config import TOP_K_RETRIEVAL
from memory_system.embedding_client import EmbeddingClient
from memory_system.memory_store import MemoryStore
from memory_system.schemas import MemoryNote, RetrievedMemory
from memory_system.vector_store import SimpleVectorStore


class RawVectorMemorySystem:
    """
    Pure baseline memory system.

    Stores raw memory content with embeddings only.
    Retrieves only by cosine similarity.
    No LLM-generated metadata, no links, no evolution, no reranking.
    """

    def __init__(self):
        self.embedding_client = EmbeddingClient()
        self.memory_store = MemoryStore()
        self.vector_store = SimpleVectorStore()

    def add_memory(self, content: str) -> MemoryNote:
        note = MemoryNote(
            id=str(uuid4()),
            content=content,
            keywords=[],
            tags=[],
            context="",
            links=[],
        )

        note.embedding = self.embedding_client.embed_text(content)
        self.memory_store.add(note)

        return note

    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> list[RetrievedMemory]:
        query_embedding = self.embedding_client.embed_text(query)
        notes = self.memory_store.all()

        vector_results = self.vector_store.search(
            query_embedding=query_embedding,
            notes=notes,
            top_k=top_k,
        )

        return [
            RetrievedMemory(
                note=note,
                score=score,
                source="raw_vector",
            )
            for note, score in vector_results
        ]

    def retrieve_context(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> str:
        memories = self.retrieve(query=query, top_k=top_k)

        if not memories:
            return "No relevant memories found."

        blocks = []

        for item in memories:
            note = item.note
            blocks.append(
                f"""
Memory ID: {note.id}
Source: {item.source}
Score: {item.score:.4f}
Content: {note.content}
"""
            )

        return "\n---\n".join(blocks)

    def clear(self) -> None:
        self.memory_store.clear()