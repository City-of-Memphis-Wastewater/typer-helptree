#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/typer_helptree/cli.py
from __future__ import annotations
import typer
from typing import Literal, List
from typer.models import OptionInfo
from rich.console import Console
from pathlib import Path
from typing import Dict, Optional, Union, List
import pyhabitat
import sys
import os
from importlib.resources import files
from enum import Enum

from typer_helptree.version_info import get_version_from_pyproject

APP_NAME = "typer-tree-demo"

console = Console() # to be above the tkinter check, in case of console.print

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name=APP_NAME,
    help=f"Visualize your entire CLI, beautifully. (v{get_version_from_pyproject()})",
    add_completion=False,
    invoke_without_command = True, 
    no_args_is_help = False,
    context_settings={"ignore_unknown_options": True,
                      "allow_extra_args": True,
                      "help_option_names": ["-h", "--help"]},
)


def debug_callback(value: bool):
#def debug_callback(ctx: typer.Context, value: bool):
    if value:
        # This runs IMMEDIATELY when --debug is parsed, even before --help
         # 1. Access the list of all command-line arguments
        full_command_list = sys.argv
        # 2. Join the list into a single string to recreate the command
        command_string = " ".join(full_command_list)
        # 3. Print the command
        typer.echo(f"command:\n{command_string}\n")
    return value

if "--show-command" in sys.argv or "--debug" in sys.argv: # requires that --show-command flag be used before the sub command
    debug_callback(True)

    
@app.callback()
def main(ctx: typer.Context,
    version: Optional[bool] = typer.Option(
    None, "--version", is_flag=True, help="Show the version."
    ),
    debug: bool = typer.Option(
        False, "--debug", is_flag=True, help="Enable verbose debug logging and echo the full command string."
    ),
    show_command: bool = typer.Option(
        False, "--show-command", is_flag=True, help="Echo the full command string to the console before execution."
    )
    ):
    """
    If no subcommand is provided, launch the GUI.
    """
    if version:
        typer.echo(get_version_from_pyproject())
        raise typer.Exit(code=0)
        
    if ctx.invoked_subcommand is None:
        gui_command()
        raise typer.Exit(code=0)


# help-tree() command: fragile, experimental, defaults to not being included.
if os.environ.get('DEV_TYPER_HELP_TREE',0) in ('true','1'):
    from typer_helptree.helptree import add_typer_help_tree
    add_typer_help_tree(
        app = app,
        console = console)

# Create tools sub-group
tools_app = typer.Typer(help="Additional utility features and maintenance tools.")
app.add_typer(tools_app, name="tools")

@tools_app.command(name="nested-tool")
def tools_nested_tool():
    """Demo"""
    print("This is a demo of a nested command.")

@tools_app.command(name="browse-exports")
def tools_browse_exports():
    """Open the system file explorer at the report output directory."""
    from typer_helptree.helpers import get_export_path
    
    target_dir = get_export_path()
    console.print(f"Opening: [bold cyan]{target_dir}[/bold cyan]")
    
    try:
        pyhabitat.show_system_explorer(path = target_dir)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
    
