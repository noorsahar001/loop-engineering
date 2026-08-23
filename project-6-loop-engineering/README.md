# Project 6: Doorbell Loop - Event-Driven PR Review

**Concept 7: Event-Driven Loop | Concept 10: Connectors**

## What This Project Demonstrates

This project builds an **event-driven loop** that automatically reviews pull requests when GitHub events fire. No manual prompts, no polling, no timers — the loop reacts to external events.

---

## Core Concepts

### Concept 7: Event-Driven Loop
An event-driven loop **reacts to external events** rather than polling on a schedule or requiring manual intervention. Think of it like a doorbell: you don't check if someone's at the door every 5 minutes — the doorbell rings when someone arrives, and you react.

**Key difference from scheduled loops (Project 3):**
- Scheduled: "Check every 5 minutes"
- Event-driven: "React when this event fires"

### Concept 10: Connectors
Connectors **bridge OpenCode to external systems**. In this project, the GitHub webhook is the connector that bridges GitHub's pull request system to OpenCode's review capability.

**How it works:**
1. GitHub fires a webhook when a PR event occurs
2. The webhook triggers a GitHub Actions workflow
3. The workflow runs OpenCode with a review prompt
4. OpenCode reviews the code and comments on the PR

--- 
| **Project 6** | **Concept 7** | **Event-Driven** | **GitHub PR event** |

### Same Loop, Different Heartbeats
All four projects demonstrate the same fundamental concept: **a loop that wakes up and does something**. The difference is what triggers the wake-up:
- **In-Session**: Time-based polling
- **Conditional**: Data-based trigger
- **Scheduled**: Cron-based timer
- **Event-Driven**: External system event

---

- **The GitHub event IS the heartbeat**
- When a PR is opened → webhook fires → OpenCode runs automatically
- When new commits are pushed → synchronize event → OpenCode runs again
- **Zero manual intervention required**

---

## Project Structure

```
project-6-loop-engineering/
├── .opencode/
│   └── workflows/
│       └── review-pr.yml          # OpenCode workflow definition
├── .github/
│   └── workflows/
│       └── opencode.yml           # GitHub Actions workflow
├── buggy_code.py                  # Code with intentional bug
├── test_buggy_code.py             # Tests (some will fail)
└── README.md                      # This file
```

---

## The Event Flow

### EVENT 1: PR Opened
```
You push buggy code → GitHub fires "pull_request.opened" event
→ GitHub Actions workflow starts → OpenCode reviews code
→ OpenCode comments on PR with findings
```

### EVENT 2: PR Synchronized
```
You push a fix → GitHub fires "pull_request.synchronize" event
→ GitHub Actions workflow starts → OpenCode reviews updated code
→ OpenCode comments on PR confirming fix
```

---

## Setup Instructions

### Step 1: GitHub Integration
```bash
cd project-6-loop-engineering
opencode github install
```

This command:
- Generates `.github/workflows/opencode.yml` automatically
- Configures GitHub webhook to fire on PR events
- Sets up OpenCode to listen for PR triggers

### Step 2: Initialize Git Repository
```bash
git init
git checkout -b main
git add .
git commit -m "Initial commit: Project 6 setup"
```

### Step 3: Create Feature Branch with Bug
```bash
git checkout -b feature/buggy-code
# ... add buggy_code.py and test_buggy_code.py
git add .
git commit -m "Add utility functions with intentional bug"
git push -u origin feature/buggy-code
```

### Step 4: Open Pull Request
- Go to GitHub repository
- Create PR from `feature/buggy-code` to `main`
- **WATCH**: GitHub Actions tab — OpenCode runs automatically!

### Step 5: Observe EVENT 1
- PR opened event fires
- OpenCode reviews code
- Check PR comments for review findings

### Step 6: Push Fix (Trigger EVENT 2)
```bash
# Fix the bug in buggy_code.py
git add buggy_code.py
git commit -m "Fix off-by-one error in get_list_item"
git push
```
- Synchronize event fires
- OpenCode re-reviews automatically
- Check PR comments for updated review

---

## Demonstrating Event-Driven Behavior

### Before Starting
- What event-driven means: no scheduler, no manual prompt
- Why connectors matter: they bridge OpenCode to external systems
- How it differs from Project 3: fires on events, not time

### Run 1 (PR Opened)
- You open the PR with buggy code
- GitHub sends webhook event to OpenCode
- OpenCode automatically triggers review
- Review analyzes the code
- **Result**: Review finds (or misses) the planted bug

### Run 2 (PR Synchronized)
- You edit buggy_code.py (add more bugs or push fixes)
- Push new commit to same PR
- GitHub sends "synchronize" event
- OpenCode automatically re-triggers review
- **Result**: This re-fire proves the event heartbeat works

---

## What Happened (Demo Log)

```
EVENT 1: PR Opened
├── GitHub fired: pull_request.opened
├── Workflow started: Review Pull Request
├── OpenCode analyzed: buggy_code.py
├── Review result: Found off-by-one error in get_list_item()
└── PR comment posted automatically

EVENT 2: PR Synchronized
├── GitHub fired: pull_request.synchronize
├── Workflow started: Review Pull Request
├── OpenCode analyzed: buggy_code.py (updated)
├── Review result: Confirmed bug fix
└── PR comment posted automatically
```

---

## Key Takeaways

1. **Event-driven loops are reactive** — they respond to external events
2. **Connectors bridge systems** — GitHub webhooks connect GitHub to OpenCode
3. **No manual prompts needed** — the event IS the trigger
4. **Same loop pattern, different heartbeat** — Projects 1-6 all use loops
5. **Real-world applications**: CI/CD, automated testing, code review, monitoring

---

## Files

| File | Purpose |
|------|---------|
| `buggy_code.py` | Contains intentional off-by-one error |
| `test_buggy_code.py` | Tests that fail due to the bug |
| `.github/workflows/opencode.yml` | GitHub Actions workflow triggered by PR events |
| `.opencode/workflows/review-pr.yml` | OpenCode workflow definition for PR review |

---

## The Complete Heartbeat Journey

```
Project 6 (Concept 7): Event-Driven Heartbeat
  └── Event: "When PR opens, review it"
```

**Same loop. Different heartbeats. Different triggers. Same purpose: wake up and act.**
