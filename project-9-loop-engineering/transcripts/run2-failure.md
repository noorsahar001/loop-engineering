# RUN 2 Transcript — FAILURE

- Fired: one-off (A3 "Run now"), 2026-08-24
- Prompt: routine-prompt.md → "RUN 2 prompt (failure case)" — reads nonexistent notes_archive.txt
- STATUS COLUMN: **GREEN ✓** (identical to RUN 1!)

## Full transcript

```
$ python commits_yesterday.py
Found 4 commits from yesterday:
  - b6c0f0d Update docs
  - 9047a0d Fix bug in feature B
  - 3e46f86 Add feature A
  - 4cc799d Initial: script and routine prompt

✓ Summary written to summary.md

---EXIT CODE: 0---

---STEP 2: read notes_archive.txt---
Get-Content: Cannot find path '...\project-9-loop-engineering\notes_archive.txt'
because it does not exist.
---EXIT CODE: 0---
```

## What the transcript revealed

- The prompt had TWO steps. Step 1 succeeded; step 2 FAILED with
  "Cannot find path ... notes_archive.txt".
- The agent reported the error honestly and ended its session normally.
- No crash, no exception in the agent infrastructure → the run shows
  **GREEN**, exactly like RUN 1.
- summary.md was NOT updated with any archived notes — the deliverable
  is incomplete even though the status says green.

## Side observation

PowerShell returned exit code 0 even after the error (native error,
non-terminating). If a naive loop checked only exit codes here, it would
call this a success too. Transcripts beat exit codes AND status columns.
