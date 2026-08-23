# Project 1: A Watch Loop

A simple demonstration of an in-session monitoring loop. One Python script does
long work in the background while another script watches for a result file and
reports when the work is done.

---

## What This Project Does

1. `long_task.py` runs a simulated long task (90 seconds of sleep).
2. When the task finishes, it writes a completion message to `output.txt`.
3. `monitor.py` runs a loop that checks for `output.txt` once every minute.
4. The moment it detects the completion message, it prints a report and exits.

You never have to watch the terminal. The monitor does the watching for you.

---

## File Descriptions

| File             | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `long_task.py`   | Simulates a long-running task (sleeps 90s), then writes `output.txt`.   |
| `monitor.py`     | Polls for `output.txt` every 60 seconds, reports exactly once on success. |
| `output.txt`     | Created automatically by `long_task.py` when it finishes.               |
| `README.md`      | This file.                                                              |

---

## How the Loop Works

### The heartbeat

`monitor.py` runs a `for` loop that repeats up to 10 times (the safety cap).
Each iteration is one "heartbeat" — a single check cycle.

### The check

Each heartbeat does two things:

1. Checks if `output.txt` exists on disk.
2. If it exists, reads the file and looks for the string `"Task successfully complete"`.

If the file is missing or incomplete, the script prints a status line and sleeps
for 60 seconds before the next heartbeat.

### The stopping condition

The monitor stops in one of three ways:

- **Success**: It finds the completion marker in `output.txt`. It prints the
  result and exits with code 0.
- **Safety cap**: It reaches 10 checks without finding the marker. It prints a
  warning and exits with code 1. This prevents infinite looping if something
  goes wrong.
- **Ctrl+C**: You press Ctrl+C at any time. The script catches the interrupt,
  prints a clean goodbye, and exits with code 0.

---

## How to Run This Project

Open a terminal and navigate to the `project-1-loop-engineering/` folder.

### Step 1: Start the long task in the background

```bash
python long_task.py &
```

The `&` sends it to the background so your terminal stays free.

On Windows PowerShell, if `&` does not work, open a second terminal tab instead
and run `python long_task.py` there.

### Step 2: Start the monitor

```bash
python monitor.py
```

The monitor will begin its loop, checking once every 60 seconds.

---

## How to Stop It Cleanly

- Press **Ctrl+C** at any time while `monitor.py` is running.
- The script will print `Ctrl+C received. Stopping monitor cleanly. Goodbye.`
  and exit immediately.

You can also stop `long_task.py` the same way, or let it finish on its own.

---

## How to Know the Task Succeeded

You will see this output from `monitor.py`:

```
monitor.py: SUCCESS — detected completion!
monitor.py: Output file says: "Task successfully complete at 2026-08-18 14:30:00"
monitor.py: Task is done. Exiting monitor.
```

You can also verify manually by reading `output.txt`:

```bash
cat output.txt
```

It will contain a line like:

```
Task successfully complete at 2026-08-18 14:30:00
```
