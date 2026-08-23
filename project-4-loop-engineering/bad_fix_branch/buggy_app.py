def divide_safe(a, b):
    if b == 0:
        return "Error"
    return a / b


def run_tests():
    print("Running tests...")
    passed = 0
    failed = 0

    try:
        result = divide_safe(10, 2)
        assert result == 5.0, f"Expected 5.0, got {result}"
        print("  PASS: divide_safe(10, 2) == 5.0")
        passed += 1
    except AssertionError as e:
        print(f"  FAIL: divide_safe(10, 2) — {e}")
        failed += 1

    try:
        result = divide_safe(10, 0)
        assert result == "Error: division by zero", f"Expected 'Error: division by zero', got {result!r}"
        print("  PASS: divide_safe(10, 0) returns error message")
        passed += 1
    except ZeroDivisionError:
        print("  FAIL: divide_safe(10, 0) raised ZeroDivisionError (bug!)")
        failed += 1
    except AssertionError as e:
        print(f"  FAIL: divide_safe(10, 0) — {e}")
        failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
