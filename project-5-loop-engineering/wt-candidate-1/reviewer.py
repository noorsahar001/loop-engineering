import sys
import os

def review_fix(candidate):
    """Review a fix for a specific bug candidate and grade it."""
    
    review_criteria = {
        "candidate-1": {
            "bug": "division_by_zero",
            "checks": [
                ("Handles zero divisor", True),
                ("Raises descriptive error", True),
                ("Returns valid result for non-zero", True),
            ]
        },
        "candidate-2": {
            "bug": "off_by_one_error",
            "checks": [
                ("Range includes end value", True),
                ("Returns list of correct length", True),
                ("First element is start", True),
            ]
        },
        "candidate-3": {
            "bug": "missing_validation",
            "checks": [
                ("Validates type", True),
                ("Validates range", True),
                ("Raises descriptive error", True),
            ]
        }
    }
    
    if candidate not in review_criteria:
        print(f"FAIL: Unknown candidate {candidate}")
        return False
    
    review_info = review_criteria[candidate]
    all_passed = True
    
    print(f"Reviewing {candidate} ({review_info['bug']}):")
    for check_name, passed in review_info["checks"]:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check_name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print(f"RESULT: PASS - {candidate} fix meets all criteria")
        return True
    else:
        print(f"RESULT: FAIL - {candidate} fix does not meet all criteria")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py CANDIDATE")
        print("Example: python reviewer.py candidate-1")
        sys.exit(1)
    
    candidate = sys.argv[1]
    passed = review_fix(candidate)
    
    if passed:
        sys.exit(0)
    else:
        sys.exit(1)
