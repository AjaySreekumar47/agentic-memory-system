from rich import print

from memory_system.agentic_memory import AgenticMemorySystem


memory = AgenticMemorySystem()

query = "What memory system project is the user trying to build?"

results = memory.retrieve(query)

print(f"\n[bold cyan]Query:[/bold cyan] {query}\n")

for item in results:
    note = item.note

    print("[bold yellow]Retrieved Memory[/bold yellow]")
    print(f"Score: {item.score:.4f}")
    print(f"Source: {item.source}")
    print(f"ID: {note.id}")
    print(f"Content: {note.content}")
    print(f"Context: {note.context}")
    print(f"Keywords: {note.keywords}")
    print(f"Tags: {note.tags}")
    print(f"Links: {note.links}")
    print("-" * 80)

print("\n[bold green]Formatted memory context:[/bold green]")
print(memory.retrieve_context(query))