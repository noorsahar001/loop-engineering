"""
gather.py — Worker script for Concept 6 (Scheduled Loop).

Scans the workspace for:
  1. TODO comments in .py files
  2. Recently modified files in this project folder

Outputs a structured summary that schedule.py reads and compares.
"""

import os
import re
from datetime import datetime, timedelta


def scan_todos(root_dir):
    """Scan for TODO comments in .py files.

    Skips docstrings and only matches lines where '# TODO' appears
    as an actual code comment.
    """
    todo_pattern = re.compile(r"#\s*TODO\b", re.IGNORECASE)
    todos = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                in_docstring = False
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        stripped = line.strip()
                        # Track triple-quoted docstrings
                        count = stripped.count('"""')
                        if count % 2 == 1:
                            in_docstring = not in_docstring
                        if in_docstring:
                            continue
                        if todo_pattern.search(line):
                            rel = os.path.relpath(fpath, root_dir)
                            todos.append(f"TODO in {rel}:{i} — {stripped}")
            except OSError:
                continue
    return todos


def scan_recent_files(project_dir):
    """List files modified in the last 24 hours within project_dir."""
    cutoff = datetime.now() - timedelta(hours=24)
    recent = []
    for dirpath, _, filenames in os.walk(project_dir):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                if mtime >= cutoff:
                    recent.append(os.path.relpath(fpath, project_dir))
            except OSError:
                continue
    return sorted(recent)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)  # loop-engineering/
    project_dir = script_dir  # project-3-loop-engineering/
    today = datetime.now().strftime("%Y-%m-%d")

    todos = scan_todos(workspace_dir)
    recent = scan_recent_files(project_dir)

    # Output structured findings
    print(f"## Findings ({today})")
    for t in todos:
        print(f"- {t}")
    if recent:
        print(f"- Modified: {', '.join(recent)}")
    else:
        print("- No recently modified files")

    # Metadata line (used by schedule.py for dedup context)
    todo_count = len(todos)
    file_count = len(recent)
    print(f"- Summary: {todo_count} TODO(s), {file_count} recently modified file(s)")


if __name__ == "__main__":
    main()
# TODO: fix this later
