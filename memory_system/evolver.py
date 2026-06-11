from typing import List

from memory_system.llm_client import LLMClient
from memory_system.schemas import MemoryNote, EvolvedMemoryOutput


MEMORY_EVOLUTION_SYSTEM_PROMPT = """
You are a memory evolution module for an LLM agent.

Your job is to decide whether an existing memory should have its metadata updated
based on a newly added related memory.

You may update:
- keywords
- tags
- context

Rules:
- Preserve the original content exactly.
- Do not overwrite historical facts.
- Do not invent new facts.
- If the new memory clarifies the old memory, update the context.
- If the new memory contradicts the old memory, preserve both facts in the context.
- If no update is needed, set should_update to false and keep fields unchanged.
"""


class Evolver:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def evolve_memory(
        self,
        existing_note: MemoryNote,
        new_note: MemoryNote,
        nearby_notes: List[MemoryNote],
    ) -> MemoryNote:
        nearby_text = "\n\n".join(
            [
                f"""
Nearby Memory ID: {m.id}
Content: {m.content}
Keywords: {m.keywords}
Tags: {m.tags}
Context: {m.context}
"""
                for m in nearby_notes
                if m.id != existing_note.id
            ]
        )

        user_prompt = f"""
Existing memory to potentially evolve:

ID: {existing_note.id}
Original Content: {existing_note.content}
Current Keywords: {existing_note.keywords}
Current Tags: {existing_note.tags}
Current Context: {existing_note.context}

New related memory:

ID: {new_note.id}
Content: {new_note.content}
Keywords: {new_note.keywords}
Tags: {new_note.tags}
Context: {new_note.context}

Other nearby memories:

{nearby_text}

Decide whether to update the existing memory metadata.
"""

        parsed = self.llm_client.structured_completion(
            system_prompt=MEMORY_EVOLUTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            output_schema=EvolvedMemoryOutput,
        )

        if not parsed.should_update:
            return existing_note

        # Conservative evolution:
        # preserve old keywords/tags and only add new ones
        existing_note.keywords = list(
            dict.fromkeys(existing_note.keywords + parsed.updated_keywords)
        )

        existing_note.tags = list(
            dict.fromkeys(existing_note.tags + parsed.updated_tags)
        )

        # Preserve original context and append clarification instead of replacing it
        if parsed.updated_context and parsed.updated_context.strip() != existing_note.context.strip():
            existing_note.context = (
                existing_note.context.strip()
                + "\n\nEvolution note: "
                + parsed.updated_context.strip()
            )

        existing_note.metadata_version += 1

        return existing_note