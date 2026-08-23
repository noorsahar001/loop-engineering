# Project 2: Make the Test Pass, than Stop

## Concept 5: Conditional Loop

A **conditional loop** runs until a specific condition is met. Unlike Concept 4 (in-session loop with file-based stop), Concept 5 uses an **external test command's exit code** as the stopping condition.

| Concept | Stop mechanism | Authority |
|---------|---------------|-----------|
| Concept 4 | File created/deleted in workspace | Agent decides |
| Concept 5 | Exit code of test command (0 = pass) | Test runner decides |

The key difference: in Concept 5, the agent does NOT decide "I think it's fixed now." Instead, an external tool (pytest) runs independently and returns an exit code. The loop respects that exit code as the source of truth.

## Concept 11: Maker-Checker Pattern

The **maker-checker pattern** separates two roles:

- **Maker** (the agent): Writes and edits code in `app.py`
- **Checker** (the test runner): Runs `pytest` and reports pass/fail via exit code

Why the test runner is the authority:
- The agent might have blind spots or bugs in its own reasoning
- The test runner is objective: it either passes or fails, no ambiguity
- The loop never overrides the test runner's judgment
- If the agent "thinks" the code is fixed but tests fail, the loop continues

## File Structure

```
project-2-loop-engineering/
  app.py        - Functions being tested (initially broken)
  tests.py      - Unit tests that check app.py (intentionally failing)
  loop_fix.py   - The conditional loop that runs tests until pass or cap
  README.md     - This file
```

## How to Run

```bash
cd project-2-loop-engineering
python loop_fix.py
```

## Interpreting Exit Codes

- **Exit code 0**: All tests passed. Loop stops immediately.
- **Exit code non-zero**: One or more tests failed. Loop continues.

## Understanding the Cap

The loop runs a maximum of **6 attempts**. If all 6 attempts fail:

```
CAPPED - tests did not pass in 6 tries
```

This means:
1. The prompt or code strategy didn't produce working fixes
2. The agent needs a different approach
3. Consider: Are the tests too strict? Is the agent editing the wrong files? Is the fix incomplete?

## Example Runs

### Success (stops at attempt 3)
```
Attempt 1 of 6
Tests FAILED (exit code 1). Retrying...
Attempt 2 of 6
Tests FAILED (exit code 1). Retrying...
Attempt 3 of 6
ALL TESTS PASSED
```

### Failure (cap hit at attempt 6)
```
Attempt 5 of 6
Tests FAILED (exit code 1). Retrying...
Attempt 6 of 6
Tests FAILED (exit code 1). Retrying...
CAPPED - tests did not pass in 6 tries
```
This means the prompt/strategy didn't work. Adjust and retry.

## Key Learning Points

1. The loop does NOT decide success - the test command does
2. Exit code 0 = pass, anything else = fail
3. The cap prevents infinite loops and signals when to rethink
4. Maker-checker keeps the agent honest - it can't skip verification
