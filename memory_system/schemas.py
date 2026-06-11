from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from pydantic import field_validator
from pydantic import BaseModel, Field, field_validator


class MemoryNote(BaseModel):
    """
    A structured A-MEM-style memory note.
    """

    id: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    keywords: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    context: str = ""

    embedding: Optional[List[float]] = None
    links: List[str] = Field(default_factory=list)

    metadata_version: int = 1


class NoteConstructionOutput(BaseModel):
    keywords: List[str]
    tags: List[str]
    context: str


class LinkDecision(BaseModel):
    memory_id: str
    should_link: bool
    reason: str


class LinkGenerationOutput(BaseModel):
    links: List[LinkDecision]


class EvolvedMemoryOutput(BaseModel):
    should_update: bool
    updated_keywords: List[str] = Field(default_factory=list)
    updated_tags: List[str] = Field(default_factory=list)
    updated_context: Optional[str] = ""
    reason: str = ""

    @field_validator("updated_context", mode="before")
    @classmethod
    def none_context_to_empty_string(cls, value):
        if value is None:
            return ""
        return value


class RetrievedMemory(BaseModel):
    note: MemoryNote
    score: float
    source: str = "vector"