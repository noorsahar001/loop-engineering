# Project 9: Rehearse a routine for free 

## What is a One-Off Routine?

A routine that fires ONCE, not repeated.
- Not scheduled (no heartbeat)
- Manual trigger (Run now / `/schedule once`)
- Used to test prompts before committing to a schedule

## A1: One-Off Schedules

Instead of:

```
/schedule every day at 9am, do X        # repeats forever
```

Do this first:

```
/schedule once tomorrow at 9am, do X    # fires exactly one time
```

If it fails tomorrow, you lost one run — not 30.

## A3: One-Off Runs

"Run now" fires the routine immediately, no schedule at all.
This project used A3 for both test firings.

## A5: Reading Runs

The status column only tells you whether the agent session ended
without crashing. The transcript tells you what actually happened.

## The Two Runs (full transcripts in `transcripts/`)

### RUN 1 — Success Case

Prompt: run `commits_yesterday.py`, verify summary.md.

```
Status:     GREEN ✓
Transcript: Found 4 commits
            ✓ Summary written to summary.md
            → Task SUCCEEDED
```

### RUN 2 — Failure Case

Prompt changed to also read `notes_archive.txt` (does not exist).

```
Status:     GREEN ✓   ← SAME as Run 1!
Transcript: Found 4 commits
            Get-Content: Cannot find path '...\notes_archive.txt'
            because it does not exist.
            → Task FAILED
```

Both runs are GREEN. One succeeded, one failed.
The status column could not tell them apart.

## The A5 Lesson in one sentence

> **Green status means the OpenCode session ended without crashing,
> not that the task succeeded — you must read the transcript to know
> if work actually completed.**

Why both were green: the agent completed its *session* — it ran
commands, saw output, and reported results — even when the result it
reported was an error. Infrastructure health ≠ task success.

## Bonus lessons from reading these transcripts

Reading the full transcripts surfaced three things no status column showed:

1. **A hidden crash:** the first firing of RUN 1 died with
   `UnicodeEncodeError` (cp1252 console can't print `✓`). Exit code 1.
   Diagnosed from the transcript alone; re-run with `PYTHONUTF8=1`.
2. **Scope creep:** "yesterday's commits" actually included a commit
   made TODAY (`git log --until today` resolves to now). Only visible
   in transcript output.
3. **Exit codes lie too:** PowerShell returned exit 0 after the
   file-not-found error in RUN 2 (non-terminating error). Neither the
   status column nor exit codes are ground truth. The transcript is.

## Why Test Before Scheduling?

Cheap to fail once, expensive to fail daily:
- One-off failure: minutes of cost, caught immediately
- Scheduled failure: silently wrong output every morning until someone reads closely

Test loop:
```
write prompt → fire once → READ TRANSCRIPT → fix → fire once → ... → then schedule
```

## Files

| File | Purpose |
|---|---|
| `commits_yesterday.py` | The task: summarize yesterday's commits into summary.md |
| `routine-prompt.md` | The one-off routine prompts (RUN 1 + RUN 2 variants) |
| `summary.md` | Output produced by the successful run |
| `transcripts/run1-success.md` | Full transcript, GREEN + genuinely succeeded |
| `transcripts/run2-failure.md` | Full transcript, GREEN + actually failed |

## Reproduce

```bash
cd project-9-loop-engineering
git init && git add . && git commit -m "Initial"

# Make commits dated yesterday (for testing):
$env:GIT_AUTHOR_DATE="2026-08-23T10:15:00"; $env:GIT_COMMITTER_DATE="2026-08-23T10:15:00"
git commit --allow-empty -m "Add feature A"

# RUN 1 (success):
$env:PYTHONUTF8="1"; python commits_yesterday.py
cat summary.md

# RUN 2 (failure): change prompt to read notes_archive.txt, fire again
cat notes_archive.txt   # ERROR — but session still ends green
```

## Checklist

- [x] Created one-off routine (not scheduled) — `routine-prompt.md`
- [x] RUN 1 fired with A3 (Run now)
- [x] RUN 1 transcript shows success (summary.md created)
- [x] RUN 1 status: GREEN
- [x] RUN 2 prompt changed to read nonexistent file
- [x] RUN 2 fired again with A3 (Run now)
- [x] RUN 2 transcript shows failure (file not found, ERROR)
- [x] RUN 2 status: GREEN (same as Run 1!)
- [x] Can say in ONE SENTENCE why status didn't differ
- [x] README explains A1, A3, A5 and the lesson
- [x] Status column is not ground truth
- [x] Always read transcript before trusting a routine
