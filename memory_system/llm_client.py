import json
from typing import Type, TypeVar

import ollama
from pydantic import BaseModel

from memory_system.config import OLLAMA_MODEL

from memory_system.schemas import (
    NoteConstructionOutput,
    LinkGenerationOutput,
    LinkDecision,
    EvolvedMemoryOutput,
)

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """
    Ollama-backed local LLM client.

    This client asks the local Ollama model to return JSON, then validates
    the result using our Pydantic schemas.
    """

    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = model

    def structured_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[T],
    ) -> T:
        schema_hint = self._schema_hint(output_schema)

        full_prompt = f"""
{system_prompt}

You must return ONLY valid JSON.
Do not include markdown.
Do not include explanations.
Do not wrap the JSON in code fences.

Expected JSON format:
{schema_hint}

User request:
{user_prompt}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],
        )

        raw_text = response["message"]["content"].strip()
        parsed_json = self._safe_json_loads(raw_text)

        return output_schema(**parsed_json)

    def _safe_json_loads(self, text: str) -> dict:
        """
        Attempts to parse model output as JSON.
        Handles cases where the model accidentally includes surrounding text.
        """

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")

            if start == -1 or end == -1 or end <= start:
                raise ValueError(f"Model did not return valid JSON:\n{text}")

            cleaned = text[start : end + 1]
            return json.loads(cleaned)

    def _schema_hint(self, output_schema: Type[T]) -> str:
        if output_schema == NoteConstructionOutput:
            return json.dumps(
                {
                    "keywords": ["keyword 1", "keyword 2"],
                    "tags": ["tag 1", "tag 2"],
                    "context": "A concise contextual description of the memory."
                },
                indent=2,
            )

        if output_schema == LinkGenerationOutput:
            return json.dumps(
                {
                    "links": [
                        {
                            "memory_id": "candidate-memory-id",
                            "should_link": True,
                            "reason": "Why this memory should or should not be linked."
                        }
                    ]
                },
                indent=2,
            )

        if output_schema == EvolvedMemoryOutput:
            return json.dumps(
                {
                    "should_update": True,
                    "updated_keywords": ["keyword 1", "keyword 2"],
                    "updated_tags": ["tag 1", "tag 2"],
                    "updated_context": "Updated context if needed.",
                    "reason": "Why the memory should or should not be updated."
                },
                indent=2,
            )

        raise ValueError(f"Unsupported output schema: {output_schema}")