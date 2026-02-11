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
import click

from .helptree import build_help_tree


def add_typer_helptree(app, console, version: str = "unknown", hidden=True):
    @app.command(
        name="helptree",
        hidden=hidden,
        help="Show all commands and options in a tree structure.")
    def help_tree_command_(ctx: typer.Context):
        """
        Fragile developer-facing function.
        Generates and prints a tree view of the CLI structure (commands and flags).
        """
        root_app_command = ctx.parent.command 
        
        # 1. Start the Rich Tree structure
        app_tree = Tree(
            f"[bold blue]{root_app_command.name}[/bold blue] (v{version})",
            guide_style="cyan"
        )

        # 2. Iterate through all subcommands of the main app
        for command_name in sorted(root_app_command.commands.keys()):
            command = root_app_command.commands[command_name]
            
            if command.name == "helptree":
                continue

            #help_text = command.help.splitlines()[0].strip() if command.help else "No help available."
            # Instead, this uses Click's internal logic to get the first sentence or short summary
            help_text = command.get_short_help_str() or "No help available."

            command_branch = app_tree.add(f"[bold white]{command.name}[/bold white] - [dim]{help_text}[/dim]")

            # 3. Add Arguments and Options (Flags)
            params_branch = command_branch.add("[yellow]Parameters[/yellow]:")
            
            if not command.params:
                params_branch.add("[dim]None[/dim]")
            
            for param in command.params:
                # New, safer check: Check if param is an Option by looking for opts attribute 
                # and ensuring it has a flag declaration (starts with '-')
                is_option = hasattr(param, 'opts') and param.opts and param.opts[0].startswith('-')
                
                if is_option:
                    # This is an Option/Flag
                    flag_names = " / ".join(param.opts)
                    
                    # Filter out the default Typer/Click flags like --help
                    if flag_names in ("-h", "--help"):
                        continue
                    
                    # Handling default value safely
                    # Check for None explicitly, as well as the Typer/Click internal sentinel value for not provided.
                    default_value = getattr(param, 'default', None)

                    # This is the sentinel value used by the Click/Typer internals
                    if default_value not in (None, click.core.UNSET):
                        default = f"[dim] (default: {default_value})[/dim]"
                    else:
                        default = ""
                    
                    params_branch.add(f"[green]{flag_names}[/green]: [dim]{param.help}[/dim]{default}")
                else:
                    # This is an Argument (Positional)
                    # Arguments have a single name property, not an opts list.
                    arg_name = param.human_readable_name.upper()
                    params_branch.add(f"[magenta]ARG: {arg_name}[/magenta]: [dim]{param.help}[/dim]")

        # 4. Print the final Panel containing the tree
        console.print(Panel(app_tree, title=f"[bold]{root_app_command.name} CLI Help Tree[/bold]", border_style="blue"))


    @app.command(name="helptree", help="Visualize CLI structure.")
    def help_tree_command(
        ctx: typer.Context,
        version: str = "unknown",
        export_json: bool = typer.Option(False, "--json", help="Export to JSON."),
        export_txt: bool = typer.Option(False, "--txt", help="Export to TXT.")
    ):
        # Ensure we use ctx.parent.command to get the main app's root command
        root_command = ctx.parent.command 
        app_name = root_command.name or "app"
        
        app_tree = Tree(f"[bold blue]{app_name}[/bold blue] (v{version})", guide_style="cyan")
        
        # This now recurses through the root_command using your original logic
        build_help_tree(root_command, app_tree, ctx)
        
        console.print(Panel(app_tree, title=f"[bold]{app_name} CLI Help Tree[/bold]", expand=False))
        
        # ... Export logic remains the same ...

        # 2. Optional Exports
        if export_json:
            from typer_helptree.helptree import build_help_data
            from typer_helptree.io import export_help_json
            data = build_help_data(root_command, ctx)
            export_help_json(data, app_name)

        if export_txt:
            from typer_helptree.io import export_help_txt
            # Capture the Rich tree as plain text using a dummy console
            from rich.console import Console
            capture_console = Console(width=100, force_terminal=False, color_system=None)
            with capture_console.capture() as capture:
                capture_console.print(app_tree)
            export_help_txt(capture.get(), app_name)