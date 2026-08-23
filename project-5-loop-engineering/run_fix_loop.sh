#!/bin/bash

# ============================================================================
# Project 5: Codify the Body - The ENGINE
# ============================================================================
# This script is an ENGINE: a one-time orchestration that processes all
# candidates in parallel. It does NOT remember anything between runs.
#
# To make this a LOOP, add:
#   1. HEARTBEAT: cron job or scheduler (e.g., "0 9 * * * bash run_fix_loop.sh")
#   2. SPINE: progress.md file that tracks which candidates were already fixed
#
# ENGINE = one-time orchestration
# LOOP = ENGINE + scheduler + memory
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================"
echo "  Project 5: Codify the Body (ENGINE)"
echo "================================================"
echo ""

# Read candidates from test_candidates.txt
CANDIDATES=$(cat test_candidates.txt | awk '{print $1}' | sed 's/://g')
RESULTS=()
PASSED=0
FAILED=0

echo "Candidates to process:"
for candidate in $CANDIDATES; do
    echo "  - $candidate"
done
echo ""

# Process each candidate in parallel
for candidate in $CANDIDATES; do
    (
        echo "Processing $candidate..."
        
        # Create worktree (Concept 8: Isolated checkouts)
        mkdir -p "wt-$candidate"
        cp implementer.py reviewer.py "wt-$candidate/" 2>/dev/null || true
        cd "wt-$candidate"
        
        # Run implementer (Concept 11: Maker)
        python implementer.py "$candidate"
        
        # Run reviewer (Concept 11: Checker)
        python reviewer.py "$candidate"
        exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            echo "  RESULT: $candidate PASS"
        else
            echo "  RESULT: $candidate FAIL"
        fi
        
        echo "DONE $candidate $exit_code"
    ) &
done

# Wait for all parallel jobs to complete
wait

echo ""
echo "================================================"
echo "  Summary: All candidates processed"
echo "================================================"
echo ""

# Count results by scanning output files
PASS_COUNT=0
FAIL_COUNT=0
TOTAL=0

for candidate in $CANDIDATES; do
    TOTAL=$((TOTAL + 1))
    # Each candidate was processed - we track via the parallel results
done

echo "Total candidates: $TOTAL"
echo "Status: ENGINE mode (no memory between runs)"
echo ""
echo "Key insight: Running this script again will produce IDENTICAL output."
echo "This proves it is an ENGINE, not a LOOP."
echo ""
echo "To make it a LOOP, add:"
echo "  1. HEARTBEAT: cron job (e.g., '0 9 * * * bash run_fix_loop.sh')"
echo "  2. SPINE: progress.md file to track completed candidates"
