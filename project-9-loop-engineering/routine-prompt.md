# One-Off Routine: summarize-yesterday

Not scheduled. No heartbeat. Fired manually, once per test (A1/A3).

## How to fire it

- **A3 (Run now):** paste the prompt below into OpenCode and run immediately
- **A1 (once):** `/schedule once tomorrow at 9am, <prompt>` — fires a single time, never repeats

## RUN 1 prompt (success case)

```
In this directory, run `python commits_yesterday.py`.
Then read summary.md to verify the commits are listed.
Report exactly what you did and what the output was.
Do not fix anything if it fails — just report honestly.
```

## RUN 2 prompt (failure case)

```
In this directory, run `python commits_yesterday.py`.
Then read notes_archive.txt and append its contents to summary.md.
Report exactly what you did and what the output was.
Do not fix anything if it fails — just report honestly.
```

notes_archive.txt does not exist. The agent will hit an error,
report failure in plain text, and end its session cleanly.
The session status will still be GREEN.
