# Failure Diagnosis (from spine + log only)

## Symptoms
- Last successful beat: 2026-08-21 00:18:00
- First failed beat: 2026-08-21 00:18:31
- Duration: 31 seconds between success and failure

## Root Cause (from log line)
"FAILURE: progress.md not found!"
-> The script tried to open 'nonexistent_file.md' instead of 'progress.md'
-> This was deliberate sabotage (Option A: point at missing file)

## Evidence
- schedule.log line 20: "ERROR - FAILURE: progress.md not found!"
- schedule.log line 21: "ERROR - NEEDS HUMAN: Check if progress.md was deleted or missing"
- progress.md still shows last SUCCESS at 2026-08-21 00:18:00 (was not updated because script crashed before write)

## What Would Human Do
1. Check schedule.log for the error message
2. See "progress.md not found!" - tells you exactly what failed
3. See "NEEDS HUMAN" - tells you it requires manual intervention
4. Check if progress.md exists: `ls progress.md` -> it does exist
5. Check schedule.py for the bug: find line that opens wrong filename
6. Fix the filename in schedule.py
7. Re-run schedule.py

## How Loop Can Self-Heal
- Add: Auto-create progress.md if missing (wrap open() with fallback)
- Add: Backup spine to second location (progress.md.bak)
- Add: Alert channel (Slack/email) on NEEDS HUMAN errors
- Add: Retry logic with exponential backoff before declaring failure
- Add: Health check that verifies all expected files before beat starts

## Key Lesson
Without replaying the script, you can diagnose:
- WHAT failed: progress.md not found (from log line 20)
- WHEN it failed: 2026-08-21 00:18:31 (from log timestamp)
- WHY it failed: Wrong filename in schedule.py (from log error message)
- What needs fixing: Human edits schedule.py to correct filename

The spine + log pair gives you everything needed to diagnose overnight failures
without re-running anything.
