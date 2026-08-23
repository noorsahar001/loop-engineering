# Project 5: Codify the Body

## Concepts
- **Concept 8 (Worktree)**: Isolated checkouts for each candidate
- **Concept 11 (Maker-Checker)**: Implementer drafts, Reviewer grades

## The Engine (run_fix_loop.sh)

This script is an ENGINE - a one-time orchestration that processes all candidates.
It does NOT remember anything between runs.

### How it works:
1. Reads candidates from `test_candidates.txt`
2. For each candidate, runs in parallel:
   - Creates an isolated worktree (`git worktree add wt-CANDIDATE main`)
   - Runs `implementer.py` to draft a fix
   - Runs `reviewer.py` to grade the fix
3. Collects PASS/FAIL results
4. Prints a summary

## Proof: No Memory

**RUN 1:** `bash run_fix_loop.sh`
```
Output: "Processed 3 candidates, 2 PASSED, 1 FAILED"
```

**RUN 2:** `bash run_fix_loop.sh`
```
Output: IDENTICAL (same candidates, same results)
```

**Why?** Because the script does NOT read/write any state file.
It just processes the same candidates every time.

## To Make This a LOOP

Add two things:

### 1. HEARTBEAT (Scheduler/Timer)
Schedule this script to run periodically.
Example: cron job to run daily at 9 AM
```
0 9 * * * bash /path/to/run_fix_loop.sh
```

### 2. SPINE (State File)
Create `progress.md` that tracks completed candidates.
- Script reads: which candidates already fixed?
- Script writes: mark candidate as fixed
- Next run only processes NEW candidates

With heartbeat + spine, identical runs become a true LOOP.

## How to Run

```bash
bash run_fix_loop.sh
```

## Key Learning

| ENGINE | LOOP |
|--------|------|
| One-time orchestration | Repeated runs with memory |
| No state between runs | State preserved in spine file |
| Same input = same output | Different output each run |
| Stateless | Stateful |

**ENGINE = one-time orchestration**
**LOOP = ENGINE + scheduler + memory**

You prove the difference by running the ENGINE twice and seeing identical output.
