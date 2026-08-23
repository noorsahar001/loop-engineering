#!/bin/bash
set -e

CHORE_NAME="todo-audit"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="audit_${TIMESTAMP}.log"
PROJECT_ROOT=$(pwd)

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== BEAT STARTED: $CHORE_NAME ==="

# Part 1: Read spine
log "Reading audit_progress.md (spine)"
if [ ! -f audit_progress.md ]; then
    log "ERROR: Spine missing! Creating new one"
    cat > audit_progress.md << 'EOF'
# Audit Progress Log
Last run: Never
Status: Initializing
EOF
fi

# Part 2: Budget check
log "Checking budget guards"
MAX_TOKENS_PER_RUN=5000
MAX_MONTHLY_COST=50.0
MAX_RUNS_PER_WEEK=35

if [ -f budget_state.json ]; then
    TOKENS_USED=$(python -c "import json; print(json.load(open('budget_state.json')).get('tokens_used', 0))")
    MONTHLY_COST=$(python -c "import json; print(json.load(open('budget_state.json')).get('monthly_cost', 0.0))")
    RUNS_THIS_WEEK=$(python -c "import json; print(json.load(open('budget_state.json')).get('runs_this_week', 0))")
    
    if [ "$TOKENS_USED" -gt "$MAX_TOKENS_PER_RUN" ]; then
        log "ERROR: BUDGET EXCEEDED: $TOKENS_USED > $MAX_TOKENS_PER_RUN tokens"
        exit 1
    fi
    
    OVER=$(python -c "print(1 if $MONTHLY_COST > $MAX_MONTHLY_COST else 0)")
    if [ "$OVER" -eq 1 ]; then
        log "ERROR: MONTHLY BUDGET: \$$MONTHLY_COST > \$$MAX_MONTHLY_COST"
        exit 1
    fi
    
    if [ "$RUNS_THIS_WEEK" -ge "$MAX_RUNS_PER_WEEK" ]; then
        log "ERROR: WEEKLY LIMIT: $RUNS_THIS_WEEK >= $MAX_RUNS_PER_WEEK runs"
        exit 1
    fi
fi

# Part 3: Create worktree
log "Creating isolated worktree"
WORKTREE_NAME="wt-audit-${TIMESTAMP}"
git worktree add "$WORKTREE_NAME" main 2>/dev/null || {
    log "Worktree creation failed, running in main directory"
    WORKTREE_NAME=""
}

if [ -n "$WORKTREE_NAME" ]; then
    cd "$WORKTREE_NAME"
fi

# Part 4: Run maker (the actual work)
log "Running audit script (maker)"
python "$PROJECT_ROOT/audit_todos.py" > audit_output.txt 2>&1
AUDIT_EXIT=$?

if [ $AUDIT_EXIT -ne 0 ]; then
    log "ERROR: Audit script failed with code $AUDIT_EXIT"
    cat audit_output.txt >> "$LOG_FILE"
    cd "$PROJECT_ROOT"
    git worktree remove "$WORKTREE_NAME" 2>/dev/null || true
    exit 1
fi

log "Audit completed, findings: $(wc -l < audit_output.txt) lines"

# Part 5: Run checker (reviewer)
log "Running review script (checker)"
python "$PROJECT_ROOT/review_audit.py" audit_output.txt
REVIEW_EXIT=$?

if [ $REVIEW_EXIT -eq 0 ]; then
    log "REVIEW PASSED"
    REVIEW_STATUS="PASSED"
else
    log "REVIEW FAILED"
    REVIEW_STATUS="FAILED"
    cd "$PROJECT_ROOT"
    git worktree remove "$WORKTREE_NAME" 2>/dev/null || true
    exit 1
fi

# Part 6: Update spine
log "Updating spine (audit_progress.md)"
cd "$PROJECT_ROOT"

TODO_COUNT=$(grep -c "TODO\|FIXME\|HACK\|XXX" "$WORKTREE_NAME/audit_output.txt" 2>/dev/null || echo "0")

cat >> audit_progress.md << EOF

## Run on $(date)
- Status: $REVIEW_STATUS
- Worktree: $WORKTREE_NAME
- Findings: $TODO_COUNT TODOs/FIXMEs found
- Log: $LOG_FILE
EOF

# Update spine header
sed -i "1s/.*/# Audit Progress Log/" audit_progress.md
sed -i "2s/.*/Last run: $(date +'%Y-%m-%d %H:%M:%S')/" audit_progress.md
sed -i "3s/.*/Status: $REVIEW_STATUS/" audit_progress.md

# Update budget state
python "$PROJECT_ROOT/update_budget.py" "$TOKENS_USED" "$MONTHLY_COST" "$RUNS_THIS_WEEK"

log "=== BEAT COMPLETED SUCCESSFULLY ==="

# Cleanup worktree
git worktree remove "$WORKTREE_NAME" 2>/dev/null || true
