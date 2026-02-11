#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/typer_helptree/helpers.py

"""

"""
from __future__ import annotations
import click
from rich.tree import Tree

def _format_param_label(param: click.Parameter) -> str:
    """
    Formats a Click parameter into a colorized string for the Rich tree.
    
    Handles the distinction between Options (flags) and Arguments (positional).
    """
    if isinstance(param, click.Option):
        flags = " / ".join(param.opts)
        # Handle default values, ignoring None or Click's internal UNSET sentinel
        default = ""
        if param.default not in (None, click.core.UNSET):
            default = f" [dim](default: {param.default})[/dim]"
        
        return f"[green]{flags}[/green]: [dim]{param.help or ''}[/dim]{default}"
    
    # Fallback for Positional Arguments
    arg_name = param.human_readable_name.upper()
    return f"[magenta]ARG: {arg_name}[/magenta]: [dim]{param.help or ''}[/dim]"


def _add_parameters_to_node(click_command: click.Command, tree_node: Tree)-> None:
    """
    Extracts visible parameters from a command and appends them to the tree node.
    """
    if not hasattr(click_command, 'params') or not click_command.params:
        return

    # Filter out standard help options to keep the tree focused on custom logic
    visible_params = [
        p for p in click_command.params 
        if not (isinstance(p, click.Option) and any(opt in ("-h", "--help") for opt in p.opts))
    ]

    if visible_params:
        params_branch = tree_node.add("[yellow]Parameters[/yellow]")
        for param in visible_params:
            params_branch.add(_format_param_label(param))


def build_help_tree(click_command: click.Command, tree_node: Tree, ctx: click.Context)-> None:
    """
    Recursively navigates Click commands and groups to build a hierarchical 
    visualization of the CLI structure.
    """
    # 1. Process the parameters for the current command level
    _add_parameters_to_node(click_command, tree_node)

    # 2. If the command is a Group (nested Typer app), traverse its children
    if isinstance(click_command, click.Group):
        traverse_click_group_children()

def traverse_click_group_children(click_command: click.Command, tree_node: Tree, ctx: click.Context)-> None:
    # Sort command names to ensure consistent output across different environments
    for cmd_name in sorted(click_command.list_commands(ctx)):
        cmd = click_command.get_command(ctx, cmd_name)
        
        # Skip invalid commands or the helptree command itself to avoid recursion loops
        if not cmd or cmd.name == "helptree":
            continue
        
        short_help = cmd.get_short_help_str() or "No description available."
        sub_node = tree_node.add(f"[bold white]{cmd.name}[/bold white] - [dim]{short_help}[/dim]")
        
        # Recursively build branches for sub-commands or nested apps
        build_help_tree(cmd, sub_node, ctx)