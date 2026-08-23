# RUN 1 Transcript — SUCCESS

- Fired: one-off (A3 "Run now"), 2026-08-24
- Prompt: routine-prompt.md → "RUN 1 prompt (success case)"
- STATUS COLUMN: **GREEN ✓**

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

$ Get-Content summary.md
# Yesterday's Summary

Date: 2026-08-24

## Commits (4 total)

- b6c0f0d Update docs
- 9047a0d Fix bug in feature B
- 3e46f86 Add feature A
- 4cc799d Initial: script and routine prompt
```

## What the transcript revealed (status column could not)

1. Task genuinely succeeded: exit 0, summary.md exists and lists commits.
2. It found **4** commits, not 3 — "Initial" was committed TODAY at 03:57,
   but `git log --until today` resolves to *now*, so it leaked in.
   Only by reading the transcript do you know "yesterday's summary"
   actually contains a commit from this morning.
3. First firing attempt CRASHED: Windows cp1252 console threw
   `UnicodeEncodeError` printing the ✓ character (exit code 1).
   Diagnosed purely from that transcript, fixed by re-running with
   PYTHONUTF8=1 — script untouched. The crash never appeared in any
   "success" claim; only the transcript showed it.
