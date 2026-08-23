# Project 7: Break it own Purpose

## Overview

This project teaches you to build observability and cost tracking into your loop,
then sabotage it to rehearse overnight failures safely.

**Concepts covered:**
- Concept 13: Cost Measurement
- Concept 14: Error Handling & Observability

## What You'll Learn

- **Observability**: You can see inside the loop at every step
- **Cost (Concept 13)**: Knowing your monthly bill before it surprises you
- **Error Handling (Concept 14)**: Clear error messages, not silent failures
- **Rehearsing failure**: Cheap when YOU are watching, catastrophic at 3 AM
- **Spine + log**: Enough to diagnose without replaying the full run

## Files

| File | Purpose |
|------|---------|
| `schedule.py` | Main loop with logging at every step |
| `gather.py` | Data collection (simulated findings) |
| `progress.md` | The spine - persistent state between beats |
| `schedule.log` | Full observability log of every action |
| `measure_cost.py` | Token cost measurement for one beat |
| `diagnostic_report.md` | Proof of diagnosis without replay |

## Cost Measurement (Concept 13)

Run `python measure_cost.py` to see:

```
One beat (gather.py run) produces:
  Output length: 211 chars -> ~52 tokens
  Total estimated tokens: ~52

Monthly Cost Projection (24 beats/day):
  TOTAL: $0.1123/month
```

At 24 runs/day (hourly), this loop costs approximately **$0.11/month**.

## How to Run

### Step 1: Measure cost
```bash
python measure_cost.py
# Output: One beat: ~52 tokens, Monthly cost: $0.11
```

### Step 2: Successful beat (RUN 1)
```bash
python schedule.py
# Output: SUCCESS
# progress.md updated with timestamp and findings
# schedule.log shows all steps completed
```

### Step 3: Sabotage it
Edit `schedule.py` line 19:
```python
# Change:
with open('progress.md') as f:
# To:
with open('nonexistent_file.md') as f:  # SABOTAGE
```

### Step 4: Failed beat (RUN 2)
```bash
python schedule.py
# Output: ERROR: progress.md not found!
# schedule.log shows where it failed
```

### Step 5: Diagnose (no replay)
```bash
# Check log without re-running
Select-String -Path schedule.log -Pattern "ERROR"
# Output: "ERROR - FAILURE: progress.md not found!"

# Check spine
Get-Content progress.md
# Output: Last beat shows SUCCESS at 2026-08-21 00:18:00
```

### Step 6: Restore and re-run
Fix `schedule.py` back to `progress.md`, then:
```bash
python schedule.py
# SUCCESS again
```

## Sabotage Method Used

**Option A: Point at missing file**

Changed `progress.md` to `nonexistent_file.md` in schedule.py.
This simulates what happens when:
- A file is accidentally deleted
- A config path changes
- A mounted drive becomes unavailable
- A permission change blocks access

## Diagnosis Without Replay

From the log + spine alone, you know:
- **WHAT failed**: progress.md not found (log line 20)
- **WHEN it failed**: 2026-08-21 00:18:31 (log timestamp)
- **WHY it failed**: Wrong filename (log error message)
- **What needs fixing**: Human corrects the filename

The spine shows the last known good state. The log shows exactly where it broke.
Together they're enough - no replay needed.

## Why This Matters

### The Overnight Failure Scenario
Your loop runs every hour. At 2 AM, a file gets deleted. You don't wake up
until 7 AM. What do you need?

1. **schedule.log**: Shows exactly what failed and when
2. **progress.md**: Shows last known good state
3. **diagnostic_report.md**: Tells you what to fix

You do NOT need to:
- Re-run the script
- Debug in the dark
- Guess what happened

### Three-Layer Safety
1. **Log** (schedule.log): Detailed step-by-step record
2. **Spine** (progress.md): Persistent state with success/failure status
3. **Alert** (NEEDS HUMAN messages): Clear signal that requires human action

## What I Learned

- My loop costs $0.11/month at hourly cadence
- How to log properly so the spine is never silent
- How to diagnose failure from spine + log alone
- Why rehearsing failure while watching is cheap
- The three-layer safety: log + spine + alert
- Overnight failures aren't catastrophes when you have observability
