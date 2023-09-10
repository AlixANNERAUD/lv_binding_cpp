from rich.console import Console
from rich.table import Table
from rich.traceback import install

Console = Console()

install(show_locals=True)

Log_Table = Table(title = "LVGL Bindings Generator", expand=True)

Log_Table.add_column("Type", width=3, justify="center")
Log_Table.add_column("Message")

def Update_Console():
    Console.clear()
    Console.print(Log_Table)

def Title(Title):
    Log_Table.add_row("- - - -", "[bold]- " + Title + "[/bold]")
    Update_Console()

def Error(Message):
    Log_Table.add_row("[bold red]Error[/bold red]", "\t- " + Message)
    Update_Console()

def Warning(Message):
    Log_Table.add_row("[bold yellow]Warning[/bold yellow]", "\t- " + Message)
    Update_Console()

def Information(Message):
    Log_Table.add_row("[bold blue]Information[/bold blue]", "\t- " + Message)
    Update_Console()

def Success(Message):
    Log_Table.add_row("[bold green]Success[/bold green]", "\t- " + Message)
    Update_Console()

def Debug(Message):
    Log_Table.add_row("[bold magenta]Debug[/bold magenta]", "\t- " + Message)
    Update_Console()