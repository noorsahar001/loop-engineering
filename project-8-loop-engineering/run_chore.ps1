# run_chore.ps1 - Windows PowerShell version of run_chore.sh
$ErrorActionPreference = "Stop"

$CHORE_NAME = "todo-audit"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_FILE = "audit_$TIMESTAMP.log"
$PROJECT_ROOT = Get-Location

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LOG_FILE -Value $line
}

Log "=== BEAT STARTED: $CHORE_NAME ==="

# Part 1: Read spine
Log "Reading audit_progress.md (spine)"
if (!(Test-Path "audit_progress.md")) {
    Log "ERROR: Spine missing! Creating new one"
    @"
# Audit Progress Log
Last run: Never
Status: Initializing
"@ | Out-File -FilePath "audit_progress.md" -Encoding utf8
}

# Part 2: Budget check
Log "Checking budget guards"
$MAX_TOKENS_PER_RUN = 5000
$MAX_MONTHLY_COST = 50.0
$MAX_RUNS_PER_WEEK = 35

if (Test-Path "budget_state.json") {
    $state = Get-Content "budget_state.json" | ConvertFrom-Json
    $TOKENS_USED = $state.tokens_used
    $MONTHLY_COST = $state.monthly_cost
    $RUNS_THIS_WEEK = $state.runs_this_week
    
    if ($TOKENS_USED -gt $MAX_TOKENS_PER_RUN) {
        Log "ERROR: BUDGET EXCEEDED: $TOKENS_USED > $MAX_TOKENS_PER_RUN tokens"
        exit 1
    }
    
    if ($MONTHLY_COST -gt $MAX_MONTHLY_COST) {
        Log "ERROR: MONTHLY BUDGET: `$$MONTHLY_COST > `$$MAX_MONTHLY_COST"
        exit 1
    }
    
    if ($RUNS_THIS_WEEK -ge $MAX_RUNS_PER_WEEK) {
        Log "ERROR: WEEKLY LIMIT: $RUNS_THIS_WEEK >= $MAX_RUNS_PER_WEEK runs"
        exit 1
    }
}

# Part 3: Create worktree
Log "Creating isolated worktree"
$WORKTREE_NAME = "wt-audit-$TIMESTAMP"
try {
    git worktree add $WORKTREE_NAME main 2>$null
} catch {
    Log "Worktree creation failed, running in main directory"
    $WORKTREE_NAME = ""
}

if ($WORKTREE_NAME -ne "") {
    Set-Location $WORKTREE_NAME
}

# Part 4: Run maker (the actual work)
Log "Running audit script (maker)"
python "$PROJECT_ROOT\audit_todos.py" > audit_output.txt 2>&1
$AUDIT_EXIT = $LASTEXITCODE

if ($AUDIT_EXIT -ne 0) {
    Log "ERROR: Audit script failed with code $AUDIT_EXIT"
    Get-Content audit_output.txt | Add-Content "$LOG_FILE"
    Set-Location $PROJECT_ROOT
    git worktree remove $WORKTREE_NAME 2>$null
    exit 1
}

$lineCount = (Get-Content audit_output.txt | Measure-Object -Line).Lines
Log "Audit completed, findings: $lineCount lines"

# Part 5: Run checker (reviewer)
Log "Running review script (checker)"
python "$PROJECT_ROOT\review_audit.py" audit_output.txt
$REVIEW_EXIT = $LASTEXITCODE

if ($REVIEW_EXIT -eq 0) {
    Log "REVIEW PASSED"
    $REVIEW_STATUS = "PASSED"
} else {
    Log "REVIEW FAILED"
    $REVIEW_STATUS = "FAILED"
    Set-Location $PROJECT_ROOT
    git worktree remove $WORKTREE_NAME 2>$null
    exit 1
}

# Part 6: Update spine
Log "Updating spine (audit_progress.md)"
Set-Location $PROJECT_ROOT

$auditFile = if ($WORKTREE_NAME -ne "" -and (Test-Path "$WORKTREE_NAME\audit_output.txt")) { "$WORKTREE_NAME\audit_output.txt" } else { "audit_output.txt" }
$TODO_COUNT = Select-String -Path $auditFile -Pattern "TODO|FIXME|HACK|XXX" | Measure-Object | Select-Object -ExpandProperty Count

$runEntry = @"

## Run on $(Get-Date)
- Status: $REVIEW_STATUS
- Worktree: $WORKTREE_NAME
- Findings: $TODO_COUNT TODOs/FIXMEs found
- Log: $LOG_FILE
"@
Add-Content -Path "audit_progress.md" -Value $runEntry

# Update spine header
$content = Get-Content "audit_progress.md" -Raw
$content = $content -replace "^# Audit Progress Log", "# Audit Progress Log"
$content = $content -replace "Last run:.*", "Last run: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$content = $content -replace "Status:.*", "Status: $REVIEW_STATUS"
$content | Out-File "audit_progress.md" -Encoding utf8

# Update budget state
python "$PROJECT_ROOT\update_budget.py" $TOKENS_USED $MONTHLY_COST $RUNS_THIS_WEEK

Log "=== BEAT COMPLETED SUCCESSFULLY ==="

# Cleanup worktree
git worktree remove $WORKTREE_NAME 2>$null
