---
name: skills
description: Instructions for safely fixing the divide-by-zero bug in buggy_app.py.
---

# Fix Bug Skill

## Bug Description

The function `divide_safe(a, b)` in `buggy_app.py` performs division without handling the case where `b` is zero. When `b == 0`, Python raises a `ZeroDivisionError` at runtime instead of returning a safe error message.

## Root Cause

The function performs `a / b` unconditionally. There is no guard clause or conditional check to prevent division by zero. This is a missing-input-validation bug.

## Fix Steps

1. Open `buggy_app.py`.
2. Locate the `divide_safe(a, b)` function.
3. Add a conditional check at the **beginning** of the function body, before the division:
   - If `b` is zero (`b == 0`), return the string `"Error: division by zero"`.
   - Otherwise, proceed with `return a / b`.
4. Do NOT modify the function signature.
5. Do NOT add any imports or external dependencies.
6. Do NOT change the behavior for non-zero values of `b`.

## Validation

After applying the fix, run these checks:

1. `divide_safe(10, 2)` must return `5.0`.
2. `divide_safe(10, 0)` must return the exact string `"Error: division by zero"`.
3. `divide_safe(10, 0)` must NOT raise `ZeroDivisionError`.
4. `divide_safe(0, 5)` must return `0.0`.
5. `divide_safe(-10, 2)` must return `-5.0`.

All five checks must pass for the fix to be considered correct.

## Expected Result

```python
def divide_safe(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b
```

## Important Constraints

- Keep the fix minimal — only add the guard clause.
- Do not refactor or rename anything.
- Do not add type hints, docstrings, or comments beyond what already exists.
- Do not change test logic or test expectations.
- The fix must be a pure behavior change inside the function body only.
