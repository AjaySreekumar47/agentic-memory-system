import numpy as np
from typing import List, Tuple

from memory_system.schemas import MemoryNote


class SimpleVectorStore:
    @staticmethod
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        va = np.array(a)
        vb = np.array(b)

        denom = np.linalg.norm(va) * np.linalg.norm(vb)
        if denom == 0:
            return 0.0

        return float(np.dot(va, vb) / denom)

    def search(
        self,
        query_embedding: list[float],
        notes: List[MemoryNote],
        top_k: int = 5,
    ) -> List[Tuple[MemoryNote, float]]:
        scored = []

        for note in notes:
            if note.embedding is None:
                continue

            score = self.cosine_similarity(query_embedding, note.embedding)
            scored.append((note, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]