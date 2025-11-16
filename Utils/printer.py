from rich.console import Console
from rich.table import Table

console = Console()

def print_tasks(tasks):
    table = Table(title="Your Tasks")

    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Due")
    table.add_column("Keep?")

    for t in tasks:
        table.add_row(str(t.id), t.title, str(t.due), "Yes" if t.keep else "No")

    console.print(table)


