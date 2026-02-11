#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/typer_helptree/dev.py

"""
Developer-facing CLI visibility. Great for screenshotting.

```bash
typer-helptree helptree
```

```python
import typer_helptree
subprocess.run("typer-helptree", "helptree")
```
"""
from __future__ import annotations
import typer
from rich.tree import Tree 
from rich.panel import Panel

from .helptree import build_help_tree


def add_typer_helptree(app, console, version: str = "unknown", hidden: bool =True):
    @app.command(name="helptree", hidden = hidden, help="Visualize CLI structure.")
    def help_tree_command(
        ctx: typer.Context,
        version: str = version,
        export_json: bool = typer.Option(False, "--export-json", help="Export to JSON."),
        export_txt: bool = typer.Option(False, "--export-txt", help="Export to TXT.")
    ):
        # Ensure we use ctx.parent.command to get the main app's root command
        root_command = ctx.parent.command 
        app_name = root_command.name or "app"
        
        app_tree = Tree(f"[bold blue]{app_name}[/bold blue] (v{version})", guide_style="cyan")
        
        # This now recurses through the root_command using your original logic
        build_help_tree(root_command, app_tree, ctx)
        
        # 2. Optional Exports
        if export_json or export_txt:
            if export_json:
                from typer_helptree.helptree import build_help_data
                from typer_helptree.io import export_help_json
                data = build_help_data(root_command, ctx, version=version)
                export_help_json(data, app_name)

            if export_txt:
                from typer_helptree.io import export_help_txt
                # Capture the Rich tree as plain text using a dummy console
                from rich.console import Console
                capture_console = Console(width=200, force_terminal=False, color_system=None)
                with capture_console.capture() as capture:
                    capture_console.print(app_tree)
                export_help_txt(capture.get(), app_name)
        
        else:
            # ONLY print if no export flags are set
            console.print(Panel(app_tree, title=f"[bold]{app_name} CLI Help Tree[/bold]", expand=False))