#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/typer_helptree/helpers.py
from __future__ import annotations
import click
from rich.tree import Tree
from typing import Dict, Any, List

def _get_param_data(param: click.Parameter) -> Dict[str, Any]:
    """
    Extracts raw metadata from a Click parameter for JSON export.
    Uses original logic to handle default values and sentinel values.
    """
    return {
        "name": param.name,
        "opts": getattr(param, 'opts', []),
        "help": getattr(param, 'help', ""),
        "default": str(param.default) if param.default not in (None, click.core.UNSET) else None
    }

def _format_param_label(param: click.Parameter) -> str:
    """
    Formats a Click parameter into a colorized string for the Rich tree.
    Preserves the 'human_readable_name' for Arguments and '-' check for Options.
    """
    is_option = hasattr(param, 'opts') and param.opts and param.opts[0].startswith('-')
    
    if is_option:
        flag_names = " / ".join(param.opts)
        default_value = getattr(param, 'default', None)
        
        default_str = ""
        if default_value not in (None, click.core.UNSET):
            default_str = f" [dim](default: {default_value})[/dim]"
            
        return f"[green]{flag_names}[/green]: [dim]{param.help or ''}[/dim]{default_str}"
    
    # Handling Positional Arguments
    arg_name = param.human_readable_name.upper()
    return f"[magenta]ARG: {arg_name}[/magenta]: [dim]{param.help or ''}[/dim]"

def _add_parameters_to_node(click_command: click.Command, tree_node: Tree) -> None:
    """Extracts parameters and appends them to the Rich tree node."""
    if not hasattr(click_command, 'params') or not click_command.params:
        return

    visible_params = [
        p for p in click_command.params 
        if not (hasattr(p, 'opts') and any(opt in ("-h", "--help") for opt in p.opts))
    ]

    if visible_params:
        params_branch = tree_node.add("[yellow]Parameters[/yellow]")
        for param in visible_params:
            params_branch.add(_format_param_label(param))

def build_help_tree(click_command: click.Command, tree_node: Tree, ctx: click.Context) -> None:
    """Builds the Rich Tree structure recursively."""
    _add_parameters_to_node(click_command, tree_node)

    if isinstance(click_command, click.Group):
        for cmd_name in sorted(click_command.list_commands(ctx)):
            cmd = click_command.get_command(ctx, cmd_name)
            if not cmd or cmd.name == "helptree":
                continue
            
            #short_help = cmd.get_short_help_str() or "No description available."
            #sub_node = tree_node.add(f"[bold white]{cmd.name}[/bold white] - [dim]{short_help}[/dim]")
            raw_help = cmd.help or ""
            full_description = raw_help.splitlines()[0].strip() if raw_help else "No description available."
            sub_node = tree_node.add(f"[bold white]{cmd.name}[/bold white] - [dim]{full_description}[/dim]")
            build_help_tree(cmd, sub_node, ctx)

def build_help_data(click_command: click.Command, ctx: click.Context) -> Dict[str, Any]:
    """Recursively builds a dictionary for JSON export, utilizing _get_param_data."""
    node_data = {
        "name": click_command.name,
        "help": click_command.get_short_help_str(),
        "parameters": [],
        "subcommands": []
    }

    if hasattr(click_command, 'params'):
        for param in click_command.params:
            if hasattr(param, 'opts') and any(opt in ("-h", "--help") for opt in param.opts):
                continue
            # Logic restored: uses the helper function
            node_data["parameters"].append(_get_param_data(param))

    if isinstance(click_command, click.Group):
        for cmd_name in sorted(click_command.list_commands(ctx)):
            cmd = click_command.get_command(ctx, cmd_name)
            if not cmd or cmd.name == "helptree":
                continue
            node_data["subcommands"].append(build_help_data(cmd, ctx))

    return node_data