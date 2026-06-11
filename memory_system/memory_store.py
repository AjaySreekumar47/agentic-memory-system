import json
from pathlib import Path
from typing import List, Optional

from memory_system.config import MEMORY_DB_DIR
from memory_system.schemas import MemoryNote


class MemoryStore:
    def __init__(self, path: Path = MEMORY_DB_DIR / "memories.json"):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self._save_raw({})

    def _load_raw(self) -> dict:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_raw(self, data: dict) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, note: MemoryNote) -> None:
        data = self._load_raw()
        data[note.id] = note.model_dump()
        self._save_raw(data)

    def update(self, note: MemoryNote) -> None:
        data = self._load_raw()

        if note.id not in data:
            raise KeyError(f"Memory note not found: {note.id}")

        data[note.id] = note.model_dump()
        self._save_raw(data)

    def get(self, note_id: str) -> Optional[MemoryNote]:
        data = self._load_raw()
        raw = data.get(note_id)
        return MemoryNote(**raw) if raw else None

    def all(self) -> List[MemoryNote]:
        data = self._load_raw()
        return [MemoryNote(**item) for item in data.values()]

    def clear(self) -> None:
        self._save_raw({})