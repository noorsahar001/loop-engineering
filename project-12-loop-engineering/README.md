# Project 12: The Dreaming Loop (Self-Improvement)

A loop that re-reads the failure logs left behind by earlier projects,
**dreams** about the failures that repeat, and turns a repeated failure
into a **proposed rule change** — never deciding, only proposing.

The core idea: a healthy loop does not just run its schedule. It
occasionally *dreams* — it stops executing and reflects on its own past
runs to make itself better. But it never merges its own ideas. A human
holds the gate.

**Concepts demonstrated:** Concept 12 (Spine & Improvement) + Concept 11
(Maker-Checker) + Concept 6 (Schedule) + Part 5 (Human Gate)

---

## Concept 12: The Spine & Improvement

A `dreaming-state.md` file is the loop's **memory**. Every beat the loop
reads it before deciding whether to propose anything.

- It remembers the **last analysis date**.
- It records every **pattern** it has seen (`FAILURE(x3)`, ...).
- It lists every **proposal** it has made (`FAILURE|R2-TEST|3`, ...).

Without this spine, the loop would re-propose the same idea every run.
With it, the loop knows **what it has already said** and moves on to the
next, genuinely new, improvement. Improvement is only real if it is
remembered — otherwise it is just noise.

## Concept 11: Maker-Checker

The improvement loop is built as two halves that never trust each other:

- **Maker (`analyze_logs.py`)** — extracts failures from the raw logs,
  groups them by type, and counts occurrences. It *makes* the analysis.
- **Checker (`dreaming_loop.py`)** — reads the maker's counts, decides
  whether a failure has repeated enough to matter, and checks the
  proposal's evidence is real (dates, counts, log lines) before it is
  allowed to become a proposal.

A proposal only becomes a change after evidence has been verified — the
maker produces, the checker validates.

## Concept 6: Schedule

The loop is designed to run on a **schedule** alongside the projects it
watches (Project 3 / Project 8). Each scheduled beat:

1. Reads the memory spine.
2. Analyses the accumulated failure logs.
3. Detects repeated failures.
4. Proposes one novel rule change (if any).
5. Writes the new memory.
6. Prints a summary — `NO_PATTERNS -> NO_PROPOSAL` on calm runs.

Because it is scheduled, it can reflect **once a day** without a human
being present. On calm days it does nothing but update its memory.

## Part 5: Human Gate

The loop **proposes; it does not decide.**

- Every proposed change is committed to a **feature branch**
  (`dream/<type>/<timestamp>`), never straight to `main`.
- If the GitHub CLI (`gh`) is available, the loop opens a pull request.
- If it is not, it saves the proposal diff under `proposals/` for a
  human to push and merge.
- **A human reviews the evidence and approves the merge.** The loop can
  never merge its own proposal, and `main` is never written to directly.

This is the safety contract: all proposals trace to real logs, and a
human stays in control.

---

## How It Works

```
dreaming_loop.py (orchestrator / CHECKER)
  │
  ├── 1. READ dreaming-state.md        → what have we already proposed?
  │
  ├── 2. ANALYZE via analyze_logs      → extract + count failures (MAKER)
  │        reads project-3 / project-8 logs
  │
  ├── 3. DETECT repeated failures      → count >= threshold (default 2)
  │
  ├── 4. CHECK novelty                 → skip what we already proposed
  │
  ├── 5. PROPOSE rule change as PR     → feature branch + commit + PR
  │        (never a direct commit to main)
  │
  ├── 6. UPDATE dreaming-state.md      → remember the pattern + proposal
  │
  └── 7. PRINT summary                 → "NO_PATTERNS -> NO_PROPOSAL"
```

### The Evidence Rule

**Every proposal MUST cite evidence.** `build_proposal()` in
`dreaming_loop.py` pulls, for the repeated failure type:

- the **occurrence count** and the **threshold**,
- the **dates** observed,
- the exact **log lines** (source file, line number, message).

A proposal with no evidence is never built. The proposal body always
includes an `## Evidence` section and a full list of every matching log
record, so the human reviewer can verify the loop is not guessing.

### Repro: RUN 1 vs RUN 2

RUN 1 — calm logs (no patterns):

```
Log sources analysed: 2
Total failures found: 0
Repeated failure types (>= 2): none

NO_PATTERNS -> NO_PROPOSAL
```

RUN 2 — planted repeated failure (`repeated_schedule.log`):

```
Total failures found: 6
Repeated failure types (>= 2): 2
  - FAILURE: 3x
  - NEEDS HUMAN: 3x

PROPOSAL MADE (as PR): [R2-TEST] Strengthen Test Coverage after 3x repeated 'FAILURE' failures
```

---

## Files

| File | Role | Description |
|------|------|-------------|
| `dreaming_loop.py` | **Orchestrator / Checker** | The improvement loop: analyses logs, detects failures, proposes rule changes as PRs, updates memory |
| `analyze_logs.py` | **Maker** | Parses logs (project-7 dialect + project-8 dialect), groups failures by type, counts occurrences |
| `dreaming-state.md` | **The Spine** | The loop's long-term memory: last analysis date, patterns found, proposals made |
| `rules.md` | **Rule set** | The current rules (Dependency Audit, Test Coverage, Documentation Freshness, Commit Frequency) that the loop can *propose* changing |
| `README.md` | **Documentation** | This file |
| `fixtures/` | **Test data** | Sample logs for RUN 1 (calm) and RUN 2 (repeated failure) |
| `proposals/` | **Human gate output** | Generated on demand: proposal `proposal.diff` for a human to review/merge |

---

## How to Run

```bash
# Point the loop at real logs from Projects 3 and 8 (auto-discovered):
python dreaming_loop.py

# RUN 1 — calm logs, expect "NO_PATTERNS -> NO_PROPOSAL":
python dreaming_loop.py --logs fixtures/calm_audit.log --logs fixtures/calm_schedule.log

# RUN 2 — planted repeated failure, expect a proposal:
python dreaming_loop.py --logs fixtures/repeated_schedule.log

# Inspect the analysis alone (the maker):
python analyze_logs.py --json --logs fixtures/repeated_schedule.log
```

The default source auto-discovery looks for `schedule.log`, `cron.log`,
and any `*.log` (including `audit_*.log`) under `project-3-…` and
`project-8-…`.

---

## Safety

- All proposals trace to **real log lines** — no invention.
- The loop **proposes; it does not decide** (Part 5 Human Gate).
- Changes happen **only via PR**; `main` is never committed to directly.
- The loop **learns what it has seen** via `dreaming-state.md`, so it
  never re-proposes the same change.
- If `gh` is unavailable, the proposal is saved for the human to push.

---

## Success Criteria

- [x] `dreaming_loop.py` reads logs from Project 3 / Project 8
- [x] `dreaming_loop.py` detects repeated failures (count >= threshold)
- [x] `dreaming_loop.py` proposes rule changes as PRs (feature branch), never a direct commit
- [x] `analyze_logs.py` extracts failures, groups by type, counts occurrences
- [x] `dreaming-state.md` tracks last analysis date, patterns found, proposals
- [x] `rules.md` lists the four current rules to be improved
- [x] Every proposal cites evidence (dates, counts, log lines)
- [x] RUN 1 (no patterns) → no PR
- [x] RUN 2 (planted repeated failure) → PR with evidence
- [x] Humans approve before merge; loop proposes, doesn't decide
