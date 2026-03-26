# src/typer_helptree/utils.py
from __future__ import annotations
import re
from pathlib import Path
from typing import Iterable, Optional
import sys

def updating_target_file_references(
    targets: Optional[Iterable[str]],
    app_name: str,
    version: str
) -> None:
    if not targets:
        return

    pattern_str = rf"({re.escape(app_name)}_v).*?(_helptree\.svg)"
    pattern = re.compile(pattern_str)

    # Use \g<1> to explicitly separate the group ID from the version digits
    replacement = rf"\g<1>{version}\g<2>"

    targets_success = set()
    
    for target in targets:
        path = Path(target)
        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")
        new_content, count = pattern.subn(replacement, content)

        if count > 0:
            path.write_text(new_content, encoding="utf-8")
            print(f"Updated {count} link(s) in {target} to v{version}", file=sys.stderr)

        targets_success.add(target)
        
    return targets_success
