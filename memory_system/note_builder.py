from uuid import uuid4

from memory_system.embedding_client import EmbeddingClient
from memory_system.llm_client import LLMClient
from memory_system.schemas import MemoryNote, NoteConstructionOutput


NOTE_CONSTRUCTION_SYSTEM_PROMPT = """
You are a memory construction module for an LLM agent.

Your job is to convert a raw interaction into a compact structured memory note.

Extract:
1. keywords: concrete concepts, entities, technologies, people, projects, preferences
2. tags: broad categories useful for future retrieval
3. context: a concise but information-rich description explaining what this memory means

Rules:
- Do not invent facts not present in the interaction.
- Keep keywords short.
- Keep tags general.
- The context should preserve the user's intent and important details.
"""


class NoteBuilder:
    def __init__(self, llm_client: LLMClient, embedding_client: EmbeddingClient):
        self.llm_client = llm_client
        self.embedding_client = embedding_client

    def build(self, content: str) -> MemoryNote:
        user_prompt = f"""
Raw interaction:

{content}

Create a structured memory note.
"""

        parsed = self.llm_client.structured_completion(
            system_prompt=NOTE_CONSTRUCTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            output_schema=NoteConstructionOutput,
        )

        note = MemoryNote(
            id=str(uuid4()),
            content=content,
            keywords=parsed.keywords,
            tags=parsed.tags,
            context=parsed.context,
        )

        note.embedding = self.embedding_client.embed_text(self._embedding_text(note))
        return note

    @staticmethod
    def _embedding_text(note: MemoryNote) -> str:
        return "\n".join(
            [
                f"Content: {note.content}",
                f"Keywords: {', '.join(note.keywords)}",
                f"Tags: {', '.join(note.tags)}",
                f"Context: {note.context}",
            ]
        )