# Project 4: A fix loop with a real Checker 

A demonstration of the Maker-Checker loop using isolated workspaces, reusable agent skills, and strict code review.

This project implements **Concept 8** (Worktree Isolation), **Concept 9** (Skills as Reusable Instructions), and **Concept 11** (Maker-Checker Loop).

---

## Concepts

### Concept 8: Worktree Isolation

A separate worktree or branch isolates work so changes can be developed and reviewed without damaging the main working copy. In this project, we simulate worktrees with separate directories:

- `good_fix_branch/` — holds a correct fix
- `bad_fix_branch/` — holds a deliberately broken fix

Each branch is independent. Changes in one do not affect the other or the original `buggy_app.py`. This isolation ensures that:

- Experiments cannot corrupt production code
- Multiple fixes can be developed in parallel
- Reviewers can inspect changes against a known baseline

### Concept 9: Skills as Reusable Instructions

A skill is a reusable instruction file for an agent. It is separate from application code so the same instructions can be reused by different implementations or agents.

The skill lives at `.opencode/skills/SKILL.md` and contains:

- What the bug is
- Why it happens (root cause)
- Step-by-step fix instructions
- Validation criteria
- Constraints on the fix

The implementer reads this skill and follows its instructions to produce a fix. The same skill could be read by a different agent or implementation in the future.

### Concept 11: Maker-Checker Loop

The maker/implementer creates the solution. The checker/reviewer independently verifies it. This separation ensures:

- No code is accepted without independent validation
- The reviewer does not trust the implementer's claims
- Bugs and regressions are caught before reaching production

The loop works as:

```
Implementer
    |
    reads SKILL.md
    |
    drafts fix
    |
Reviewer
    |
    runs tests
    |
PASS -----> PR would be opened
    |
FAIL
    |
PR blocked
    |
Fix issues
    |
Run reviewer again
```

The loop repeats until the reviewer outputs PASS.

---

## Why the Reviewer Must Be Strict

If a reviewer passes a deliberately bad fix, the reviewer is useless. A strict reviewer:

- Independently tests the fix against known expectations
- Checks the exact return values, not just that "no crash occurred"
- Verifies that normal behavior is preserved
- Detects partial fixes (e.g., wrong error message)
- Inspects source code for unrelated changes

A bad reviewer that trusts the implementer or only checks for crashes will miss subtle bugs. This project demonstrates this by including a deliberately broken fix that a strict reviewer catches.

---

## File Documentation

### `buggy_app.py`

The original application with a known bug. The `divide_safe(a, b)` function performs division without handling `b == 0`, causing a `ZeroDivisionError`. Tests expose this bug.

### `.opencode/skills/SKILL.md`

An OpenCode skill file containing reusable fix instructions. This is documentation for an agent, not executable code. It tells an implementer exactly how to fix the bug, what to validate, and what constraints to follow.

### `implementer.py`

The maker agent. It:

1. Reads the buggy application
2. Reads the OpenCode skill
3. Follows the skill's fix instructions
4. Applies the fix
5. Writes the corrected version to `good_fix_branch/`
6. Runs basic validation tests

### `reviewer.py`

The checker agent. It:

1. Loads the fixed version from a specified branch
2. Loads the original buggy version
3. Runs independent tests against the fix
4. Checks for exact return values
5. Verifies no unrelated behavior is broken
6. Outputs PASS or FAIL with specific reasons

Usage:

```
python reviewer.py good    # reviews good_fix_branch/
python reviewer.py bad     # reviews bad_fix_branch/
```

### `good_fix_branch/buggy_app.py`

The correct fix. Adds a guard clause `if b == 0: return "Error: division by zero"` before the division. All tests pass.

### `bad_fix_branch/buggy_app.py`

A deliberately broken fix. Returns `"Error"` instead of `"Error: division by zero"` when `b == 0`. This is a partial fix that prevents the crash but returns the wrong error message. The reviewer catches this.

### `README.md`

This file. Explains the project, concepts, and how to run everything.

---

## How to Run

### Run the buggy app (see the bug)

```
python buggy_app.py
```

Expected output: 1 test passes, 1 test fails with `ZeroDivisionError`.

### Run the implementer (generate the good fix)

```
python implementer.py
```

This reads the skill, applies the fix, and writes `good_fix_branch/buggy_app.py`.

### Run the reviewer on the good fix

```
python reviewer.py good
```

Expected output: **PASS** — all checks pass. PR would be opened.

### Run the reviewer on the bad fix

```
python reviewer.py bad
```

Expected output: **FAIL** — the error message is wrong. PR blocked.

---

## Example Outputs

### GOOD Fix — Reviewer Output

```
============================================================
REVIEWER — Reviewing branch: good
Reviewing file: .../good_fix_branch/buggy_app.py
============================================================

[1] Loading original buggy_app.py...
    Loaded.

[2] Loading fixed version from good...
    Loaded.

[3] Running tests...
    Test 1: divide_safe(10, 2) == 5.0
    PASS
    Test 2: divide_safe(10, 0) must not crash
    PASS (returned 'Error: division by zero')
    Test 3: divide_safe(10, 0) == 'Error: division by zero'
    PASS
    Test 4: divide_safe(100, 4) == 25.0 (normal division preserved)
    PASS
    Test 5: divide_safe(-10, 2) == -5.0 (edge case)
    PASS
    Test 6: divide_safe(0, 5) == 0.0
    PASS

[4] Checking source code for unrelated changes...
    PASS — test infrastructure preserved

============================================================
RESULT: PASS
All checks passed. Fix is correct.

Opening PR...
PR would be opened
============================================================
```

### BAD Fix — Reviewer Output

```
============================================================
REVIEWER — Reviewing branch: bad
Reviewing file: .../bad_fix_branch/buggy_app.py
============================================================

[1] Loading original buggy_app.py...
    Loaded.

[2] Loading fixed version from bad...
    Loaded.

[3] Running tests...
    Test 1: divide_safe(10, 2) == 5.0
    PASS
    Test 2: divide_safe(10, 0) must not crash
    PASS (returned 'Error')
    Test 3: divide_safe(10, 0) == 'Error: division by zero'
    FAIL — Returned wrong value: 'Error'
    ...

============================================================
RESULT: FAIL
Failed 1 check(s):
  1. divide_safe(10, 0) returned 'Error', expected 'Error: division by zero'

PR blocked — fix not ready
============================================================
```

---

## How to Interpret Results

- **PASS**: The fix is correct. All tests pass. The PR would be opened.
- **FAIL**: The fix is incomplete or broken. The PR is blocked. The implementer must fix the issues and resubmit.

---

## How to Tighten Reviewer Checks

To make the reviewer even stricter, you can:

1. Add more edge case tests (floats, very large numbers, string inputs)
2. Check that the function signature has not changed
3. Verify that no new imports were added
4. Check that the number of lines changed is minimal
5. Verify that no test logic was modified
6. Add type checking (e.g., ensure return type matches expectations)

---

## Why Isolation / Worktrees Matter

Without isolation, a bad fix could:

- Corrupt the production codebase
- Break other developers' work
- Introduce regressions that are hard to trace

With isolated branches:

- Each fix is self-contained
- The original code is always available for comparison
- Multiple fixes can be tested in parallel
- Bad fixes can be discarded without consequence

---

## Why Skills Are Separate from Code

Skills are instruction documents, not executable code. Separating them from application code means:

- The same skill can be reused for different implementations
- Skills can be version-controlled independently
- Agents can read and follow skills without modifying them
- Skills serve as living documentation of how bugs should be fixed
- Different agents (human or AI) can use the same skill consistently
