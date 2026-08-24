# Project 10: Secrets Drill (A2 + A4 Lesson)

## What is A2 (The Environment)?

Environment variables: values passed to the process when it runs.

- Available in OpenCode environment panel
- Accessible via: `os.getenv('KEY_NAME')`
- NOT in Git, NOT gitignored (separate system)

## What is A4 (Secrets)?

Secrets: credentials, tokens, API keys.

- NEVER commit to Git
- NEVER rely on .gitignore'd files (cloud doesn't get them)
- ALWAYS put in environment variables

## The Drill: Deliberate Failure

### RUN 1 (WILL FAIL - Wrong Way):

Steps:

1. Token is in `.env` file (gitignored)
2. Routine tries to read `.env`
3. But routine runs in CLOUD, and gitignored files don't reach cloud
4. `.env` file missing → routine fails
5. Transcript shows: `✗ .env file not found`

### RUN 2 (WILL SUCCEED - Right Way):

Steps:

1. Move token from `.env` to environment-variables panel
2. Add prompt line: "Credentials are available as environment
   variables; do not look for a '.env' file."
3. Routine runs in cloud
4. Reads `os.getenv('API_TOKEN')`
5. Transcript shows: `✓ Found token in environment`

## Mechanical Reason RUN 1 Failed

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

## How to Reproduce Locally

A local run is misleading: `.env` exists on your machine, so the
wrong way *appears* to work. To rehearse honestly, simulate the cloud:

```bash
git clone <this-repo-url> cloud-sim
cd cloud-sim
python fetch_data.py          # RUN 1: fails — no .env in clone
API_TOKEN=... python fetch_data.py   # RUN 2: succeeds via env var
```

The clone contains exactly what GitHub contains — and GitHub never
received `.env`.
