from rich.console import Console
from rich.panel import Panel

console = Console()
style = "bold on black"


def print_msg(msg):
    # panel = Panel(f"{msg}", style="bold white on red", expand=False)
    return console.print(f"{msg}", style=style, justify="left")
