# Loop Engineering — Projects 1–12

A hands-on, from-scratch journey through **loop engineering**: building automated systems that wake up, do work, verify it, remember state, and (in the later projects) improve themselves. Each numbered folder is a self-contained, runnable demonstration of one specific Loop Engineering concept. Every project has its own README; the ones in the repo are preserved and authoritative — this top-level document is an index and guided walkthrough.

---

## Overview

### What is Loop Engineering?

Loop engineering is the discipline of building **reliable automation loops**: systems that
periodically (or on demand) wake up, do bounded work, verify the result, record what happened,
and repeat — without a human staring at a terminal. The hard problems are not "write a script" but
"How do I know it actually worked?", "What memory does it keep between runs?", "How do I stop it
from burning money?", and "Who decides what it is allowed to change?"

### The purpose of these 12 projects

The projects progress from a **naïve monitoring loop** (Project 1) toward a **self-improving loop
that proposes its own rule changes** (Project 12). Along the way each project isolates and proves a
single concept, so a learner can see *exactly* what makes a "loop" versus a one-off script:

- **Monitoring** — watching for a condition (P1)
- **Feedback / verification** — the loop uses an external signal (test exit codes) as truth (P2)
- **Scheduling & persistence** — loops that survive across sessions via a memory "spine" (P3)
- **Isolation & reusable instructions** — working in safe branches driven by skills (P4)
- **Engine vs. Loop** — proving the difference between stateless orchestration and a real loop (P5)
- **Event-driven behavior** — reacting to external events instead of a timer (P6)
- **Observability & cost** — logging, diagnosing failures without replay, and budgeting (P7)
- **A full combined capstone** — every earlier concept assembled into one daily loop (P8)
- **Rehearsal & honest verification** — one-off runs and reading transcripts, not status colors (P9)
- **Secrets & environments** — keeping credentials out of Git and in the environment (P10)
- **Human gates & API triggers** — automation that cannot run without an explicit human decision (P11)
- **The "dreaming" loop** — a loop that reflects on its own past failures and proposes improvements (P12)

> Everything documented here is **based only on what actually exists in this repository**. Where a
> project is incomplete or depends on an external system (e.g., GitHub), that is stated explicitly.

---

## Projects Overview

| Project | Name | Main Concept | Key Files | Status |
|---------|------|--------------|-----------|--------|
| [Project 1](./project-1-loop-engineering) | A Watch Loop | In-session monitoring loop | `long_task.py`, `monitor.py` | Complete |
| [Project 2](./project-2-loop-engineering) | Make the Test Pass, then Stop | Conditional loop + maker-checker | `loop_fix.py`, `app.py`, `tests.py` | Complete |
| [Project 3](./project-3-loop-engineering) | The Morning Brief with a Memory | Scheduled loop + the "Spine" | `schedule.py`, `gather.py`, `progress.md` | Complete |
| [Project 4](./project-4-loop-engineering) | A Fix Loop with a Real Checker | Worktree isolation + skills + maker-checker | `implementer.py`, `reviewer.py`, `.opencode/skills/SKILL.md` | Complete |
| [Project 5](./project-5-loop-engineering) | Codify the Body | Engine vs. loop (stateless orchestration) | `run_fix_loop.sh`, `implementer.py`, `reviewer.py` | Complete (engine demo) |
| [Project 6](./project-6-loop-engineering) | Doorbell Loop | Event-driven loop + connectors | `.github/workflows/opencode.yml`, `.opencode/workflows/review-pr.yml` | Complete (config; needs GitHub to run live) |
| [Project 7](./project-7-loop-engineering) | Break It On Purpose | Cost measurement + observability | `schedule.py`, `measure_cost.py`, `schedule.log` | Complete |
| [Project 8](./project-8-loop-engineering) | Your Own Daily Loop (Capstone) | Full loop: heartbeat + worktree + skill + maker-checker + connector + spine + budget | `run_chore.sh`/`.ps1`, `audit_todos.py`, `review_audit.py`, `update_budget.py` | Complete (capstone) |
| [Project 9](./project-9-loop-engineering) | Rehearse a Routine for Free | One-off runs; transcripts over status colors | `commits_yesterday.py`, `routine-prompt.md`, `transcripts/` | Complete |
| [Project 10](./project-10-loop-engineering) | Secrets Drill | Environment (A2) + secrets (A4) | `fetch_data.py`, `.env`, `.gitignore` | Complete |
| [Project 11](./project-11-loop-engineering) | Build the Two-Routine Gate | API trigger (A3) + human gate (A4) + checklist (A6) | `routine_a_draft.py`, `routine_b_execute.py` | Complete |
| [Project 12](./project-12-loop-engineering) | The Dreaming Loop | Self-improvement via spine + maker-checker + human gate | `dreaming_loop.py`, `analyze_logs.py`, `rules.md`, `fixtures/` | Complete |

---

## Project 1 — A Watch Loop

[Open folder](./project-1-loop-engineering)

### Purpose
Demonstrate the simplest loop of all: **watch for a condition without a human watching the
terminal.** One script does long work in the background while another repeatedly checks for a
result file.

### What it demonstrates
An **in-session monitoring loop** (Concept 4): a polling loop with a defined heartbeat
(`CHECK_INTERVAL = 60` seconds), a success condition, and a safety cap that prevents infinite
looping.

### How it works
`long_task.py` sleeps 90 seconds, then writes `Task successfully complete at <timestamp>` to
`output.txt`. `monitor.py` runs up to 10 checks (one per 60 seconds). Each check looks for
`output.txt` and reads whether it contains the completion marker. It exits `0` on success, `1` on
reaching the safety cap, and handles `Ctrl+C` cleanly.

### Important files
| File | Purpose |
|------|---------|
| `long_task.py` | Simulates a long task (90s sleep), then writes `output.txt` |
| `monitor.py` | Polls for `output.txt` every 60s, checks the marker, exits on success/cap/interrupt |
| `output.txt` | Generated by `long_task.py` when finished (present, shows a real run) |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-1-loop-engineering/
  long_task.py
  monitor.py
  output.txt
  README.md
```

### Step-by-step execution
1. Run `long_task.py` in the background.
2. Run `monitor.py` in the foreground (or a second terminal).
3. Let `monitor.py` poll until it detects the completion marker.
4. Stop cleanly with `Ctrl+C`, or let it exit on success.

### Example commands
```bash
cd project-1-loop-engineering
python long_task.py &     # background (Windows: second terminal instead)
python monitor.py
```

### Expected behavior / output
```
monitor.py: SUCCESS — detected completion!
monitor.py: Output file says: "Task successfully complete at 2026-08-18 03:02:27"
monitor.py: Task is done. Exiting monitor.
```
`output.txt` in the repo already contains a real completion timestamp, proving a prior run.

### Key Loop Engineering concepts
Heartbeat, polling interval, success condition, safety cap (bounded loop), clean interrupt.

### What proves the loop works
The monitor **reports exactly once on success and exits** — it never double-reports and never
loops forever (the 10-check cap guarantees termination).

### Current status
**Complete.** All files present and runnable (Python only, no dependencies).

---

## Project 2 — Make the Test Pass, then Stop

[Open folder](./project-2-loop-engineering)

### Purpose
Demonstrate a **conditional loop** that uses an **external test command's exit code** as the
stopping condition — instead of the agent/loop "deciding" it is done.

### What it demonstrates
- **Concept 5 (Conditional Loop):** the loop runs until `pytest` returns exit code `0`.
- **Concept 11 (Maker-Checker):** the maker edits code; the checker (pytest) is the authority.

### How it works
`loop_fix.py` runs `python -m pytest tests.py -v` repeatedly (up to 6 attempts). If the exit code
is `0`, it prints `ALL TESTS PASSED` and stops. Otherwise it retries, and after 6 failures prints
`CAPPED - tests did not pass in 6 tries`. `tests.py` deliberately fails against the initial
`app.py`, so the loop is exercised.

### Important files
| File | Purpose |
|------|---------|
| `loop_fix.py` | The conditional loop that runs tests until pass or cap |
| `app.py` | Functions under test (currently fixed) |
| `tests.py` | Unit tests for `app.py` (initially intentionally failing) |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-2-loop-engineering/
  app.py
  tests.py
  loop_fix.py
  README.md
  .pytest_cache/          # evidence pytest was run
  __pycache__/            # Python bytecode cache
```

### Step-by-step execution
Run the single entry point; observe attempts, exit codes, and either success or the cap.

### Example commands
```bash
cd project-2-loop-engineering
python loop_fix.py
# or run pytest directly to see failing state:
python -m pytest tests.py -v
```

### Expected behavior / output
On success (stops at the passing attempt):
```
Attempt 1 of 6
Tests FAILED (exit code 1). Retrying...
...
ALL TESTS PASSED
```
On a capped failure:
```
CAPPED - tests did not pass in 6 tries
```

### Key Loop Engineering concepts
Exit code as ground truth, maker-checker separation, cap to prevent runaway retries.

### What proves the loop works
The loop **does not decide success** — it respects the external test runner's exit code, and the
cap prevents an infinite retry loop.

### Current status
**Complete.** `.pytest_cache` and `__pycache__` show the suite has actually been executed. Requires
`pytest` to be installed. Note: `app.py` and `tests.py` currently match, so a fresh run would pass
on attempt 1; the "initially failing" scenario is documented, not force-recreated.

---

## Project 3 — The Morning Brief with a Memory

[Open folder](./project-3-loop-engineering)

### Purpose
Demonstrate a **scheduled loop** that **survives across sessions** by persisting state in a "spine"
file, so it never repeats work it already did.

### What it demonstrates
- **Concept 6 (Unattended Scheduled):** a loop triggered by a timer / cron / Task Scheduler, not
  on-demand.
- **Concept 12 (The Spine):** `progress.md` stores findings between runs; the loop adds **only new**
  findings.

### How it works
`schedule.py` (orchestrator) each run: (1) reads `progress.md` (the spine), (2) runs `gather.py`
to collect fresh data (TODO comments + recently modified files), (3) computes the **set difference**
between newly gathered findings and what is already in the spine, (4) appends only the truly-new
findings, and (5) prints what changed or "No new findings".

### Important files
| File | Role | Purpose |
|------|------|---------|
| `progress.md` | **The Spine** | Persistent memory of all findings across runs |
| `gather.py` | **Worker** | Scans workspace for `# TODO` comments and recently modified files |
| `schedule.py` | **Orchestrator** | Reads spine → runs worker → compares → updates spine |
| `README.md` | Documentation | Project-local walkthrough (preserved) |

### File / folder structure
```
project-3-loop-engineering/
  gather.py
  progress.md
  README.md
  schedule.py
```

### Step-by-step execution
Run `schedule.py` multiple times and observe how the second and third runs add **only new**
findings (the spine prevents duplicates).

### Example commands
```bash
cd project-3-loop-engineering
python schedule.py   # Run 1 — populates the spine
python schedule.py   # Run 2 — no duplication of findings already in progress.md
python schedule.py   # Run 3 — same
```
Scheduling options (from the project README): cron `0 * * * * cd /path/project-3 && python3
schedule.py >> cron.log 2>&1`, or Windows Task Scheduler.

### Expected behavior / output
Run 1 adds findings. Later runs print lines like:
```
>>> No new findings — spine already has everything.
>>> Only updating timestamp.
```
`progress.md` (present in the repo) shows accumulated findings across prior runs: several TODO
lines and "Summary" metadata lines — the proof that the spine has held state between runs.

### Key Loop Engineering concepts
Scheduled/unattended heartbeat, spine (persistent memory), set-difference deduplication,
survival across sessions.

### What proves the loop works
Running the schedule more than once never duplicates a finding already recorded in `progress.md`.

### Current status
**Complete.** All files present. `schedule.py` contains `# TODO: test new finding for Run 2` and
`gather.py` ends with `# TODO: fix this later`, so a fresh `gather.py` run will find and record
those TODOs (expected, given how the worker works).

---

## Project 4 — A Fix Loop with a Real Checker

[Open folder](./project-4-loop-engineering)

### Purpose
Demonstrate the **Maker-Checker fix loop** using isolated workspaces (simulated worktrees), a
**reusable agent skill**, and a **strict code reviewer** that catches even *partial* fixes.

### What it demonstrates
- **Concept 8 (Worktree Isolation):** `good_fix_branch/` and `bad_fix_branch/` hold independent
  fixes so experiments never corrupt the original code.
- **Concept 9 (Skills as Reusable Instructions):** `.opencode/skills/SKILL.md` is an instruction
  document (not code) describing the bug, root cause, fix steps, validation, and constraints.
- **Concept 11 (Maker-Checker Loop):** `implementer.py` drafts the fix; `reviewer.py`
  independently validates it and blocks a PR on failure.

### How it works
`buggy_app.py` contains `divide_safe(a, b)` that raises `ZeroDivisionError` when `b == 0`.
`implementer.py` reads the skill and writes a correct fix to `good_fix_branch/`. `reviewer.py`
loads a branch, runs 6 checks (exact return values, no crash, normal behavior preserved, edge
cases, and a source-inspection check for unrelated changes), and emits **PASS** or **FAIL**. The
`bad_fix_branch` contains a deliberately partial fix (returns `"Error"` instead of
`"Error: division by zero"`) that the strict reviewer catches.

### Important files
| File | Purpose |
|------|---------|
| `buggy_app.py` | Original app with the divide-by-zero bug |
| `.opencode/skills/SKILL.md` | Reusable agent instruction file for the fix |
| `implementer.py` | Maker: reads skill, applies fix, writes `good_fix_branch/` |
| `reviewer.py` | Checker: reviews `good` or `bad` branch, outputs PASS/FAIL |
| `good_fix_branch/buggy_app.py` | The correct fix |
| `bad_fix_branch/buggy_app.py` | The deliberately broken (partial) fix |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-4-loop-engineering/
  buggy_app.py
  implementer.py
  reviewer.py
  README.md
  .opencode/skills/SKILL.md
  good_fix_branch/buggy_app.py
  bad_fix_branch/buggy_app.py
  __pycache__/
```

### Step-by-step execution
1. Run the buggy app to see the failure.
2. Run the implementer to produce the good fix.
3. Run the reviewer on `good`, then on `bad`.

### Example commands
```bash
cd project-4-loop-engineering
python buggy_app.py          # see the ZeroDivisionError
python implementer.py        # generate good_fix_branch/buggy_app.py
python reviewer.py good      # expect PASS
python reviewer.py bad       # expect FAIL (wrong error message)
```

### Expected behavior / output
- `reviewer.py good` → `RESULT: PASS ... PR would be opened`
- `reviewer.py bad` → `RESULT: FAIL ... PR blocked — fix not ready`

### Key Loop Engineering concepts
Maker-checker separation, worktree/branch isolation, skills as reusable instructions, strict,
non-trusting verification.

### What proves the loop works
A **deliberately bad** fix is rejected because the reviewer checks *exact return values*, not just
"did it crash". The maker and checker are independent and the checker never trusts the maker.

### Current status
**Complete.** All source, skill, and both branch directories are present and runnable.

---

## Project 5 — Codify the Body

[Open folder](./project-5-loop-engineering)

### Purpose
Distinguish an **ENGINE** (one-time, stateless orchestration) from a **LOOP** (engine + scheduler +
memory). The project deliberately builds only the engine, then shows what turns it into a loop.

### What it demonstrates
- **Concept 8 (Worktree):** an isolated checkout per candidate.
- **Concept 11 (Maker-Checker):** `implementer.py` drafts a fix; `reviewer.py` grades it.

### How it works
`run_fix_loop.sh` reads candidates from `test_candidates.txt`, and for each candidate runs
`implementer.py` then `reviewer.py` **in parallel** inside isolated `wt-<candidate>/` folders,
collecting PASS/FAIL. Because it reads/writes **no state file**, running it twice yields identical
output — proving it is an *engine*, not a loop. The README explains that adding a **heartbeat**
(scheduler) and a **spine** (state file) converts it into a true loop.

> Note: although the README describes `git worktree add`, the checked-in `run_fix_loop.sh` actually
> creates isolated folders with `mkdir -p wt-<candidate>` and copies the scripts in. Documented
> here as actually implemented.

### Important files
| File | Purpose |
|------|---------|
| `run_fix_loop.sh` | The engine: orchestrates all candidates, parallel, stateless |
| `implementer.py` | Maker — drafts a fix per candidate |
| `reviewer.py` | Checker — grades the fix per candidate |
| `test_candidates.txt` | Candidate list (`candidate-1/2/3: <bug type>`) |
| `wt-candidate-1/2/3/` | Generated isolated checkouts (from prior runs) |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-5-loop-engineering/
  implementer.py
  README.md
  reviewer.py
  run_fix_loop.sh
  test_candidates.txt
  wt-candidate-1/implementer.py, reviewer.py, good_fix_branch/buggy_app.py
  wt-candidate-2/...            (generated)
  wt-candidate-3/...            (generated)
```

### Step-by-step execution
Run the engine twice and observe **identical output** both times — that identity is the proof it
is stateless.

### Example commands
```bash
cd project-5-loop-engineering
bash run_fix_loop.sh   # bash required (Windows: Git Bash / WSL)
```

### Expected behavior / output
Summarizes how many candidates were processed and notes:
```
Status: ENGINE mode (no memory between runs)
Key insight: Running this script again will produce IDENTICAL output.
```
The script currently prints a generic summary (it does not yet fully aggregate per-candidate
PASS/FAIL into a single count), but the engine/loop distinction is the intended lesson.

### Key Loop Engineering concepts
Stateless engine vs. stateful loop; the need for a heartbeat (schedule) and a spine (memory) to
convert an engine into a loop.

### What proves the point
Re-running produces the same output because there is no state between runs.

### Current status
**Complete as an engine demonstration** and intentionally *not* yet a loop (that is the lesson).
`bash` is required (Windows users need Git Bash/WSL). The `wt-candidate-*` directories show the
engine was actually executed.

---

## Project 6 — Doorbell Loop (Event-Driven PR Review)

[Open folder](./project-6-loop-engineering)

### Purpose
Demonstrate an **event-driven loop**: automation that reacts to an external event (a GitHub pull
request) instead of polling on a timer or needing a manual prompt.

### What it demonstrates
- **Concept 7 (Event-Driven Loop):** react when an event fires ("doorbell") rather than "check every
  X".
- **Concept 10 (Connectors):** the GitHub webhook bridges GitHub's PR system to an OpenCode review
  capability.

### How it works
GitHub fires a `pull_request` event (`opened`, `synchronize`) → the GitHub Actions workflow
(`.github/workflows/opencode.yml`) runs OpenCode with a review prompt → OpenCode reviews the code
and comments on the PR. The paired `.opencode/workflows/review-pr.yml` documents the same review
behavior as an OpenCode workflow. `buggy_code.py` contains an intentional off-by-one bug and
`test_buggy_code.py` has tests that fail because of it, so a real review would find it.

### Important files
| File | Purpose |
|------|---------|
| `.github/workflows/opencode.yml` | GitHub Actions workflow, trigger: `pull_request [opened, synchronize]` |
| `.opencode/workflows/review-pr.yml` | OpenCode workflow definition for PR review |
| `buggy_code.py` | Contains the intentional off-by-one bug |
| `test_buggy_code.py` | Tests that fail due to the bug |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-6-loop-engineering/
  buggy_code.py
  README.md
  test_buggy_code.py
  .github/workflows/opencode.yml
  .opencode/workflows/review-pr.yml
```

### Step-by-step execution (live demo requires GitHub)
From the project README: install GitHub integration, init git, create a feature branch with the
buggy code, open a PR, watch the automatic review, then push a fix and watch the re-review on the
`synchronize` event.

### Example commands
```bash
cd project-6-loop-engineering
opencode github install
git init && git checkout -b main && git add . && git commit -m "Project 6 setup"
# ... create feature branch, push, open PR — the workflow fires automatically
```

### Expected behavior / output
On `pull_request.opened` → review finds the bug and comments. On `pull_request.synchronize` →
review re-runs. The re-fire on a second event is what proves the event heartbeat works.

### Key Loop Engineering concepts
Event-driven heartbeat (vs. scheduled), connectors/webhooks, reactive automation, CI/CD review.

### Source-only validation
`buggy_code.py` + `test_buggy_code.py` can be run locally to confirm the planted bug is real:
```bash
cd project-6-loop-engineering
python -m pytest test_buggy_code.py -v   # the off-by-one tests will fail
```

### Current status
**Complete as configuration and source**, but the *live* event-driven loop depends on a GitHub
repository with OpenCode integration (`opencode github install`), which cannot fire offline. The
workflow files and buggy code are all present.

---

## Project 7 — Break It On Purpose

[Open folder](./project-7-loop-engineering)

### Purpose
Build **observability and cost tracking** into a scheduled loop, then deliberately **sabotage** it
to rehearse an overnight failure safely (and cheaply) while you are watching.

### What it demonstrates
- **Concept 13 (Cost Measurement):** estimate tokens and projected monthly cost per beat.
- **Concept 14 (Error Handling & Observability):** every step logged; failures are explicit and
  diagnosable from a log + spine without re-running.

### How it works
`schedule.py` runs one "beat": logs start, reads the spine (`progress.md`), runs `gather.py`
(subprocess, with timeout), compares findings, and updates the spine — logging every step to
`schedule.log`. `measure_cost.py` runs `gather.py` once, estimates tokens (~4 chars/token), and
projects monthly cost at hourly cadence. The README walks through a **sabotage exercise**: point
the spine read at a nonexistent file, re-run, and diagnose the failure from `schedule.log` +
`progress.md` + `diagnostic_report.md` — no replay needed.

### Important files
| File | Purpose |
|------|---------|
| `schedule.py` | Main scheduled loop with logging at every step |
| `gather.py` | Data collection (simulated findings) |
| `measure_cost.py` | Token / monthly cost measurement for one beat |
| `progress.md` | The spine — persistent state between beats |
| `schedule.log` | Full observability log of every action (present, shows real runs) |
| `diagnostic_report.md` | Proof of diagnosis from spine + log alone (present) |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-7-loop-engineering/
  diagnostic_report.md
  gather.py
  measure_cost.py
  progress.md
  README.md
  schedule.log
  schedule.py
```

### Step-by-step execution
1. Measure cost. 2. Run a successful beat. 3. Sabotage `schedule.py` (point the `progress.md` read
at a missing file). 4. Run the failed beat. 5. Diagnose from the log + spine (no replay).
6. Restore and re-run.

### Example commands
```bash
cd project-7-loop-engineering
python measure_cost.py     # ~52 tokens/beat; monthly ≈ $0.11 at hourly cadence
python schedule.py         # SUCCESS beat
# ... sabotage schedule.py ...
python schedule.py         # ERROR: progress.md not found!
# diagnose without replay:
Select-String -Path schedule.log -Pattern "ERROR"   # PowerShell
# or: grep ERROR schedule.log
Get-Content progress.md
```

### Expected behavior / output
`measure_cost.py` prints a one-beat token estimate and a monthly cost projection (roughly
`$0.11/month`). `schedule.log` (present) records error lines and `NEEDS HUMAN` alerts from the
sabotage run, and `diagnostic_report.md` shows the full WHAT / WHEN / WHY diagnosis reconstructed
from log + spine alone.

### Key Loop Engineering concepts
Observability, cost measurement, error handling, three-layer safety (log + spine + alert),
rehearsing failure.

### What proves the loop works
A deliberately introduced failure is **discovered and diagnosed without re-running the script** —
the log and spine together are enough.

### Current status
**Complete.** The sabotage exercise is fully documented and the artifacts (`schedule.log`,
`diagnostic_report.md`, `progress.md`) are present. `gather.py` here is a simplified simulated
finder (checks file/path presence), unlike Project 3's TODO scanner.

---

## Project 8 — Your Own Daily Loop (Capstone)

[Open folder](./project-8-loop-engineering)

### Purpose
The **capstone**: assemble all six parts of loop engineering into one unattended, budget-guarded
TODO-audit loop, then leave it to run on a schedule and stay able to understand and diagnose it.

### What it demonstrates
The **six parts of a complete loop**:
1. **Heartbeat** — scheduled (weekdays 9 AM via cron).
2. **Worktree** — each run works in an isolated `wt-audit-<TIMESTAMP>` workspace.
3. **Skill** — `.opencode/skills/todo-audit.yml` holds reusable audit instructions.
4. **Maker-Checker** — `audit_todos.py` (maker) scans; `review_audit.py` (checker) validates.
5. **Connector** — cron fires the chore script (extensible to a webhook).
6. **Spine** — `audit_progress.md` records every run.

Plus **budget guards** (max tokens/run, monthly cost, runs/week) and **Concept 15 ("Keeping Up")**:
`Loop Speed <= Your Review Speed`.

### How it works
`run_chore.sh` (and `run_chore.ps1` for Windows): reads/initializes the spine, checks budget
guards against `budget_state.json`, creates an isolated worktree (falls back to the main directory
if worktree creation fails), runs the maker (`audit_todos.py`) to scan for TODO/FIXME/HACK/XXX
comments, runs the checker (`review_audit.py`) to validate the result, updates the spine, and
updates the budget state via `update_budget.py`.

### Important files
| File | Role | Purpose |
|------|------|---------|
| `run_chore.sh` / `run_chore.ps1` | Orchestrator | Unix / Windows chore runner (heartbeat + worktree + maker + checker + spine) |
| `audit_todos.py` | **Maker** | Scans Python files for TODO/FIXME/HACK/XXX, writes `audit_findings.json` |
| `review_audit.py` | **Checker** | Validates the audit result (findings limits, critical errors) |
| `update_budget.py` | Budget | Tracks tokens/cost/runs in `budget_state.json` |
| `.opencode/skills/todo-audit.yml` | **Skill** | Reusable audit instructions |
| `audit_progress.md` | **Spine** | Persistent per-run history (present, shows runs) |
| `budget_state.json` | Budget | Current budget usage (present: 2 runs this week, tokens 3000, cost $0.01) |
| `audit_*.log` | Logs | Per-run observability logs (present) |
| `audit_findings.json`, `audit_output.txt` | Output | Audit results from prior runs |
| `sample_module.py`, `test_week.md` | Extras | Sample module and test-week notes |
| `README.md` | Documentation | Project-local walkthrough (preserved) |

### File / folder structure
```
project-8-loop-engineering/
  audit_20260821_*.log
  audit_findings.json
  audit_output.txt
  audit_progress.md
  audit_todos.py
  budget_state.json
  README.md
  review_audit.py
  run_chore.ps1
  run_chore.sh
  sample_module.py
  test_week.md
  update_budget.py
  .opencode/skills/todo-audit.yml
```

### Step-by-step execution
1. Run manually to test. 2. Schedule via cron. 3. Let it run unattended. 4. Review the spine each
morning. 5. If it fails, diagnose from spine + logs. 6. Judge whether to speed up or slow down.

### Example commands
```bash
cd project-8-loop-engineering
bash run_chore.sh                      # Windows: ./run_chore.ps1
# schedule (Unix cron):
0 9 * * 1-5 cd /path/to/project-8 && bash run_chore.sh
# inspect state:
cat audit_progress.md
ls -lt audit_*.log | head -1
```

### Expected behavior / output
Each beat logs `BEAT STARTED → ... → BEAT COMPLETED SUCCESSFULLY` (or explicit errors), appends a
run record to `audit_progress.md`, and updates `budget_state.json`. The present artifacts confirm
prior successful runs (`REVIEW PASSED`, spine `Status: PASSED`). Note: `run_chore.sh` uses `git
worktree add ... main`, which requires the project to be inside a git repo with a `main` branch;
on this checkout the log shows a graceful fallback ("Worktree creation failed, running in main
directory") — the loop still completes.

### Key Loop Engineering concepts
Full loop assembly: heartbeat, worktree, skill, maker-checker, connector, spine, budget guards,
human "keeping up" rate, diagnosing from spine + logs.

### What proves the loop works
The spine (`audit_progress.md`) and per-run logs show multiple completed runs, and `budget_state.json`
confirms the budget guards tracked actual usage without overspend.

### Current status
**Complete (capstone).** Real audit artifacts are present. Requires `bash` (or PowerShell for the
`.ps1` variant) and a git repo for the optional worktree step; the script degrades gracefully when
worktree creation is unavailable.

---

## Project 9 — Rehearse a Routine for Free

[Open folder](./project-9-loop-engineering)

### Purpose
Prove that you should **rehearse a routine with a one-off run** (cheap) before committing it to a
schedule (expensive), and that a routine's **status column is not ground truth** — you must read
the **transcript**.

### What it demonstrates
- **A1 (One-off schedules):** `/schedule once ...` fires exactly one time.
- **A3 (One-off runs / "Run now"):** fire immediately, no schedule.
- **A5 (Reading runs):** a GREEN status only means the agent session ended cleanly, **not** that the
  task succeeded.

### How it works
`commits_yesterday.py` summarizes yesterday's commits into `summary.md` (via `git log --since
yesterday --until today --oneline`). Two one-off runs were fired: RUN 1 (success) and RUN 2 (same
prompt plus reading a nonexistent `notes_archive.txt`). Both runs show **GREEN** in the status
column, but the transcripts reveal RUN 1 truly succeeded while RUN 2 failed at step 2. Full
transcripts are preserved in `transcripts/`.

### Important files
| File | Purpose |
|------|---------|
| `commits_yesterday.py` | Summarizes yesterday's commits into `summary.md` |
| `routine-prompt.md` | The one-off routine prompts (RUN 1 + RUN 2 variants) and how to fire A1/A3 |
| `summary.md` | Output of the successful run (present) |
| `transcripts/run1-success.md` | Full transcript — GREEN + genuinely succeeded |
| `transcripts/run2-failure.md` | Full transcript — GREEN + actually failed |
| `work.txt` | A small placeholder/note file |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-9-loop-engineering/
  commits_yesterday.py
  README.md
  routine-prompt.md
  summary.md
  work.txt
  transcripts/run1-success.md
  transcripts/run2-failure.md
```

### Step-by-step execution
From the project README: init git, create commits dated yesterday, run the script with
`PYTHONUTF8=1` (RUN 1), then fire RUN 2 with the modified prompt that reads a nonexistent file,
and compare the transcripts.

### Example commands
```bash
cd project-9-loop-engineering
git init && git add . && git commit -m "Initial"
# create yesterday-dated commits for testing, then:
$env:PYTHONUTF8="1"; python commits_yesterday.py
cat summary.md
# RUN 2: change the prompt to read notes_archive.txt (nonexistent) and fire again
cat notes_archive.txt   # ERROR — but the session still ends GREEN
```

### Expected behavior / output
- RUN 1 transcript: exit 0, `summary.md` written listing 4 commits → genuinely succeeded.
- RUN 2 transcript: step 1 succeeds, step 2 fails with "Cannot find path ... notes_archive.txt" —
  yet the **status is GREEN**, identical to RUN 1.

### Key Loop Engineering concepts
One-off rehearsal, honest verification, transcript-over-status, hidden pitfalls (UnicodeEncodeError
on Windows `cp1252`, scope-creep in "yesterday", PowerShell exit-code lies).

### What proves the loop lesson
Two runs with **identical GREEN status** but **different outcomes**; only reading the transcripts
reveals which truly succeeded.

### Current status
**Complete.** Both transcripts are preserved and the lesson is fully demonstrated.

---

## Project 10 — Secrets Drill

[Open folder](./project-10-loop-engineering)

### Purpose
Run a deliberate-failure drill proving that **secrets must live in environment variables, not in
gitignored files**, because gitignored files never reach the cloud where scheduled routines run.

### What it demonstrates
- **A2 (The Environment):** environment variables are injected at process launch and accessed via
  `os.getenv()`; they are separate from Git.
- **A4 (Secrets):** credentials/API keys must NEVER be committed and must NOT rely on gitignored
  files in a cloud environment.

### How it works
`fetch_data.py` first tries to read the token from `.env` (the WRONG way in the cloud), then falls
back to `os.getenv('API_TOKEN')` (the RIGHT way). RUN 1 (fresh `git clone`, no `.env`) fails
because gitignored files are absent in a clone. RUN 2 (token moved to environment variables)
succeeds via `os.getenv`.

### Important files
| File | Purpose |
|------|---------|
| `fetch_data.py` | Routine needing a token; reads `.env` then falls back to the environment |
| `test_transcript.md` | Full side-by-side transcript of RUN 0/1/2 and the mechanical reason |
| `.env` | Local placeholder `API_TOKEN` (gitignored — NOT committed) |
| `.gitignore` | Keeps `.env` and Python noise out of Git |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-10-loop-engineering/
  fetch_data.py
  README.md
  test_transcript.md
  .env          # gitignored placeholder token
  .gitignore
```

### Step-by-step execution (rehearse honestly)
Clone the repo to simulate the cloud (a clone has exactly what GitHub has — no `.env`), run the
script (fails), then pass the token via an environment variable (succeeds).

### Example commands
```bash
git clone <this-repo-url> cloud-sim
cd cloud-sim/project-10-loop-engineering
python fetch_data.py                # RUN 1: ".env file not found" → exit 1
# RUN 2:
$env:API_TOKEN="..." ; python fetch_data.py   # PowerShell
# or: API_TOKEN=... python fetch_data.py       # bash
```

### Expected behavior / output
- RUN 1: `✗ .env file not found` → `✗ No token found in environment variables` → `NEEDS HUMAN` → exit 1.
- RUN 2: `✓ Found token in environment` → `✓ SUCCESS` → exit 0.

### Key Loop Engineering concepts
Environment vs. Git, secrets handling, cloud-vs-local behavior, honest rehearsal of failure.

### What proves the lesson
A local run is misleading (`.env` exists locally); a **fresh clone fails**, mechanically proving
that gitignored files do not travel to the cloud.

### Current status
**Complete.** `.env` here contains a dummy test placeholder; `.gitignore` excludes it. There is no
`fetch_data.py` caller requiring a real API (the script is fully self-contained for the demo).

---

## Project 11 — Build the Two-Routine Gate

[Open folder](./project-11-loop-engineering)

### Purpose
Build a **human-gated automation system**: Routine A drafts work and stops; Routine B executes the
draft **only when a human fires it over HTTP**. Nothing runs on a timer.

### What it demonstrates
- **A3 (API Trigger):** an HTTP endpoint (`POST /execute`) starts a routine; no schedule/cron.
- **A4 (Human Gate):** a checkpoint where a person's decision controls whether the next step
  happens (your `curl` command *is* the approval signature).
- **A6 (Checklist Before Production):** a completed pre-flight checklist (secrets, constant-time
  token compare, idempotence, loopback binding, fingerprint logging, no schedules).

### How it works
`routine_a_draft.py` (Routine A) is a one-off manual invoke that writes `draft_pending.json` with
status `PENDING APPROVAL` and prints the exact `curl` command, then exits. `routine_b_execute.py`
(Routine B) is a stdlib HTTP server on `127.0.0.1:8011` that refuses to act unless: (1) a valid
bearer token arrives (constant-time compare → else 401), and (2) the draft status is exactly
`PENDING APPROVAL` (else 404/409). On success it performs the task list, flips the draft to
`EXECUTED` (the gate closes behind itself), and appends a signed entry to `approval_log.md`.

### Important files
| File | Purpose |
|------|---------|
| `routine_a_draft.py` | Drafter — one-off invoke, creates the pending draft |
| `routine_b_execute.py` | Executor — stdlib HTTP server, API-trigger only |
| `draft_pending.json` | Generated by A; consumed and flipped by B (status shows `EXECUTED` from prior test) |
| `approval_log.md` | Human-control evidence; every execution recorded with token fingerprint |
| `.env` | `BEARER_TOKEN` (gitignored placeholder) |
| `.gitignore` | Keeps `.env` out of Git |
| `README.md` | Project-local walkthrough (preserved) |

### File / folder structure
```
project-11-loop-engineering/
  approval_log.md
  draft_pending.json
  README.md
  routine_a_draft.py
  routine_b_execute.py
  .env          # gitignored placeholder bearer token
  .gitignore
```

### Step-by-step execution
1. Ensure `BEARER_TOKEN` is set (in `.env` or environment). 2. Start Routine B (listens and waits
   for a *human*). 3. Run Routine A to mint a pending draft. 4. Fire Routine B yourself via `curl`.
5. Observe the gate: wrong token → 401; correct call → executes; re-fire → 409 (gate already closed).

### Example commands
```bash
cd project-11-loop-engineering
python routine_b_execute.py          # listens on 127.0.0.1:8011, waits for a HUMAN
python routine_a_draft.py            # mints draft_pending.json (PENDING APPROVAL)
curl -X POST http://127.0.0.1:8011/execute \
     -H "Authorization: Bearer <token-from-.env>"
# wrong token → 401; success → executes; repeating → 409
```

### Expected behavior / output
Before any call, Routine B prints `idle... waiting for a HUMAN` and `approval_log.md` is untouched.
A successful call executes tasks, flips the draft to `EXECUTED`, and appends a log entry. `grep -i
schedule *.py` finds nothing — there is no timer anywhere.

### Key Loop Engineering concepts
API trigger (no schedule), human gate, bearer-token auth, idempotence/one-shot execution,
audit logging with fingerprints, pre-production checklist.

### What proves the loop works
No schedule exists in the code; Routine B physically cannot start without a human's HTTP request.
`approval_log.md` (present) records multiple executed approvals with token fingerprints, while the
draft is flipped to `EXECUTED` so it can never double-run.

### Current status
**Complete.** State artifacts (`approval_log.md`, `draft_pending.json`) reflect real past runs. The
README's A6 checklist is mostly complete; remaining items (HTTPS reverse proxy, per-user tokens,
rate limiting, real task execution) are explicitly marked as *before real deployment*.

---

## Project 12 — The Dreaming Loop (Self-Improvement)

[Open folder](./project-12-loop-engineering)

### Purpose
Build a loop that **reflects on its own past failures** and turns a repeated failure into a
**proposed rule change** — while *never deciding on its own* (a human holds the gate).

### What it demonstrates
- **Concept 12 (Spine & Improvement):** `dreaming-state.md` is the loop's memory; it never
  re-proposes the same change.
- **Concept 11 (Maker-Checker):** `analyze_logs.py` is the maker (extracts/counts failures);
  `dreaming_loop.py` is the checker (validates evidence before proposing).
- **Concept 6 (Schedule):** designed to run on a schedule alongside Projects 3 / 8.
- **Part 5 (Human Gate):** proposals become PRs on feature branches; `main` is never written
  directly; changes only merge after human review.

### How it works
`dreaming_loop.py` each beat: (1) reads `dreaming-state.md`, (2) analyses the real logs of
Projects 3 / 8 via `analyze_logs.py`, (3) detects repeated failure types (count ≥ threshold,
default 2), (4) checks novelty against the memory, (5) proposes a rule change as a **feature branch
+ commit + PR** (or saves a diff under `proposals/` if `gh` is absent), (6) updates the memory, and
(7) prints a summary. Every proposal must cite evidence (dates, counts, log lines). With calm logs
it emits `NO_PATTERNS -> NO_PROPOSAL`.

### Important files
| File | Role | Purpose |
|------|------|---------|
| `dreaming_loop.py` | Orchestrator / Checker | Analyses logs, detects repeated failures, proposes rule changes, updates memory |
| `analyze_logs.py` | Maker | Parses Project 7 + Project 8 log dialects, groups/counts failures |
| `dreaming-state.md` | The Spine | Long-term memory (last analysis, patterns, proposals) |
| `rules.md` | Rule set | The 4 current rules (Dependency Audit, Test Coverage, Documentation Freshness, Commit Frequency) the loop may propose changing |
| `fixtures/` | Test data | Calm (RUN 1) and repeated-failure (RUN 2) logs |
| `proposals/` | Human gate | Generated on demand: proposal `.md`/`.diff` for human review |
| `README.md` | Documentation | Project-local walkthrough (preserved) |

> `proposals/` is generated on demand by the loop; it is not pre-populated in this checkout.

### File / folder structure
```
project-12-loop-engineering/
  analyze_logs.py
  dreaming_loop.py
  dreaming-state.md
  README.md
  rules.md
  fixtures/calm_audit.log
  fixtures/calm_schedule.log
  fixtures/repeated_schedule.log
  proposals/            # created at runtime when a proposal is generated
```

### Step-by-step execution
Run `dreaming_loop.py` against the fixture logs: RUN 1 (calm) should propose nothing; RUN 2
(planted repeated failure) should propose a rule change with cited evidence. Inspect the analysis
alone with `analyze_logs.py`.

### Example commands
```bash
cd project-12-loop-engineering
python dreaming_loop.py --logs fixtures/calm_audit.log --logs fixtures/calm_schedule.log
python dreaming_loop.py --logs fixtures/repeated_schedule.log
python analyze_logs.py --json --logs fixtures/repeated_schedule.log
python dreaming_loop.py                    # auto-discovers Project 3 / Project 8 logs
```

### Expected behavior / output
- RUN 1 (calm): `Total failures found: 0` ... `NO_PATTERNS -> NO_PROPOSAL`.
- RUN 2 (planted): `Total failures found: 6`, two repeated types (`FAILURE: 3x`, `NEEDS HUMAN: 3x`),
  and `PROPOSAL MADE (as PR): [R2-TEST] Strengthen Test Coverage after 3x repeated 'FAILURE' failures`.

### Key Loop Engineering concepts
Self-improvement, spine/novelty (never re-proposing), maker-checker evidence validation, scheduled
reflection, human gate (propose, don't decide), evidence tracing.

### What proves the loop works
With calm logs it proposes nothing; with a planted repeated failure it produces a proposal **with
citations to real dates, counts, and log lines**, and records what it has seen so it never proposes
the same change again.

### Current status
**Complete.** The maker/checker/orchestrator, the four rules, the memory spine, and the test
fixtures are all present. The project is Python 3 stdlib-only with no external dependencies. `gh`
must be installed and authenticated to auto-open PRs; without it the proposal is saved under
`proposals/` for a human.

---

## Learning Progression

Each project builds on the previous one. The progression (based only on what is in the repo):

```
Project 1  →  The most basic loop: poll for a file with a heartbeat and a safety cap.
   ↓          (Monitoring)
Project 2  →  Loop until an external source of truth (test exit code) says pass.
   ↓          (Conditional loop + maker-checker)
Project 3  →  Make the loop survive across sessions with a persistent "spine".
   ↓          (Scheduled loop + persistent memory)
Project 4  →  Split the fix work into maker + strict checker, isolated in worktrees,
   ↓          driven by reusable skills.
Project 5  →  Prove the difference between a stateless ENGINE and a stateful LOOP.
   ↓          (Engine = orchestration; Loop = engine + heartbeat + memory)
Project 6  →  Trigger the loop from an external EVENT instead of a timer.
   ↓          (Event-driven heartbeat + connectors)
Project 7  →  Make the loop observable and measure its cost; rehearse failure safely.
   ↓          (Observability + cost + error handling)
Project 8  →  Assemble everything into one unattended, budget-guarded daily loop.
   ↓          (Capstone: heartbeat + worktree + skill + maker-checker + connector + spine)
Project 9  →  Verify honestly: rehearse with one-off runs and READ THE TRANSCRIPTS.
   ↓          (Transcript-over-status)
Project 10 →  Handle secrets and environments so the loop survives in the cloud.
   ↓          (Secrets + environment variables)
Project 11 →  Add a human gate and an API trigger: automation that can't run without
   ↓          an explicit human decision.
Project 12 →  Let the loop reflect on its own past failures and PROPOSE improvements.
              (Self-improvement + human gate — propose, don't decide)
```

From "watch a file" (P1) → "verify with tests" (P2) → "remember between runs" (P3) → "isolate and
review fixes" (P4) → "understand what makes it a loop" (P5) → "react to events" (P6) → "see inside
and meter cost" (P7) → "combine it all" (P8) → "verify honestly" (P9) → "handle secrets" (P10) →
"restrain it with a human gate" (P11) → "let it self-improve safely" (P12).

---

## Architecture / Loop Pattern

Across the projects a common loop shape recurs. Expressed in the spirit of
`Observe → Decide → Act → Verify → Record → Repeat`, and grounded only in what the projects
actually implement:

```
[Observe]   Wake up — via a heartbeat (In-session poll   —— P1
                                Conditional test pass    —— P2
                                Schedule / timer         —— P3, P7, P8, P12
                                External event           —— P6
                                Human / API trigger      —— P11)
                ↓
[Read spine] Read persistent memory of what is already known / done
                (progress.md        —— P3, P7
                 audit_progress.md   —— P8
                 dreaming-state.md   —— P12)
                ↓
[Decide / Act] Do bounded work, often split Maker vs. Checker
                (implementer.py / reviewer.py         —— P4, P5
                 audit_todos.py / review_audit.py      —— P8
                 analyze_logs.py / dreaming_loop.py    —— P12)
                ↓
[Verify]      Check the result against an independent authority
                (test exit code  —— P2
                 strict reviewer —— P4, P8
                 evidence check —— P12)
                ↓
[Record]      Persist the outcome to a spine + a log for later diagnosis
                (progress.md / schedule.log      —— P7
                 audit_progress.md / audit_*.log  —— P8
                 approval_log.md                  —— P11
                 dreaming-state.md                —— P12)
                ↓
[Repeat / Gate] Stop on success or cap (P1, P2), or hand decisions to a human
                (P9 honesty, P10 secrets, P11 human gate, P12 propose-not-decide)
```

Not every step appears in every project — for example, Projects 1–2 are stateless (no spine), and
the event-driven/API-trigger loops replace the "schedule" observe step. The pattern is meant to be
read as the *common skeleton* the series builds toward, made explicit in Project 8 (capstone) and
Project 12 (self-improvement).

---

## How to Run All Projects

### Prerequisites
- **Python 3** on `PATH` (`python` / `python3`).
- **`pytest`** — required by Project 2 (`pip install pytest`).
- **Bash** — required by Projects 5 and 8 (Windows: use Git Bash or WSL), or use `run_chore.ps1`
  for Project 8 on Windows PowerShell.
- **`git`** — required by Projects 5, 8, 9, and 12 (for worktrees, commit summaries, and proposing
  changes).
- **`gh` (GitHub CLI)** — optional, used by Project 12 to open PRs; without it the proposal is
  saved as a diff.
- **GitHub + OpenCode integration** — required for the *live* event-driven demo in Project 6
  (`opencode github install`).
- **Network/HTTP** — used only by Project 11 (a local HTTP server on `127.0.0.1:8011`).

### Installation / Setup
Projects 1, 3, 4, 6, 7, 9, 10, 11, 12 use the Python standard library only — no installation
required beyond Python. For a full local run:

```bash
pip install pytest        # Project 2 only
```

For Projects 10/11, create a local `.env` with your own placeholder values (they are gitignored):
- Project 10: `API_TOKEN=<your-token>`
- Project 11: `BEARER_TOKEN=<your-token>`

### Per-Project Commands

**Project 1 — A Watch Loop**
```bash
cd project-1-loop-engineering
python long_task.py &      # Windows: run in a second terminal instead of &
python monitor.py
```

**Project 2 — Make the Test Pass, then Stop**
```bash
cd project-2-loop-engineering
python loop_fix.py
```

**Project 3 — The Morning Brief with a Memory**
```bash
cd project-3-loop-engineering
python schedule.py    # run several times to see the spine prevent duplication
```

**Project 4 — A Fix Loop with a Real Checker**
```bash
cd project-4-loop-engineering
python buggy_app.py        # see the bug
python implementer.py      # generate the good fix
python reviewer.py good    # PASS
python reviewer.py bad     # FAIL
```

**Project 5 — Codify the Body**
```bash
cd project-5-loop-engineering
bash run_fix_loop.sh       # run twice to observe identical (stateless) output
```

**Project 6 — Doorbell Loop (Event-Driven PR Review)**
```bash
cd project-6-loop-engineering
opencode github install        # requires GitHub integration
# then init/push a feature branch and open a PR — the workflow fires on PR events
python -m pytest test_buggy_code.py -v   # offline sanity check of the planted bug
```

**Project 7 — Break It On Purpose**
```bash
cd project-7-loop-engineering
python measure_cost.py
python schedule.py
# ... optionally sabotage schedule.py (see project README) ...
grep ERROR schedule.log       # or: Select-String -Path schedule.log -Pattern "ERROR"
```

**Project 8 — Your Own Daily Loop (Capstone)**
```bash
cd project-8-loop-engineering
bash run_chore.sh             # Windows: ./run_chore.ps1
cat audit_progress.md
ls -lt audit_*.log | head -1
```

**Project 9 — Rehearse a Routine for Free**
```bash
cd project-9-loop-engineering
git init && git add . && git commit -m "Initial"
# create yesterday-dated commits, then:
$env:PYTHONUTF8="1"; python commits_yesterday.py
cat summary.md
# RUN 2: fire the prompt variant that reads notes_archive.txt (nonexistent) — compare transcripts
```

**Project 10 — Secrets Drill**
```bash
git clone <this-repo-url> cloud-sim
cd cloud-sim/project-10-loop-engineering
python fetch_data.py                        # RUN 1: fails (no .env in clone)
$env:API_TOKEN="..." ; python fetch_data.py # RUN 2: succeeds via environment
```

**Project 11 — Build the Two-Routine Gate**
```bash
cd project-11-loop-engineering
python routine_b_execute.py                 # terminal 1: listens, waits for a human
python routine_a_draft.py                   # terminal 2: mints the pending draft
curl -X POST http://127.0.0.1:8011/execute \
     -H "Authorization: Bearer <token-from-.env>"
```

**Project 12 — The Dreaming Loop (Self-Improvement)**
```bash
cd project-12-loop-engineering
python dreaming_loop.py --logs fixtures/calm_audit.log --logs fixtures/calm_schedule.log
python dreaming_loop.py --logs fixtures/repeated_schedule.log
python analyze_logs.py --json --logs fixtures/repeated_schedule.log
```

---

## Project Comparison

| Project | Automation | Monitoring | Scheduling | Feedback | Persistence | Verification | Agent involvement | Fix/Retry behavior |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1 — A Watch Loop** | Yes | Yes | No (in-session) | Yes (file marker) | No | Yes (checks marker) | No | No (monitors only) |
| **2 — Test Pass, Stop** | Yes | Partial (loop state) | No | Yes (test exit code) | No | Yes (pytest) | Yes (maker/checker roles) | Yes (retries up to 6) |
| **3 — Morning Brief** | Yes | Yes (finds TODOs/files) | Yes (cron/Task Scheduler) | Partial (dedup diff) | Yes (progress.md spine) | Partial (set comparison) | No (plain scripts) | No |
| **4 — Fix Loop w/ Checker** | Yes | No | No | Yes (reviewer PASS/FAIL) | Partial (branch isolation) | Yes (6 strict checks) | Yes (implementer/reviewer) | Yes (redo until PASS) |
| **5 — Codify the Body** | Yes | No | No (engine only) | Yes (per-candidate PASS/FAIL) | No (deliberately stateless) | Yes (reviewer) | Yes (implementer/reviewer) | No (engine processes once) |
| **6 — Doorbell Loop** | Yes | No | No (event-driven) | Yes (GH Actions on PR event) | Partial (in GitHub) | Yes (review prompt) | Yes (OpenCode review) | Partial (re-reviews on synchronize) |
| **7 — Break It On Purpose** | Yes | Yes (logs/spine) | Yes (scheduled) | Yes (error signals) | Yes (progress.md + schedule.log) | Yes (logged status) | No | No (surfaces for human) |
| **8 — Daily Loop (Capstone)** | Yes | Yes | Yes (weekday cron) | Yes (maker/checker) | Yes (audit_progress.md, budget_state) | Yes (review_audit.py) | Yes (maker/checker + skill) | Partial (fails closed, budget guards) |
| **9 — Rehearse a Routine** | Yes | Yes (transcripts) | No (one-off only) | Yes (transcript review) | Partial (summary.md) | Yes (read transcript) | Yes (one-off agent runs) | No (rehearse, then fix) |
| **10 — Secrets Drill** | Yes | Partial (outcome shown) | No (run on demand) | Yes (exit code/status) | No | Yes (checks token found) | Yes (routine) | No |
| **11 — Two-Routine Gate** | Yes | Yes (approval_log.md) | No (API trigger only) | Yes (HTTP status codes) | Yes (draft_pending.json, approval_log) | Yes (gate checks token + status) | Yes (two routines) | Partial (409 blocks replay) |
| **12 — Dreaming Loop** | Yes | Yes (reads logs) | Yes (scheduled) | Yes (detects repeated failures) | Yes (dreaming-state.md) | Yes (evidence check) | Yes (maker/checker) | Yes (proposes changes as PRs) |

Legend: **Automation** = does work without a human; **Monitoring** = observes its own state or
external state; **Scheduling** = runs on a timer/cron; **Feedback** = uses a signal to adjust;
**Persistence** = remembers state across runs; **Verification** = independently checks the result;
**Agent involvement** = an agent/maker/checker role is present; **Fix/Retry** = changes behavior
in response to failure.

---

## Key Lessons

1. **A loop needs a heartbeat and a stopping condition.** Every loop wakes up somehow (in-session
   poll, test result, timer, event, human/API call) and must terminate — via success, a safety cap,
   or a gate. Projects 1–2 make this explicit with their caps.
2. **Do not be the judge of your own work.** Use an external authority — a test runner's exit code
   (P2), a strict independent reviewer (P4, P8), or verified evidence (P12). A checker that trusts
   the maker is useless; a partially-correct fix must be caught.
3. **Memory (a "spine") is what turns a script into a loop.** Without saved state, re-running
   repeats work (P3, P5). The spine also enables *diagnosis without replay* (P7) and *never
   re-proposing the same improvement* (P12).
4. **Know the difference between an engine and a loop.** An engine is stateless one-time
   orchestration; a loop is an engine plus a heartbeat plus memory (P5).
5. **Different triggers, same loop.** The same loop can be triggered by a timer (P3), an external
   event (P6), or an explicit human/API call (P11). Choose the right heartbeat for the job.
6. **Make it observable and meter its cost.** Log every step, keep a spine, and watch the budget
   (P7, P8). The "overnight failure" is only catastrophic if you can't see inside the loop.
7. **Status columns and exit codes lie.** A GREEN status only means the session ended cleanly — you
   must read the transcript to know whether the task actually succeeded (P9).
8. **Secrets never ride with Git.** Gitignored files never reach the cloud; use environment
   variables instead (P10).
9. **Keep a human in control.** Automation works best when it *proposes* and a human *decides* —
   via gate checklists (P11) and propose-not-decide self-improvement (P12). "Loop speed must be ≤
   your review speed" (P8).
10. **Rehearse failure cheaply while you are watching.** One-off runs and deliberate sabotage let
    you learn how a loop breaks for minutes of cost instead of days (P7, P9).

---

## Final Summary

After completing all 12 projects, a developer should understand that a genuinely useful automation
"loop" is more than a script that repeats — it is a bounded, observable, verifiable, stateful
system with the right trigger and a clear safety boundary. Concretely, you will know how to:

- Build a monitoring poll and a conditional fix loop (P1–P2).
- Make a loop persistent across sessions with a memory spine and schedule it (P3).
- Isolate work in worktrees and drive agents with reusable skills, checked by a strict,
  non-trusting reviewer (P4–P5).
- Trigger loops from external events via connectors (P6).
- Instrument a loop so failures are diagnosable without replay, and meter its cost (P7).
- Combine all six parts of loop engineering into one unattended, budget-guarded daily loop (P8).
- Verify work honestly by reading transcripts rather than trusting status columns (P9).
- Handle secrets and environments so loops survive outside your machine (P10).
- Add human gates and explicit API triggers so automation stays under human control (P11).
- Finally, build a loop that reflects on its own past failures and *proposes* — but never decides —
  its own improvements, keeping a human in charge at every branch (P12).

The series moves from "watch a file" to "a system that improves its own rules," but the golden
thread throughout is: **automate the work, verify independently, remember the state, observe the
cost, and let a human keep the final say.**

---

*This top-level README aggregates Projects 1–12. The authoritative, project-specific detail for
each folder lives in each project's own `README.md`, which is preserved and unchanged.*
