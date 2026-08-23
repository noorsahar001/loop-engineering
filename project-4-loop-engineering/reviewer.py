import sys
import os
import importlib.util

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BUGGY_PATH = os.path.join(PROJECT_DIR, "buggy_app.py")

BRANCH_MAP = {
    "good": os.path.join(PROJECT_DIR, "good_fix_branch", "buggy_app.py"),
    "bad": os.path.join(PROJECT_DIR, "bad_fix_branch", "buggy_app.py"),
}


def load_module(path, name="target_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def reviewer_check(fix_path, branch_name):
    print("=" * 60)
    print(f"REVIEWER — Reviewing branch: {branch_name}")
    print(f"Reviewing file: {fix_path}")
    print("=" * 60)

    reasons = []
    all_pass = True

    # Load both versions
    print("\n[1] Loading original buggy_app.py...")
    original = load_module(BUGGY_PATH, "original")
    print("    Loaded.")

    print(f"\n[2] Loading fixed version from {branch_name}...")
    try:
        fixed = load_module(fix_path, "fixed")
        print("    Loaded.")
    except Exception as e:
        print(f"    FAILED to load: {e}")
        print("\nFAIL — Fix file could not be loaded or executed.")
        return False

    # Check 1: divide_safe(10, 2) must return 5.0
    print("\n[3] Running tests...")
    print("    Test 1: divide_safe(10, 2) == 5.0")
    try:
        result = fixed.divide_safe(10, 2)
        assert result == 5.0, f"Expected 5.0, got {result!r}"
        print("    PASS")
    except Exception as e:
        print(f"    FAIL — {e}")
        reasons.append(f"divide_safe(10, 2) did not return 5.0: {e}")
        all_pass = False

    # Check 2: divide_safe(10, 0) must NOT crash
    print("    Test 2: divide_safe(10, 0) must not crash")
    try:
        result = fixed.divide_safe(10, 0)
        print(f"    PASS (returned {result!r})")
    except ZeroDivisionError:
        print("    FAIL — ZeroDivisionError raised (bug not fixed!)")
        reasons.append("divide_safe(10, 0) raised ZeroDivisionError — original bug not fixed")
        all_pass = False
    except Exception as e:
        print(f"    FAIL — Unexpected error: {e}")
        reasons.append(f"divide_safe(10, 0) raised unexpected error: {e}")
        all_pass = False

    # Check 3: divide_safe(10, 0) must return exact error string
    print("    Test 3: divide_safe(10, 0) == 'Error: division by zero'")
    try:
        result = fixed.divide_safe(10, 0)
        expected_msg = "Error: division by zero"
        assert result == expected_msg, f"Expected {expected_msg!r}, got {result!r}"
        print("    PASS")
    except AssertionError:
        print(f"    FAIL — Returned wrong value: {result!r}")
        reasons.append(f"divide_safe(10, 0) returned {result!r}, expected 'Error: division by zero'")
        all_pass = False
    except Exception as e:
        print(f"    FAIL — {e}")
        reasons.append(f"divide_safe(10, 0) check failed: {e}")
        all_pass = False

    # Check 4: Normal division preserved
    print("    Test 4: divide_safe(100, 4) == 25.0 (normal division preserved)")
    try:
        result = fixed.divide_safe(100, 4)
        assert result == 25.0, f"Expected 25.0, got {result!r}"
        print("    PASS")
    except Exception as e:
        print(f"    FAIL — {e}")
        reasons.append(f"Normal division broken: divide_safe(100, 4) = {result!r}")
        all_pass = False

    # Check 5: Edge case — negative numbers
    print("    Test 5: divide_safe(-10, 2) == -5.0 (edge case)")
    try:
        result = fixed.divide_safe(-10, 2)
        assert result == -5.0, f"Expected -5.0, got {result!r}"
        print("    PASS")
    except Exception as e:
        print(f"    FAIL — {e}")
        reasons.append(f"Edge case broken: divide_safe(-10, 2) = {result!r}")
        all_pass = False

    # Check 6: Zero numerator
    print("    Test 6: divide_safe(0, 5) == 0.0")
    try:
        result = fixed.divide_safe(0, 5)
        assert result == 0.0, f"Expected 0.0, got {result!r}"
        print("    PASS")
    except Exception as e:
        print(f"    FAIL — {e}")
        reasons.append(f"divide_safe(0, 5) = {result!r}, expected 0.0")
        all_pass = False

    # Check 7: Read source code to verify no unrelated changes
    print("\n[4] Checking source code for unrelated changes...")
    fixed_source = read_file(fix_path)
    original_source = read_file(BUGGY_PATH)

    if "run_tests" in original_source and "run_tests" not in fixed_source:
        reasons.append("run_tests function was removed — unrelated change detected")
        all_pass = False
        print("    FAIL — run_tests removed")
    else:
        print("    PASS — test infrastructure preserved")

    # Final verdict
    print("\n" + "=" * 60)
    if all_pass:
        print("RESULT: PASS")
        print("All checks passed. Fix is correct.")
        print("\nOpening PR...")
        print("PR would be opened")
    else:
        print("RESULT: FAIL")
        print(f"Failed {len(reasons)} check(s):")
        for i, r in enumerate(reasons, 1):
            print(f"  {i}. {r}")
        print("\nPR blocked — fix not ready")
    print("=" * 60)

    return all_pass


def main():
    if len(sys.argv) < 2:
        branch = "good"
    else:
        branch = sys.argv[1].lower()

    if branch not in BRANCH_MAP:
        print(f"Unknown branch: {branch!r}")
        print(f"Available branches: {', '.join(BRANCH_MAP.keys())}")
        sys.exit(1)

    fix_path = BRANCH_MAP[branch]

    if not os.path.exists(fix_path):
        print(f"Fix file not found: {fix_path}")
        print(f"Run implementer.py first to generate the good fix.")
        sys.exit(1)

    success = reviewer_check(fix_path, branch)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
