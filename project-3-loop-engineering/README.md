# Project 3: The Morning Brief with a Memory


**Concepts demonstrated:** Concept 6 (unattended Scheduled) + Concept 12 (The Spine)

---

## Concept 6: Unattended Scheduled

A scheduled loop runs on a **timer** — not constantly, not on-demand, but on a fixed schedule.

| Concept | Trigger | Duration | Persistence |
|---------|---------|----------|-------------|
| **Concept 4** — In-session, one-shot | Called once | Runs and dies | None |
| **Concept 5** — Conditional, tests decide | Tests trigger next step | Runs as long as tests pass | In-session only |
| **Concept 6** — Scheduled loop | Timer / cron / Task Scheduler | Runs periodically | **Spine persists between runs** |

Concept 6 is the only one that **survives across sessions**. The loop can be triggered by:
- **Linux/macOS:** A cron job (`*/60 * * * * python3 schedule.py`)
- **Windows:** Task Scheduler (runs `python schedule.py` every hour)
- **Manual:** Just run `python schedule.py` whenever you want

---

## Concept 12: The Spine

The spine is **persistent memory** — a file (`progress.md`) that stores what the loop has already found.

**Without a spine:**
- Run 1: Finds items A, B, C
- Run 2: Finds items A, B, C, D → adds A, B, C again (DUPLICATE)
- Run 3: Finds items A, B, C, D, E → adds A, B, C, D again (DUPLICATE)

**With a spine:**
- Run 1: Finds items A, B, C → stores in progress.md
- Run 2: Finds items A, B, C, D → reads spine, sees A,B,C already known, adds ONLY D
- Run 3: Finds items A, B, C, D, E → reads spine, sees A,B,C,D already known, adds ONLY E

**progress.md IS the spine.** It holds state between runs so the loop never repeats work.

---

## How It Works

```
schedule.py (orchestrator)
  │
  ├── 1. READ progress.md (the spine) → what do we already know?
  │
  ├── 2. RUN gather.py → scan workspace for TODOs, recent files
  │
  ├── 3. COMPARE new findings vs existing findings
  │       - Old findings: already in progress.md
  │       - New findings: not yet in progress.md
  │
  ├── 4. UPDATE progress.md → add only new findings, update timestamp
  │
  └── 5. PRINT summary → what changed (or "No new findings")
```

### The Comparison Logic

The spine works because `schedule.py` compares **exact strings**:

1. It reads all `- ` lines from progress.md's `## Findings` section
2. It collects all `- ` lines from gather.py's output
3. It computes: `truly_new = gathered - existing`
4. Only `truly_new` lines get added to progress.md

This is a simple set difference — no AI, no heuristics, just exact matching.

---

## Files

| File | Role | Description |
|------|------|-------------|
| `progress.md` | **The Spine** | Persistent memory — stores all findings across runs |
| `gather.py` | **Worker** | Scans workspace for TODO comments and recently modified files |
| `schedule.py` | **Orchestrator** | Reads spine → runs worker → compares → updates spine |
| `README.md` | **Documentation** | This file |

---

## How to Run

### Manual testing (recommended for learning):

```bash
# Run 1 — first execution, spine is empty
python schedule.py

# Run 2 — spine has findings from Run 1
python schedule.py

# Run 3 — spine has findings from Run 1 + Run 2
python schedule.py
```

### Automated scheduling (Linux/macOS cron):

```bash
# Edit crontab
crontab -e

# Add this line — runs every hour
0 * * * * cd /path/to/project-3-loop-engineering && python3 schedule.py >> cron.log 2>&1
```

### Automated scheduling (Windows Task Scheduler):

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 1 hour
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\project-3-loop-engineering\schedule.py`

---

## Example: Run 1 vs Run 2

### Run 1 Output:
```
=== Schedule Run: 2026-08-19 03:45:00 ===
Last run: None
Existing findings in spine: 0

[Gathering new data...]
Gathered 2 finding(s):
  - TODO in project-1/long_task.py:4 — # TODO: add error handling
  - Modified: gather.py, schedule.py, progress.md

>>> 2 NEW finding(s) added to progress.md:
  + TODO in project-1/long_task.py:4 — # TODO: add error handling
  + Modified: gather.py, schedule.py, progress.md

Spine updated. Next run will build on 2 finding(s).
```

### Run 2 Output (nothing new happened):
```
=== Schedule Run: 2026-08-19 04:45:00 ===
Last run: 2026-08-19 03:45:00
Existing findings in spine: 2

[Gathering new data...]
Gathered 2 finding(s):
  - TODO in project-1/long_task.py:4 — # TODO: add error handling
  - Modified: gather.py, schedule.py, progress.md

>>> No new findings — spine already has everything.
>>> Only updating timestamp.

Spine updated. Next run will build on 2 finding(s).
```

### Run 2 Output (new TODO added):
```
=== Schedule Run: 2026-08-19 05:45:00 ===
Last run: 2026-08-19 04:45:00
Existing findings in spine: 2

[Gathering new data...]
Gathered 3 finding(s):
  - TODO in project-1/long_task.py:4 — # TODO: add error handling
  - TODO in project-2/tests.py:12 — # TODO: fix failing test
  - Modified: gather.py, schedule.py, progress.md

>>> 1 NEW finding(s) added to progress.md:
  + TODO in project-2/tests.py:12 — # TODO: fix failing test

Spine updated. Next run will build on 3 finding(s).
```

**The second run did NOT repeat the first run's findings.** This proves the spine works.

---

## Success Criteria

- [x] `progress.md` exists and is the spine (holds state between runs)
- [x] `gather.py` collects simple data (TODOs + recently modified files)
- [x] `schedule.py` reads progress.md, gathers new data, compares, updates only with NEW findings
- [x] Run 1 populates progress.md with initial findings + timestamp
- [x] Run 2 recognizes old findings, adds ONLY new findings
- [x] Run 2 does NOT repeat Run 1's findings (spine works)
- [x] README.md explains Concept 6 vs 4 vs 5 and why the spine prevents duplication
