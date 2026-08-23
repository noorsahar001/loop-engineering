#!/usr/bin/env python3
"""Review Audit Results - The CHECKER
Validates audit output and determines if it's acceptable.
"""

import sys
import re

MAX_FINDINGS = 50
MAX_HIGH_PRIORITY = 10

def review_audit(audit_file):
    """Validate audit results"""
    try:
        with open(audit_file, 'r') as f:
            results = f.read()
    except FileNotFoundError:
        print(f"FAIL: Audit file {audit_file} not found")
        return 1
    
    if not results.strip():
        print("FAIL: Audit file is empty")
        return 1
    
    # Check for critical errors
    if 'ERROR' in results and 'Could not read' not in results:
        print("FAIL: Audit found critical errors")
        return 1
    
    # Count findings
    todo_count = len(re.findall(r'\bTODO\b', results))
    fixme_count = len(re.findall(r'\bFIXME\b', results))
    hack_count = len(re.findall(r'\bHACK\b', results))
    xxx_count = len(re.findall(r'\bXXX\b', results))
    
    total = todo_count + fixme_count + hack_count + xxx_count
    
    # Check high priority items
    high_priority = fixme_count + hack_count
    
    if high_priority > MAX_HIGH_PRIORITY:
        print(f"FAIL: Too many high-priority items ({high_priority} > {MAX_HIGH_PRIORITY})")
        return 1
    
    if total > MAX_FINDINGS:
        print(f"FAIL: Too many total findings ({total} > {MAX_FINDINGS})")
        return 1
    
    # All checks passed
    print(f"PASS: {total} findings (TODO:{todo_count}, FIXME:{fixme_count}, HACK:{hack_count}, XXX:{xxx_count})")
    print(f"  High priority: {high_priority}")
    print(f"  Low priority: {todo_count + xxx_count}")
    return 0

if __name__ == '__main__':
    audit_file = sys.argv[1] if len(sys.argv) > 1 else 'audit_output.txt'
    sys.exit(review_audit(audit_file))
