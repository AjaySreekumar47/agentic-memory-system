from rich import print
import pandas as pd
from evals.synthetic_cases import SYNTHETIC_MEMORY_EVENTS, SYNTHETIC_QUERIES
from evals.metrics import (
    keyword_hit_rate,
    keyword_hit_rate_at_1,
    reciprocal_rank_by_content,
)
from memory_system.agentic_memory import AgenticMemorySystem
from memory_system.raw_vector_memory import RawVectorMemorySystem

def main():
    memory = AgenticMemorySystem()
    memory.clear()

    print("[bold cyan]Adding synthetic memories...[/bold cyan]")

    for event in SYNTHETIC_MEMORY_EVENTS:
        memory.add_memory(event["content"])

    print("\n[bold cyan]Running retrieval evaluation...[/bold cyan]")

    scores = []
    scores_at_1 = []
    reciprocal_ranks = []
    rows = []

    for case in SYNTHETIC_QUERIES:
        results = memory.retrieve(case["query"], top_k=5)
        score = keyword_hit_rate(results, case["expected_keywords"])
        score_at_1 = keyword_hit_rate_at_1(results, case["expected_keywords"])
        rr = reciprocal_rank_by_content(results, case["expected_memory_content"])

        scores.append(score)
        scores_at_1.append(score_at_1)
        reciprocal_ranks.append(rr)

        print("\n[bold yellow]Query[/bold yellow]")
        print(case["query"])

        print("[bold yellow]Expected Keywords[/bold yellow]")
        print(case["expected_keywords"])

        print("[bold yellow]Keyword Hit Rate[/bold yellow]")
        print(score)

        print("[bold yellow]Keyword Hit Rate @ 1[/bold yellow]")
        print(score_at_1)

        print("[bold yellow]Reciprocal Rank[/bold yellow]")
        print(rr)

        print("[bold yellow]Top Retrieved Memories[/bold yellow]")
        for item in results[:3]:
            print(
                f"- score={item.score:.3f} | source={item.source} | content={item.note.content}"
            )
        
        rows.append(
            {
                "query": case["query"],
                "expected_memory_content": case["expected_memory_content"],
                "keyword_hit_rate": score,
                "keyword_hit_rate_at_1": score_at_1,
                "reciprocal_rank": rr,
                "top_retrieved_content": results[0].note.content if results else "",
                "top_retrieved_score": results[0].score if results else 0.0,
            }
        )

    avg = sum(scores) / len(scores)
    avg_at_1 = sum(scores_at_1) / len(scores_at_1)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n[bold green]Average Keyword Hit Rate[/bold green]")
    print(f"{avg:.3f}")

    print("[bold green]Average Keyword Hit Rate @ 1[/bold green]")
    print(f"{avg_at_1:.3f}")

    print("[bold green]Mean Reciprocal Rank[/bold green]")
    print(f"{mrr:.3f}")

    results_df = pd.DataFrame(rows)
    output_path = "data/results/eval_results.csv"
    results_df.to_csv(output_path, index=False)

    print("[bold green]Saved evaluation results to[/bold green]")
    print(output_path)


if __name__ == "__main__":
    main()