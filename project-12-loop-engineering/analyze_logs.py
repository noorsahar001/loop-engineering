"""analyze_logs.py — The Dreaming Loop's Log Parser.

Reads the observability logs left behind by earlier projects, extracts
every failure, groups those failures by type, and counts occurrences.

Two log dialects are understood:

1. project-7 style schedule.log (Python `logging` format):
       <YYYY-MM-DD HH:MM:SS,mmm> - ERROR - FAILURE: <what failed>
       <YYYY-MM-DD HH:MM:SS,mmm> - ERROR - NEEDS HUMAN: <what to check>

2. project-8 style audit_<timestamp>.log:
       [<YYYY-MM-DD HH:MM:SS>] ERROR: <message>

A failure is a line that is marked as an error and matches one of the
recognised failure markers (FAILURE, NEEDS HUMAN, ERROR, REVIEW FAILED).

Everything is stdlib only. There are no external dependencies.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dialect 1:  2026-08-21 00:18:31,744 - ERROR - FAILURE: msg
DIALECT1 = re.compile(
    r"(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[,\s]\d+ - ERROR - "
    r"(?P<kind>FAILURE|NEEDS HUMAN):\s*(?P<msg>.*)"
)

# Dialect 2:  [2026-08-21 01:48:18] ERROR: msg
DIALECT2 = re.compile(
    r"\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"ERROR(?: |:)\s*(?P<kind>FAILURE|NEEDS HUMAN|REVIEW FAILED)?\s*:?\s*(?P<msg>.*)"
)

# Also catch plain review checkpoints like "REVIEW FAILED" and "BUDGET EXCEEDED"
PLAIN_ERROR = re.compile(
    r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+(?:\[?)\s*"
    r"(?P<kind>ERROR|FAILURE|REVIEW FAILED|BUDGET EXCEEDED|MONTHLY BUDGET|WEEKLY LIMIT)"
)

FAILURE_MARKERS = (
    "FAILURE",
    "NEEDS HUMAN",
    "REVIEW FAILED",
    "BUDGET EXCEEDED",
    "MONTHLY BUDGET",
    "WEEKLY LIMIT",
)


def _failure_type(line):
    """Return a stable failure-type key for a raw log line, or None."""
    lowered = line.lower()
    for marker in FAILURE_MARKERS:
        if marker.lower() in lowered:
            return marker
    return None


def parse_file(path):
    """Parse a single log file into a list of failure records.

    Returns: list of dicts:
        {"timestamp": str, "type": str, "message": str, "line": int}
    """
    records = []
    if not os.path.isfile(path):
        return records

    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for idx, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue

            m = DIALECT1.match(line) or DIALECT2.match(line)
            if m:
                ftype = _failure_type(line) or (m.group("kind") or "ERROR")
                records.append(
                    {
                        "timestamp": m.group("ts"),
                        "type": ftype,
                        "message": (m.group("msg") or line).strip(),
                        "line": idx,
                    }
                )
                continue

            # Bare error lines caught without a crafted prefix
            pm = PLAIN_ERROR.match(line)
            if pm:
                records.append(
                    {
                        "timestamp": pm.group("ts"),
                        "type": _failure_type(line) or "ERROR",
                        "message": line,
                        "line": idx,
                    }
                )

    return records


def analyze_logs(paths):
    """Parse multiple log files and aggregate failures.

    Returns an analysis dict:
        {
          "source": {...file -> failure tally...},
          "failure_types": {type -> count},
          "failures": [ {timestamp, source, type, message, line}, ... ],
          "total": N
        }
    """
    type_counter = Counter()
    source_counter = Counter()
    all_failures = []

    for path in paths:
        name = os.path.basename(path)
        records = parse_file(path)
        source_counter[name] += len(records)
        for rec in records:
            type_counter[rec["type"]] += 1
            all_failures.append(
                {
                    "source": name,
                    "timestamp": rec["timestamp"],
                    "type": rec["type"],
                    "message": rec["message"],
                    "line": rec["line"],
                }
            )

    # Sort failures chronologically (best effort) by timestamp string.
    all_failures.sort(key=lambda r: (r["timestamp"], r["source"], r["line"]))

    return {
        "source": dict(source_counter),
        "failure_types": dict(type_counter),
        "failures": all_failures,
        "total": len(all_failures),
    }


def format_report(analysis):
    """Render a human-readable report of the analysis."""
    lines = []
    lines.append("Failure Analysis Report")
    lines.append("=" * 60)
    lines.append("Total failures found: {0}".format(analysis["total"]))

    lines.append("\nFailures by source:")
    for src, count in sorted(analysis["source"].items()):
        lines.append("  {0}: {1}".format(src, count))

    lines.append("\nFailures by type:")
    for ftype, count in sorted(
        analysis["failure_types"].items(), key=lambda kv: (-kv[1], kv[0])
    ):
        lines.append("  {0}: {1}".format(ftype, count))

    lines.append("\nIndividual failure records:")
    if not analysis["failures"]:
        lines.append("  (none)")
    for f in analysis["failures"]:
        lines.append(
            "  [{0}] {1} ({2}:{3}) {4}".format(
                f["timestamp"], f["type"], f["source"], f["line"], f["message"]
            )
        )

    return "\n".join(lines)


def default_sources():
    """Resolve the log files the dreamer should read (Projects 3 and 8).

    Project 3 has no schedule.log, so we fall back to any *.log under the
    project folder. Project 8 writes per-run audit_<timestamp>.log files.

    Returns a list of absolute paths to log files that actually exist.
    """
    candidates = []
    for proj in ("project-3-loop-engineering", "project-8-loop-engineering"):
        proj_dir = os.path.join(os.path.dirname(BASE_DIR), proj)
        # Primary name
        for name in ("schedule.log", "cron.log"):
            p = os.path.join(proj_dir, name)
            if os.path.isfile(p):
                candidates.append(p)
        # Any audit log / *.log in the project folder
        if os.path.isdir(proj_dir):
            for f in sorted(os.listdir(proj_dir)):
                if f.lower().endswith(".log"):
                    p = os.path.join(proj_dir, f)
                    if os.path.isfile(p) and p not in candidates:
                        candidates.append(p)
    return candidates


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    explicit = [a for a in argv if not a.startswith("--")]

    if explicit:
        paths = explicit
    else:
        paths = default_sources()

    if not paths:
        print("No log files found to analyze.", file=sys.stderr)
        return 1

    analysis = analyze_logs(paths)
    report = format_report(analysis)

    if "--json" in argv:
        out = {
            "paths": paths,
            "analysis": analysis,
        }
        print(json.dumps(out, indent=2, default=str))
    else:
        print(report)
        print("\nSource paths:")
        for p in paths:
            print("  " + p)

    return 0


if __name__ == "__main__":
    sys.exit(main())
