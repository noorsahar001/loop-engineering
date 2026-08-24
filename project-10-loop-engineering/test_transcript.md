# Transcript Comparison — Secrets Drill

Environment used for both runs: a fresh `git clone` of this repository
(`p10-cloud-sim`). A clone contains **exactly what GitHub contains** —
and `.env` is gitignored, so it is physically absent there.

---

## RUN 0 (bonus) — Same script, run LOCALLY where `.env` exists

```
Attempting to read .env file...
✓ Found token in .env: dummy_toke...
EXIT CODE: 0
```

This is the trap: on your machine the wrong way looks like it works.
Nothing failed here — which is precisely why the bug ships.

---

## RUN 1 - WRONG (Token in .env, gitignored)

Location of token: `.env` file → committed? NO → pushed? NO → in cloud clone? NO

```
Attempting to read .env file...
✗ .env file not found (expected in cloud)

Attempting to read from environment variables...
✗ No token found in environment variables
NEEDS HUMAN: Set API_TOKEN in environment panel
EXIT CODE: 1
```

- Status: GREEN (no crash, clean transcript)
- Outcome: FAILED — no token found, routine cannot do its job
- Root cause: gitignored files never reach GitHub; the cloud clone was
  built from GitHub; therefore `.env` does not exist where the routine runs

---

## RUN 2 - RIGHT (Token moved to environment variables)

Change made:
1. `API_TOKEN = dummy_token_12345_for_testing_only` added to the
   environment panel (injected into the process at launch)
2. Routine prompt updated:
   > Credentials are available as environment variables;
   > do not look for a '.env' file.

Same cloud clone, still no `.env` present:

```
Attempting to read .env file...
✗ .env file not found (expected in cloud)

Attempting to read from environment variables...
✓ Found token in environment: dummy_toke...
✓ SUCCESS: Using token from environment
EXIT CODE: 0
```

- Status: GREEN
- Outcome: SUCCESS — `os.getenv('API_TOKEN')` delivered the secret

---

## Side-by-side

|                    | RUN 1                          | RUN 2                       |
|--------------------|--------------------------------|-----------------------------|
| Token location     | `.env` file (local only)       | Environment variable        |
| Committed to Git?  | NO (gitignored)                | N/A (separate system from Git) |
| In cloud clone?    | NO                             | YES (passed to process)     |
| Script exit code   | 1                              | 0                           |
| Status / Outcome   | GREEN / FAILED                 | GREEN / SUCCESS             |

## Mechanical Reason

```
.env file on your machine:
- Committed?              NO  (gitignored)
- Reached GitHub?         NO  (gitignored files excluded)
- In cloud clone?         NO  (never left local machine)
- Available to routine?   NO  (file not present)
→ FAILURE

Environment variables:
- Set in OpenCode panel?       YES
- Part of Git?                 NO  (separate system)
- Passed to cloud process?     YES
- Available via os.getenv()?   YES
→ SUCCESS
```

Lesson locked in: **gitignored files never reach the cloud, so anything
the routine needs must travel by another channel — the environment.**
