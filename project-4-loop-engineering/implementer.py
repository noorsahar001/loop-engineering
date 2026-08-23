import os
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_PATH = os.path.join(PROJECT_DIR, ".opencode", "skills", "SKILL.md")
BUGGY_PATH = os.path.join(PROJECT_DIR, "buggy_app.py")
GOOD_BRANCH_DIR = os.path.join(PROJECT_DIR, "good_fix_branch")
GOOD_FIX_PATH = os.path.join(GOOD_BRANCH_DIR, "buggy_app.py")


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    print("=" * 50)
    print("IMPLEMENTER — The Maker")
    print("=" * 50)

    # Step 1: Read the buggy app
    print("\n[1] Reading buggy_app.py...")
    buggy_code = read_file(BUGGY_PATH)
    print(f"    Loaded {len(buggy_code)} characters.")

    # Step 2: Read the OpenCode skill
    print("\n[2] Reading OpenCode skill: .opencode/skills/SKILL.md...")
    skill_content = read_file(SKILL_PATH)
    print(f"    Skill loaded: {len(skill_content)} characters.")
    print("    Skill name: fix-bug")

    # Step 3: Parse skill instructions (extract fix steps)
    print("\n[3] Following skill instructions...")
    print("    - Bug: divide_safe does not handle b == 0")
    print("    - Fix: Add guard clause for b == 0")
    print("    - Return 'Error: division by zero' when b is zero")

    # Step 4: Apply the fix
    print("\n[4] Applying the fix...")
    fixed_code = (
        'def divide_safe(a, b):\n'
        '    if b == 0:\n'
        '        return "Error: division by zero"\n'
        '    return a / b\n'
        '\n'
        '\n'
        'def run_tests():\n'
        '    print("Running tests...")\n'
        '    passed = 0\n'
        '    failed = 0\n'
        '\n'
        '    try:\n'
        '        result = divide_safe(10, 2)\n'
        '        assert result == 5.0, f"Expected 5.0, got {result}"\n'
        '        print("  PASS: divide_safe(10, 2) == 5.0")\n'
        '        passed += 1\n'
        '    except AssertionError as e:\n'
        '        print(f"  FAIL: divide_safe(10, 2) — {e}")\n'
        '        failed += 1\n'
        '\n'
        '    try:\n'
        '        result = divide_safe(10, 0)\n'
        '        assert result == "Error: division by zero", f"Expected \'Error: division by zero\', got {result!r}"\n'
        '        print("  PASS: divide_safe(10, 0) returns error message")\n'
        '        passed += 1\n'
        '    except ZeroDivisionError:\n'
        '        print("  FAIL: divide_safe(10, 0) raised ZeroDivisionError (bug!)")\n'
        '        failed += 1\n'
        '    except AssertionError as e:\n'
        '        print(f"  FAIL: divide_safe(10, 0) — {e}")\n'
        '        failed += 1\n'
        '\n'
        '    print(f"\\nResults: {passed} passed, {failed} failed")\n'
        '    return failed == 0\n'
        '\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    success = run_tests()\n'
        '    exit(0 if success else 1)\n'
    )

    # Step 5: Write the fixed version
    print(f"\n[5] Writing fixed version to {GOOD_BRANCH_DIR}/...")
    os.makedirs(GOOD_BRANCH_DIR, exist_ok=True)
    with open(GOOD_FIX_PATH, "w", encoding="utf-8") as f:
        f.write(fixed_code)
    print(f"    Written to: {GOOD_FIX_PATH}")

    # Step 6: Run basic tests
    print("\n[6] Running basic validation tests...")
    test_cases = [
        ("divide_safe(10, 2) == 5.0", 10, 2, 5.0),
        ("divide_safe(10, 0) returns error", 10, 0, "Error: division by zero"),
        ("divide_safe(0, 5) == 0.0", 0, 5, 0.0),
    ]

    # Import and test the fixed code
    import importlib.util
    spec = importlib.util.spec_from_file_location("fixed_app", GOOD_FIX_PATH)
    fixed_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixed_module)

    all_pass = True
    for desc, a, b, expected in test_cases:
        result = fixed_module.divide_safe(a, b)
        if result == expected:
            print(f"    PASS: {desc}")
        else:
            print(f"    FAIL: {desc} — got {result!r}")
            all_pass = False

    # Step 7: Print result
    print("\n" + "=" * 50)
    if all_pass:
        print("Fix drafted in good_fix_branch/")
    else:
        print("Fix validation FAILED — check output above")
    print("=" * 50)


if __name__ == "__main__":
    main()
