from memory_system.schemas import RetrievedMemory


def keyword_hit_rate(
    results: list[RetrievedMemory],
    expected_keywords: list[str],
) -> float:
    """
    Measures how many expected keywords appear somewhere in the retrieved memories.

    This is a simple first-pass retrieval metric.
    """

    retrieved_text = "\n".join(
        [
            f"{item.note.content} {item.note.context} {' '.join(item.note.keywords)} {' '.join(item.note.tags)}"
            for item in results
        ]
    ).lower()

    hits = 0

    for keyword in expected_keywords:
        if keyword.lower() in retrieved_text:
            hits += 1

    if not expected_keywords:
        return 0.0

    return hits / len(expected_keywords)

def keyword_hit_rate_at_1(
    results: list[RetrievedMemory],
    expected_keywords: list[str],
) -> float:
    """
    Measures whether expected keywords appear in only the top retrieved memory.

    This is stricter than keyword_hit_rate because it evaluates ranking quality.
    """

    if not results or not expected_keywords:
        return 0.0

    top_note = results[0].note

    top_text = (
        f"{top_note.content} "
        f"{top_note.context} "
        f"{' '.join(top_note.keywords)} "
        f"{' '.join(top_note.tags)}"
    ).lower()

    hits = 0

    for keyword in expected_keywords:
        if keyword.lower() in top_text:
            hits += 1

    return hits / len(expected_keywords)

def reciprocal_rank_by_content(
    results: list[RetrievedMemory],
    expected_memory_content: str,
) -> float:
    """
    Computes reciprocal rank of the expected memory.

    If the expected memory is ranked first, score = 1.0.
    If ranked second, score = 0.5.
    If ranked third, score = 0.333.
    If not found, score = 0.0.
    """

    if not results or not expected_memory_content:
        return 0.0

    expected = expected_memory_content.strip().lower()

    for rank, item in enumerate(results, start=1):
        actual = item.note.content.strip().lower()

        if actual == expected:
            return 1.0 / rank

    return 0.0