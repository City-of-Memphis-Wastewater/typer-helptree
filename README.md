# typer-helptree

The `helptree` command can be added to your Typer CLI.

## User story
- **Dev**: *"I want to a screenshot of my CLI structure, to add to my GitHub release and to my README."*

```bash
typer-helptree helptree
```

![Screenshot of the typer-helptree helptree](https://raw.githubusercontent.com/City-of-Memphis-Wastewater/typer-helptree/main/assets/typer-helptree_v0.2.4.png)

## How To 

Use `helptree` in your Typer CLI: 

```python
# src/your_fancy_app/cli.py

# --- External Imports ---
import typer
from rich.console import Console
# Import the add_typer_helptree command.
from typer_helptree.helptree import add_typer_helptree

# --- Internal Imports ---
from ._version import __version__ # or however you do this.

# --- Typical Typer App Instantiation ---
APP_NAME "your-fancy-app"
console = Console()
app = typer.Typer(
    name=APP_NAME
)

# --- The Magic ---

add_typer_helptree(app=app, console=console, version = __version__, hidden=True)

```

And then, from the command line:

```bash
your-fancy-app helptree
```
---

### Projects that use **typer-helptree**

- https://pypi.org/project/pdflinkcheck/
- https://pypi.org/project/dworshak/
