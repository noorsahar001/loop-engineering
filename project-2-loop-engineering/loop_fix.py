"""loop_fix.py - Conditional loop with maker-checker pattern.

Runs pytest as an external command, checks the exit code, and stops
when tests pass or the cap is hit.
"""
import subprocess
import sys

MAX_ATTEMPTS = 6
TEST_CMD = [sys.executable, "-m", "pytest", "tests.py", "-v"]


def run_tests():
    """Run the test command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        TEST_CMD,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def main():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n{'='*50}")
        print(f"Attempt {attempt} of {MAX_ATTEMPTS}")
        print(f"{'='*50}")

        exit_code, stdout, stderr = run_tests()

        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)

        if exit_code == 0:
            print("ALL TESTS PASSED")
            return 0
        else:
            print(f"Tests FAILED (exit code {exit_code}). Retrying...")

    print(f"\nCAPPED - tests did not pass in {MAX_ATTEMPTS} tries")
    return 1


if __name__ == "__main__":
    sys.exit(main())
