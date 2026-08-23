import sys
import os

def implement_fix(candidate):
    """Draft a fix for a specific bug candidate."""
    
    fix_map = {
        "candidate-1": {
            "bug": "division_by_zero",
            "file": "buggy_app.py",
            "fix": """def safe_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    result = safe_divide(10, 2)
    print(f"Result: {result}")
"""
        },
        "candidate-2": {
            "bug": "off_by_one_error",
            "file": "buggy_app.py",
            "fix": """def count_range(start, end):
    return list(range(start, end + 1))

if __name__ == "__main__":
    numbers = count_range(1, 5)
    print(f"Numbers: {numbers}")
"""
        },
        "candidate-3": {
            "bug": "missing_validation",
            "file": "buggy_app.py",
            "fix": """def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    return True

if __name__ == "__main__":
    result = validate_age(25)
    print(f"Validation passed: {result}")
"""
        }
    }
    
    if candidate not in fix_map:
        print(f"Unknown candidate: {candidate}")
        return False
    
    fix_info = fix_map[candidate]
    
    fix_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "good_fix_branch")
    os.makedirs(fix_dir, exist_ok=True)
    
    fix_file = os.path.join(fix_dir, fix_info["file"])
    with open(fix_file, "w") as f:
        f.write(fix_info["fix"])
    
    print(f"Fix drafted for {candidate} ({fix_info['bug']})")
    print(f"  Written to: good_fix_branch/{fix_info['file']}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python implementer.py CANDIDATE")
        print("Example: python implementer.py candidate-1")
        sys.exit(1)
    
    candidate = sys.argv[1]
    success = implement_fix(candidate)
    
    if not success:
        sys.exit(1)
