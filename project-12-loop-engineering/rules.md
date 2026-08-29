# Rules — the Dreaming Loop's Current Rule Set

These are the rules the Dreaming Loop is allowed to *propose changes to*.
The loop never edits this file directly — it proposes rule changes as a
pull request, and a human approves the merge (Part 5: Human Gate).

Each rule has an ID, a name, the file it governs, and a description of
the behaviour it prescribes. Evidence from real logs (dates + counts +
line references) must back any proposed change.

---

## Rule 1: Dependency Audit

- **ID:** `R1-DEP`
- **Governs:** `project-8-loop-engineering` audit findings
- **Rule:** Every loop beat must run a dependency audit that reports
  outdated or vulnerable packages, and must surface the result in the
  spine (`audit_progress.md`).
- **Proposal hook:** If repeated failures show the audit cannot complete
  (missing lockfile, broken package manager), the loop may propose
  broadening the audit scope.

## Rule 2: Test Coverage

- **ID:** `R2-TEST`
- **Governs:** every loop project with a test suite
- **Rule:** Each commit must not reduce the previously recorded test
  pass rate; a failing test must be fixed in the same beat that finds it.
- **Proposal hook:** If a test fails repeatedly across beats without
  being fixed, the loop may propose raising a guard that blocks the loop
  from continuing until the test passes.

## Rule 3: Documentation Freshness

- **ID:** `R3-DOC`
- **Governs:** `README.md` and `*.md` spines in each project
- **Rule:** Any time a behaviour changes, the documentation describing
  that behaviour must be updated in the same pull request.
- **Proposal hook:** If documentation is found to contradict implemented
  behaviour during review, the loop may propose a freshness check that
  flags stale docs as an error in the log.

## Rule 4: Commit Frequency

- **ID:** `R4-COMMIT`
- **Governs:** the git history of the whole workspace
- **Rule:** Work is committed in small, single-purpose commits; a
  long-running loop must checkpoint its state at least once per beat.
- **Proposal hook:** If a beat runs for a long time with no commit
  checkpoint, the loop may propose splitting large work into smaller
  mandatory checkpoints.

---

## How rules can change

1. The Dreaming Loop analyses the real logs (Project 3 / Project 8).
2. If a failure type repeats enough times, the loop drafts a **proposed
   rule change** citing the evidence (dates, counts, log lines).
3. The change is prepared as a git branch + commit (never a direct
   commit to `main`).
4. A pull request is opened for the change.
5. A **human** reviews and approves the merge. The loop only proposes —
   it never decides and never merges its own change.

---

_Edits to this file must go through a pull request._ Status: current as
of the last merge.
