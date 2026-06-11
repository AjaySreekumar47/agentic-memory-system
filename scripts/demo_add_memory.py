from rich import print

from memory_system.agentic_memory import AgenticMemorySystem


memory = AgenticMemorySystem()

examples = [
    "The user wants to build an efficient memory system for an LLM chatbot and compare four research paper approaches.",
    "The user prefers building the project locally in VS Code instead of Colab because this is a systems engineering project.",
    "The first paper being studied is A-MEM, which uses structured memory notes, link generation, and memory evolution.",
]

for item in examples:
    note = memory.add_memory(item)

    print("\n[bold green]Added memory[/bold green]")
    print(f"ID: {note.id}")
    print(f"Content: {note.content}")
    print(f"Keywords: {note.keywords}")
    print(f"Tags: {note.tags}")
    print(f"Context: {note.context}")
    print(f"Links: {note.links}")