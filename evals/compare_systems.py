import pandas as pd
from rich import print

from evals.synthetic_cases import SYNTHETIC_MEMORY_EVENTS, SYNTHETIC_QUERIES
from evals.metrics import (
    keyword_hit_rate,
    keyword_hit_rate_at_1,
    reciprocal_rank_by_content,
)
from memory_system.agentic_memory import AgenticMemorySystem
from memory_system.raw_vector_memory import RawVectorMemorySystem


def evaluate_system(system_name: str, memory_system):
    memory_system.clear()

    print(f"\n[bold cyan]Evaluating system:[/bold cyan] {system_name}")

    for event in SYNTHETIC_MEMORY_EVENTS:
        memory_system.add_memory(event["content"])

    rows = []

    for case in SYNTHETIC_QUERIES:
        results = memory_system.retrieve(case["query"], top_k=5)

        score = keyword_hit_rate(results, case["expected_keywords"])
        score_at_1 = keyword_hit_rate_at_1(results, case["expected_keywords"])
        rr = reciprocal_rank_by_content(results, case["expected_memory_content"])

        rows.append(
            {
                "system": system_name,
                "query": case["query"],
                "expected_memory_content": case["expected_memory_content"],
                "keyword_hit_rate": score,
                "keyword_hit_rate_at_1": score_at_1,
                "reciprocal_rank": rr,
                "top_retrieved_content": results[0].note.content if results else "",
                "top_retrieved_score": results[0].score if results else 0.0,
            }
        )

        print(f"\n[bold yellow]Query:[/bold yellow] {case['query']}")
        print(f"Keyword Hit Rate: {score}")
        print(f"Keyword Hit Rate @ 1: {score_at_1}")
        print(f"Reciprocal Rank: {rr}")
        print(f"Top Retrieved: {results[0].note.content if results else 'None'}")

    return rows


def main():
    all_rows = []

    systems = [
        ("raw_vector", RawVectorMemorySystem()),
        ("agentic_memory", AgenticMemorySystem()),
    ]

    for system_name, system in systems:
        all_rows.extend(evaluate_system(system_name, system))

    results_df = pd.DataFrame(all_rows)
    output_path = "data/results/system_comparison.csv"
    results_df.to_csv(output_path, index=False)

    summary_df = (
    results_df.groupby("system")[
        ["keyword_hit_rate", "keyword_hit_rate_at_1", "reciprocal_rank"]
    ]
    .mean()
    .reset_index()
)

    summary_output_path = "data/results/system_comparison_summary.csv"
    summary_df.to_csv(summary_output_path, index=False)

    print("\n[bold green]System Comparison Summary[/bold green]")
    print(summary_df)

    print("\n[bold green]Saved detailed comparison results to[/bold green]")
    print(output_path)

    print("[bold green]Saved summary comparison results to[/bold green]")
    print(summary_output_path)


if __name__ == "__main__":
    main()