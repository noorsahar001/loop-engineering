"""ROUTINE A - Drafter.

Trigger type: ONE-OFF MANUAL INVOKE (no schedule, no API endpoint).
It runs once when a human runs it, mints a reviewable draft, and exits.

It never touches the network and never performs any real work. Its only
job is to produce draft_pending.json in status "PENDING APPROVAL" and
hand the decision to a human. Routine B cannot legally run until that
human personally fires it over the API.
"""

import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFT_PATH = os.path.join(BASE_DIR, "draft_pending.json")
EXECUTE_URL = "http://127.0.0.1:8011/execute"

SAMPLE_TASKS = [
    {"id": 1, "title": "Summarize weekly metrics report", "action": "generate_summary"},
    {"id": 2, "title": "Rename legacy config keys", "action": "batch_rename"},
    {"id": 3, "title": "Send recap email to team list", "action": "notify"},
]


def build_draft():
    return {
        "project": "Project 11 - Two-Routine Gate System",
        "created_by": "routine_a_draft.py (one-off manual invoke)",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PENDING APPROVAL",
        "note": (
            "Nothing here has been executed. This file is a PROPOSAL. "
            "Routine B refuses to act unless its status is exactly "
            "'PENDING APPROVAL' AND a human fires the API call."
        ),
        "tasks": SAMPLE_TASKS,
    }


def print_approval_instructions(draft):
    print()
    print("=" * 64)
    print("STATUS: PENDING APPROVAL - NO WORK HAS BEEN DONE")
    print("=" * 64)
    print(f"Draft written to : {os.path.basename(DRAFT_PATH)}")
    print(f"Tasks proposed   : {len(draft['tasks'])}")
    for task in draft["tasks"]:
        print(f"  #{task['id']} {task['title']} [{task['action']}]")
    print()
    print("APPROVAL REQUIRED BEFORE ANYTHING RUNS:")
    print()
    print("1. REVIEW   Open draft_pending.json and read every task.")
    print("2. APPROVE  Fire Routine B yourself, manually, via curl:")
    print()
    print(f'     curl -X POST {EXECUTE_URL} \\')
    print('          -H "Authorization: Bearer <token-from-.env>"')
    print()
    print("   Routine B has NO schedule. It cannot start itself.")
    print("   Your curl command IS the human gate (A4).")
    print("3. REJECT   Do nothing, edit, or delete the draft.")
    print("            An unfired trigger never executes.")


def main():
    draft = build_draft()
    with open(DRAFT_PATH, "w", encoding="utf-8") as fh:
        json.dump(draft, fh, indent=2)
    print("[ROUTINE A] Draft created (one-off invoke, no schedule).")
    print_approval_instructions(draft)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
