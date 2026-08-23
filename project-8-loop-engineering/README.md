# Project 8: Your own Daily loop   
# Full Loop - TODO Audit (Capstone)

This is the capstone project combining all six parts of loop engineering.

## Six Parts of This Loop

### 1. Heartbeat (When to run)
- Scheduled: Weekdays 9 AM via cron
- Triggered by: `0 9 * * 1-5 bash run_chore.sh`
- Cadence: 5 times per week

### 2. Worktree (Isolation)
- Each run gets isolated `wt-audit-TIMESTAMP/` workspace
- Changes don't affect main branch
- Git-clean separation

### 3. Skill (How to do it)
- `.opencode/skills/todo-audit.yml`
- Reusable instructions for auditing
- Not code, just the process

### 4. Maker-Checker (Validation)
- **Maker:** `audit_todos.py` scans Python files for TODOs
- **Checker:** `review_audit.py` validates results
- Only safe changes get approved

### 5. Connector (Integration)
- Cron job fires `run_chore.sh`
- Could be extended to GitHub webhook
- External system triggers loop

### 6. Spine (Memory)
- `audit_progress.md` tracks every run
- Records what was found, when, and status
- Loop's persistent state

## Budget Guards

Max tokens per run: 5000
Max monthly cost: $50
Max runs per week: 35

Loop stops if any limit is exceeded.

## Concept 15: Understanding Keeping Up

**Question:** As your loop makes changes, do you still understand
what your project is doing?

If loop runs 5x/week and changes things, you MUST review each change.
If you can't keep up (too many changes, too fast), SLOW THE LOOP DOWN.

Formula:
```
Loop Speed <= Your Review Speed
```

If Loop Speed > Your Review Speed:
Then SLOW THE LOOP DOWN (less heartbeat)

## Running the Loop

```bash
# Manual run (for testing):
bash run_chore.sh

# Schedule it (cron):
0 9 * * 1-5 cd /path/to/project-8 && bash run_chore.sh

# Check spine after run:
cat audit_progress.md

# Check logs:
ls -lt audit_*.log | head -1
```

## One Week Unattended

After setting up:
1. Walk away (don't watch terminal)
2. Let it run 5 days (weekdays)
3. Check audit_progress.md each morning
4. Review any findings
5. Judge: Do you trust what it's doing?

## When It Fails (And It Will)

Don't panic. Use spine + logs:

```bash
cat audit_progress.md        # What was it doing?
tail audit_*.log             # Why did it fail?
git log -5 --oneline         # What did it change?
```

Then fix ONE thing:
- Budget was too low? Raise it
- Checker was too strict? Loosen it
- Heartbeat is too frequent? Slow it down
- Spine is unclear? Add more logging

Re-run and verify. Don't change everything at once.

## Success Criteria

- Loop ran 5+ times without manual intervention
- Spine (audit_progress.md) updated each time
- You reviewed at least 3 audit results
- You understand what loop changed
- Budget guards held (no overspend)
- At least one failed run that you diagnosed from spine alone
- You know whether to speed it up or slow it down
