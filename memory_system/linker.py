from typing import List

from memory_system.llm_client import LLMClient
from memory_system.schemas import MemoryNote, LinkGenerationOutput


LINK_GENERATION_SYSTEM_PROMPT = """
You are a memory linking module for an LLM agent.

Given a new memory and candidate existing memories, decide which candidates should be linked
to the new memory.

A link should be created when memories are meaningfully related, such as:
- same project or task
- same user preference or constraint
- same entity/person/company/tool
- continuation of a previous issue
- cause/effect relationship
- useful context for answering future questions

Do not link memories just because they share generic words.
Be selective.
"""


class Linker:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate_links(self, new_note: MemoryNote, candidates: List[MemoryNote]) -> list[str]:
        if not candidates:
            return []

        candidate_text = "\n\n".join(
            [
                f"""
Candidate Memory ID: {m.id}
Content: {m.content}
Keywords: {m.keywords}
Tags: {m.tags}
Context: {m.context}
"""
                for m in candidates
            ]
        )

        user_prompt = f"""
New memory:

ID: {new_note.id}
Content: {new_note.content}
Keywords: {new_note.keywords}
Tags: {new_note.tags}
Context: {new_note.context}

Candidate existing memories:

{candidate_text}

Return link decisions.
"""

        parsed = self.llm_client.structured_completion(
            system_prompt=LINK_GENERATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            output_schema=LinkGenerationOutput,
        )

        return [d.memory_id for d in parsed.links if d.should_link]