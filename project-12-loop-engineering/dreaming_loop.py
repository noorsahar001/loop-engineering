"""dreaming_loop.py — The Self-Improving Dreaming Loop.

The loop "dreams": it re-reads the observability logs left behind by
Projects 3 and 8, looks for failures that repeat across runs, and turns
a repeated failure into a **proposed rule change**.

Core discipline:
- Every proposal MUST cite evidence (dates, counts, log lines).
- Changes happen ONLY via a pull request — never a direct commit to main.
- The loop remembers what it has already seen in `dreaming-state.md` so
  it never proposes the same change twice.
- The loop proposes; it does not decide. A human approves before merge
  (Part 5: Human Gate).

Flow:
    1. READ dreaming-state.md          (what have we already proposed?)
    2. ANALYZE logs via analyze_logs   (extract + count failures)
    3. DETECT repeated failures        (count >= threshold)
    4. CHECK novelty                   (not already proposed/seen)
    5. PROPOSE rule change as PR       (branch + commit, evidence cited)
    6. UPDATE dreaming-state.md        (remember what we saw)
    7. PRINT summary                   ("no patterns -> no PR" on calm runs)

Safe by default: with calm logs (no repeated failures) the loop proposes
nothing and emits "NO_PATTERNS -> NO_PROPOSAL".

stdlib only. The PR is created with the git CLI and, when available,
the GitHub CLI (`gh`). If `gh` is absent, the proposal is committed to a
feature branch and its diff is saved under `proposals/` for a human to
push and merge.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

import analyze_logs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
STATE_PATH = os.path.join(BASE_DIR, "dreaming-state.md")
RULES_PATH = os.path.join(BASE_DIR, "rules.md")
PROPOSAL_DIR = os.path.join(BASE_DIR, "proposals")

# A failure type must repeat at least this many times to be "repeated".
PROPOSAL_THRESHOLD = 2

# Map a failure type to the rule it should strengthen.
# Each entry says WHICH rule to touch and the human-facing rationale.
RULE_HOOKS = {
    "FAILURE": {
        "rule_id": "R2-TEST",
        "rule_name": "Test Coverage",
    },
    "NEEDS HUMAN": {
        "rule_id": "R4-COMMIT",
        "rule_name": "Commit Frequency",
    },
    "BUDGET EXCEEDED": {
        "rule_id": "R1-DEP",
        "rule_name": "Dependency Audit",
    },
    "MONTHLY BUDGET": {
        "rule_id": "R3-DOC",
        "rule_name": "Documentation Freshness",
    },
    "WEEKLY LIMIT": {
        "rule_id": "R3-DOC",
        "rule_name": "Documentation Freshness",
    },
    "REVIEW FAILED": {
        "rule_id": "R2-TEST",
        "rule_name": "Test Coverage",
    },
}
DEFAULT_RULE = {"rule_id": "R3-DOC", "rule_name": "Documentation Freshness"}


def run_git(args, cwd=REPO_ROOT):
    """Run a git command and return (returncode, stdout)."""
    proc = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def has_gh():
    """True if the GitHub CLI is available on PATH."""
    return shutil.which("gh") is not None


def read_state():
    """Parse dreaming-state.md into a structured dict."""
    state = {
        "last_analysis": None,
        "last_run": None,
        "patterns": [],
        "proposals": [],
    }
    if not os.path.isfile(STATE_PATH):
        return state

    with open(STATE_PATH, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    m = re.search(r"last_analysis`:\s*(.*)", text)
    if m:
        state["last_analysis"] = m.group(1).strip()

    m = re.search(r"last_run`:\s*(.*)", text)
    if m:
        state["last_run"] = m.group(1).strip()

    for m in re.finditer(r"^- Pattern: `([^`]+)`\s*$", text, re.MULTILINE):
        state["patterns"].append(m.group(1))

    for m in re.finditer(r"^- Proposal: `([^`]+)`\s*$", text, re.MULTILINE):
        state["proposals"].append(m.group(1))

    return state


def normalize_failure_type(raw):
    """Map a failure type string to a canonical hook key."""
    upper = raw.upper()
    if "NEEDS HUMAN" in upper:
        return "NEEDS HUMAN"
    if "BUDGET EXCEEDED" in upper:
        return "BUDGET EXCEEDED"
    if "MONTHLY BUDGET" in upper or "WEEKLY LIMIT" in upper:
        return "MONTHLY BUDGET"
    if "REVIEW FAILED" in upper:
        return "REVIEW FAILED"
    if "FAILURE" in upper:
        return "FAILURE"
    return "FAILURE"


def build_proposal(ftype, failures, count):
    """Assemble a rule-change proposal with full evidence citations."""
    hook = RULE_HOOKS.get(normalize_failure_type(ftype), DEFAULT_RULE)

    # Evidence: 3 sample log lines from real records + full list.
    sample_lines = []
    for f in failures:
        sample_lines.append(
            "  [{0}] {1} ({2}:{3}) {4}".format(
                f["timestamp"], f["type"], f["source"], f["line"], f["message"]
            )
        )

    dates = ", ".join(sorted({f["timestamp"][:10] for f in failures}))

    title = (
        f"[{hook['rule_id']}] Strengthen {hook['rule_name']} after "
        f"{count}x repeated '{ftype}' failures"
    )

    evidence_block = "\n".join(sample_lines[:6] if sample_lines else ["  (none)"])

    body = """## Why

The Dreaming Loop detected a failure type that repeats across real logs
from Projects 3 and 8. A repeated failure means the current rule is not
enough; the rule should be strengthened.

## Evidence

Failure type: **{type}**
Occurrence count: **{count}** (proposal threshold: {threshold})
Dates observed: {dates}

Relevant log lines:

```
{evidence}
```

Full list ({total} total):
""".format(
        type=ftype,
        count=count,
        threshold=PROPOSAL_THRESHOLD,
        dates=dates,
        evidence=evidence_block,
        total=len(failures),
    )

    for f in failures:
        body += (
            "- [{0}] {1} ({2}:{3}) {4}\n".format(
                f["timestamp"], f["type"], f["source"], f["line"], f["message"]
            )
        )

    body += """

## Proposed change: {rule_id} — {rule_name}

The current rule text in `rules.md` does not guard against this repeated
failure. Propose adding a hard guard: when the failure type `{type}`
occurs more than `{count}` times across beats, the loop must stop and
require human intervention (Part 5: Human Gate) before continuing.

This proposal cites dates, counts, and specific log lines. It does not
self-merge. A human must review and approve this pull request.
""".format(
        rule_id=hook["rule_id"],
        rule_name=hook["rule_name"],
        type=ftype,
        count=count,
    )

    return {
        "failure_type": ftype,
        "count": count,
        "rule_id": hook["rule_id"],
        "rule_name": hook["rule_name"],
        "title": title,
        "body": body,
        "signature": "{type}|{rule_id}|{count}".format(
            type=ftype, rule_id=hook["rule_id"], count=count
        ),
    }


def write_state(records):
    """Regenerate dreaming-state.md from the current records."""
    patterns = records["patterns"]
    proposals = records["proposals"]

    lines = []
    lines.append("# Dreaming State — the Loop's Memory\n")
    lines.append(
        "<!-- This file is regenerated by dreaming_loop.py on every beat. "
        "Do not hand-edit the machine fields. -->\n"
    )
    lines.append("This file records the loop's long-term memory: the last")
    lines.append("analysis date, the patterns found, and every proposal/PR.\n")
    lines.append("---\n")
    lines.append("## Last Analysis Date\n")
    lines.append("- `last_analysis`: {0}".format(records["last_analysis"]))
    lines.append("- `last_run`: {0}".format(records["last_run"]))
    lines.append("\n## Patterns Found\n")
    if patterns:
        for p in patterns:
            lines.append("- Pattern: `{0}`".format(p))
    else:
        lines.append("_No patterns have been found yet._")
    lines.append("\n## Proposals\n")
    if proposals:
        for p in proposals:
            lines.append("- Proposal: `{0}`".format(p))
    else:
        lines.append("_No proposals have been made yet._")
    lines.append("")

    with open(STATE_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def commit_rule_change(proposal, branch):
    """Commit the proposed rule change on a dedicated branch (no direct main)."""
    # Read current rules so the branch starts from the real file.
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as fh:
            rules_text = fh.read()
    except FileNotFoundError:
        rules_text = "# Rules\n"

    # Build the amended rules.md text for the proposal.
    amendment = (
        "\n---\n\n"
        "## Proposed Amendment: {rule_id} — {rule_name}\n\n"
        "PENDING HUMAN APPROVAL. Proposed by the Dreaming Loop on "
        "{date} after {count}x repeated `{ftype}` failures.\n\n"
        "{body}\n"
    ).format(
        rule_id=proposal["rule_id"],
        rule_name=proposal["rule_name"],
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        count=proposal["count"],
        ftype=proposal["failure_type"],
        body=(
            "> This section is provisional and is removed or kept only "
            "after the human decides on this pull request."
        ),
    )
    proposed_rules = rules_text + amendment

    # Write the proposal detail file too.
    os.makedirs(PROPOSAL_DIR, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", proposal["title"]).strip("-").lower()
    proposal_doc = os.path.join(PROPOSAL_DIR, slug + ".md")
    with open(proposal_doc, "w", encoding="utf-8") as fh:
        fh.write(
            "# Proposal: {0}\n\n{1}\n\n## Branch\n\n`{2}`\n\n"
            "## Status\n\nOPEN — awaiting human review and merge.\n".format(
                proposal["title"], proposal["body"], branch
            )
        )

    # Only touch rules.md on the dedicated branch — never on main.
    checkout_rc, checkout_out = run_git(["checkout", "-b", branch])
    if checkout_rc != 0:
        # Could not create the feature branch; do NOT touch main.
        return checkout_rc, "could not create branch {0}: {1}".format(
            branch, checkout_out.strip()
        )
    try:
        with open(RULES_PATH, "w", encoding="utf-8") as fh:
            fh.write(proposed_rules)
        # Git paths are relative to the repo root (same as RULES_PATH IS).
        run_git(["add", RULES_PATH, proposal_doc])
        rc, out = run_git(["commit", "-m", proposal["title"]])
        return rc, out
    finally:
        # Return to main regardless of commit success, and drop any
        # working-tree residue so main stays untouched (the proposal
        # lives only on its feature branch).
        run_git(["checkout", "main"])
        run_git(["checkout", "--", RULES_PATH])


def open_or_save_pr(proposal, branch):
    """Open a PR with `gh`, or fall back to saving the diff for a human."""
    if has_gh():
        rc, out = subprocess.run(
            [
                "gh", "pr", "create",
                "--base", "main",
                "--head", branch,
                "--title", proposal["title"],
                "--body", proposal["body"],
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        if rc == 0:
            return "PR_CREATED", (out or "").strip()
        return "PR_FAILED_GH", (out or "").strip()

    # Fallback: capture the diff so a human can open the PR manually.
    rc, diff = run_git(["diff", "main..." + branch])
    os.makedirs(PROPOSAL_DIR, exist_ok=True)
    diff_path = os.path.join(PROPOSAL_DIR, "proposal.diff")
    with open(diff_path, "w", encoding="utf-8") as fh:
        fh.write(diff or "")
    return "PR_SAVED_FOR_HUMAN", diff_path


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]

    # Optional override for the log sources & threshold (used by tests).
    log_paths = []
    threshold = PROPOSAL_THRESHOLD
    quiet = "--quiet" in argv
    it = iter(argv)
    for arg in it:
        if arg == "--logs":
            log_paths.append(next(it))
        elif arg == "--threshold":
            threshold = int(next(it))

    if not log_paths:
        log_paths = analyze_logs.default_sources()

    now = datetime.now()
    now_ts = now.strftime("%Y-%m-%d %H:%M:%S")

    state = read_state()

    # 1. ANALYZE the logs.
    analysis = analyze_logs.analyze_logs(log_paths)

    # 2. DETECT repeated failures -> group failures by type.
    by_type = {}
    for f in analysis["failures"]:
        key = normalize_failure_type(f["type"])
        by_type.setdefault(key, []).append(f)

    repeated = {
        ftype: recs
        for ftype, recs in by_type.items()
        if len(recs) >= threshold
    }

    # Track every distinct pattern we observed (for the memory file).
    for ftype, recs in by_type.items():
        label = "{ftype}(x{count})".format(ftype=ftype, count=len(recs))
        if label not in state["patterns"]:
            state["patterns"].append(label)

    proposal_made = None
    pr_result = None

    # 3/4. For each repeated failure, propose if it is novel (never seen).
    for ftype in sorted(repeated):
        recs = repeated[ftype]
        proposal = build_proposal(ftype, recs, len(recs))

        # Novelty check: do not re-propose a signature we already logged.
        if proposal["signature"] in state["proposals"]:
            if not quiet:
                print(
                    "SKIP: '{0}' already proposed. Not re-proposing.".format(
                        proposal["signature"]
                    )
                )
            continue

        if not quiet:
            print("PROPOSE: {0}".format(proposal["title"]))

        branch = "dream/{0}/{1}".format(
            ftype.lower().replace(" ", "-"),
            now.strftime("%Y%m%d-%H%M%S"),
        )

        rc, commit_out = commit_rule_change(proposal, branch)
        if rc != 0:
            if not quiet:
                print("COMMIT FAILED on branch {0}: {1}".format(branch, commit_out))
            continue

        try:
            pr_result = open_or_save_pr(proposal, branch)
        except Exception as exc:  # noqa: BLE001 - never let the loop crash
            if not quiet:
                print(
                    "PR STEP FAILED (change stays on branch {0}): {1}".format(
                        branch, exc
                    )
                )
            continue

        state["proposals"].append(proposal["signature"])
        proposal_made = proposal
        break  # one proposal per beat is enough; keep it reviewable

    # 5/6. Update the memory.
    state["last_analysis"] = now_ts
    state["last_run"] = now_ts
    write_state(state)

    # 7. Report.
    lines = []
    lines.append("=" * 60)
    lines.append("DREAMING LOOP RUN  —  {0}".format(now_ts))
    lines.append("=" * 60)
    lines.append("Log sources analysed: {0}".format(len(log_paths)))
    lines.append("Total failures found: {0}".format(analysis["total"]))
    lines.append("Repeated failure types (>= {0}): {1}".format(
        threshold, len(repeated) or "none"))
    for ftype, recs in repeated.items():
        lines.append("  - {0}: {1}x".format(ftype, len(recs)))
    if proposal_made:
        lines.append("")
        lines.append("PROPOSAL MADE (as PR): {0}".format(proposal_made["title"]))
        lines.append("  rule:  {0} - {1}".format(
            proposal_made["rule_id"], proposal_made["rule_name"]))
        lines.append("  count: {0} ({1})".format(proposal_made["count"],
                                                 proposal_made["failure_type"]))
        lines.append("  PR:    {0} -> {1}".format(pr_result[0], pr_result[1]))
    else:
        lines.append("")
        lines.append("NO_PATTERNS -> NO_PROPOSAL (no repeated failures to fix)")

    out = "\n".join(lines)
    if not quiet:
        print(out)

    return 0 if proposal_made is None else 0


if __name__ == "__main__":
    sys.exit(main())
