"""
schedule.py — Scheduled Loop with Spine (Concept 6 + Concept 12).

This is the orchestrator. It runs on a schedule (cron / Task Scheduler)
and proves the "spine" concept: progress.md persists state between runs,
so the loop never repeats work it already did.

How it works each run:
  1. Read progress.md (the spine) to learn what was already found
  2. Run gather.py to collect fresh data
  3. Compare: which findings are TRULY NEW?
  4. If new findings exist → append to progress.md
  5. If nothing new → just update the timestamp
  6. Print what changed (or "No new findings")
"""

import os
import re
import subprocess
import sys
from datetime import datetime


PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "progress.md"
)
GATHER_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "gather.py"
)


def read_spine(path):
    """Read progress.md and extract existing findings as a set of strings."""
    if not os.path.exists(path):
        return "Never", "None", set()

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract last updated timestamp
    m_updated = re.search(r"Last updated:\s*(.+)", content)
    last_updated = m_updated.group(1).strip() if m_updated else "Never"

    m_run = re.search(r"Last run date:\s*(.+)", content)
    last_run = m_run.group(1).strip() if m_run else "None"

    # Extract findings (lines starting with "- " under ## Findings)
    findings = set()
    in_findings = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Findings"):
            in_findings = True
            continue
        if in_findings and stripped.startswith("## "):
            break  # next section
        if in_findings and stripped.startswith("- "):
            findings.add(stripped[2:])  # strip "- " prefix

    return last_updated, last_run, findings


def write_spine(path, old_findings, new_finding_lines, timestamp, run_date):
    """Write updated progress.md with old + new findings."""
    header = f"""# Progress Log

Last updated: {timestamp}
Last run date: {run_date}

## Findings
"""
    all_findings = sorted(old_findings | set(new_finding_lines))
    body = "\n".join(f"- {f}" for f in all_findings) if all_findings else "(No findings yet)"

    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n" + body + "\n")


def run_gather():
    """Run gather.py and return its output lines."""
    result = subprocess.run(
        [sys.executable, GATHER_SCRIPT],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[ERROR] gather.py failed:\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip().splitlines()


def extract_gather_findings(lines):
    """Extract finding strings from gather.py output."""
    findings = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            findings.append(stripped[2:])
    return findings


def main():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    run_date = now.strftime("%Y-%m-%d")

    # Step 1: Read the spine
    last_updated, last_run, existing = read_spine(PROGRESS_FILE)
    print(f"=== Schedule Run: {timestamp} ===")
    print(f"Last run: {last_run}")
    print(f"Existing findings in spine: {len(existing)}")

    # Step 2: Run gather.py
    print("\n[Gathering new data...]")
    gather_lines = run_gather()
    new_findings = extract_gather_findings(gather_lines)
    print(f"Gathered {len(new_findings)} finding(s):")
    for f in new_findings:
        print(f"  - {f}")

    # Step 3: Compare — find TRULY NEW findings
    new_set = set(new_findings)
    truly_new = new_set - existing

    # Step 4: Update spine
    if truly_new:
        print(f"\n>>> {len(truly_new)} NEW finding(s) added to progress.md:")
        for f in sorted(truly_new):
            print(f"  + {f}")
        write_spine(PROGRESS_FILE, existing, truly_new, timestamp, run_date)
    else:
        print("\n>>> No new findings — spine already has everything.")
        print(">>> Only updating timestamp.")
        write_spine(PROGRESS_FILE, existing, set(), timestamp, run_date)

    print(f"\nSpine updated. Next run will build on {len(existing | truly_new)} finding(s).")


# TODO: test new finding for Run 2

if __name__ == "__main__":
    main()
