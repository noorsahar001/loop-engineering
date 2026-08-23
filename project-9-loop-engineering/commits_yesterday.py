#!/usr/bin/env python3
"""Summarize commits from yesterday onto claude/summary branch"""

import subprocess
from datetime import datetime, timedelta

def get_yesterday_commits():
    """Get commits from yesterday"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    result = subprocess.run(
        ['git', 'log', '--since', yesterday, '--until', 'today', '--oneline'],
        capture_output=True, text=True
    )

    commits = result.stdout.strip().split('\n')
    return [c for c in commits if c]

def main():
    commits = get_yesterday_commits()

    if not commits:
        print("✓ No commits yesterday")
        return 0

    print(f"Found {len(commits)} commits from yesterday:")
    for commit in commits:
        print(f"  - {commit}")

    # Write summary
    with open('summary.md', 'w') as f:
        f.write(f"# Yesterday's Summary\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"## Commits ({len(commits)} total)\n\n")
        for commit in commits:
            f.write(f"- {commit}\n")

    print("\n✓ Summary written to summary.md")
    return 0

if __name__ == '__main__':
    exit(main())
