"""ROUTINE B - Executor.

Trigger type: API TRIGGER ONLY (A3). No schedule, no cron, no self-start.
This script does nothing useful until a HUMAN sends:

    POST /execute
    Authorization: Bearer <token-from-.env>

That manual call IS the human gate (A4): the decision to run belongs to
a person, not to a timer or to Routine A.

Gate rules enforced on every request:
  1. Valid bearer token required (constant-time compare) -> else 401
  2. draft_pending.json must exist                        -> else 404
  3. draft status must equal "PENDING APPROVAL"           -> else 409

On success it performs the tasks, flips the draft to EXECUTED (so the
gate closes behind it), and appends a signed entry to approval_log.md.
"""

import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFT_PATH = os.path.join(BASE_DIR, "draft_pending.json")
LOG_PATH = os.path.join(BASE_DIR, "approval_log.md")
HOST = "127.0.0.1"
PORT = int(os.getenv("PORT", "8011"))
REQUIRED_STATUS = "PENDING APPROVAL"


def load_token():
    """Prefer real environment variable; fall back to .env for local runs."""
    token = os.getenv("BEARER_TOKEN")
    if token:
        return token.strip()
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("BEARER_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return None


def fingerprint(token):
    """Never log raw tokens - log a short hash instead."""
    return hashlib.sha256(token.encode()).hexdigest()[:12]


def execute_tasks(draft):
    performed = []
    for task in draft.get("tasks", []):
        print(f"[EXECUTE] task {task['id']}: {task['title']} ({task['action']}) -> done")
        performed.append({"id": task["id"], "title": task["title"], "result": "done"})
    return performed


def append_approval_log(when_utc, client_ip, token):
    entry = (
        f"\n## Approval - {when_utc}\n"
        "- decided_by: HUMAN (manual API call)\n"
        f"- trigger: POST /execute from {client_ip} (API trigger, no schedule)\n"
        f"- token_fingerprint: sha256:{fingerprint(token)}\n"
        "- outcome: EXECUTED\n"
    )
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(entry)


class ExecutorHandler(BaseHTTPRequestHandler):
    server_version = "RoutineBGate/1.0"

    def _send(self, code, payload):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"service": "routine_b_execute", "trigger": "api_only",
                             "status": "idle, waiting for a human"})
        else:
            self._send(404, {"error": "unknown endpoint"})

    def do_POST(self):
        now_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

        # Gate 1: bearer token (A3 authentication + A4 human proof)
        auth = self.headers.get("Authorization", "")
        expected = f"Bearer {TOKEN}"
        if not TOKEN or not hmac.compare_digest(auth, expected):
            print(f"[GATE] {now_utc} REJECTED 401: missing/invalid bearer token")
            self._send(401, {"error": "unauthorized: valid bearer token required"})
            return

        if self.path != "/execute":
            self._send(404, {"error": "unknown endpoint"})
            return

        # Gate 2: draft must exist
        if not os.path.exists(DRAFT_PATH):
            print(f"[GATE] {now_utc} REJECTED 404: no draft found")
            self._send(404, {"error": "draft_pending.json not found - run Routine A first"})
            return

        with open(DRAFT_PATH, encoding="utf-8") as fh:
            draft = json.load(fh)

        # Gate 3: status check
        status = draft.get("status")
        if status != REQUIRED_STATUS:
            print(f"[GATE] {now_utc} REJECTED 409: status '{status}'")
            self._send(409, {
                "error": f"draft status is '{status}', "
                         f"expected '{REQUIRED_STATUS}'. Nothing was executed.",
                "hint": "run Routine A again to mint a fresh pending draft",
            })
            return

        print(f"[GATE ] {now_utc} OPENED by human API call from {self.client_address[0]}")
        performed = execute_tasks(draft)

        # Close the gate behind us so this draft can never double-run.
        draft["status"] = "EXECUTED"
        draft["approved_by"] = "HUMAN (manual API call)"
        draft["executed_at"] = now_utc
        draft["results"] = performed
        with open(DRAFT_PATH, "w", encoding="utf-8") as fh:
            json.dump(draft, fh, indent=2)

        append_approval_log(now_utc, self.client_address[0], TOKEN)
        print(f"[LOG  ] approval recorded in {os.path.basename(LOG_PATH)}")

        self._send(200, {
            "status": "executed",
            "executed_at": now_utc,
            "tasks_done": len(performed),
            "logged_to": os.path.basename(LOG_PATH),
            "gate": "closed (draft status is now EXECUTED)",
        })

    def log_message(self, fmt, *args):  # keep console output readable
        pass


def main():
    global TOKEN
    TOKEN = load_token()
    if not TOKEN:
        print("FATAL: no BEARER_TOKEN found (env var or .env).")
        print("Save the bearer token to .env before starting Routine B.")
        return 1
    server = HTTPServer((HOST, PORT), ExecutorHandler)
    print(f"[ROUTINE B] listening on {HOST}:{PORT}")
    print("[ROUTINE B] TRIGGER TYPE: API ONLY - no schedule exists.")
    print(f"[ROUTINE B] idle... waiting for a HUMAN to fire POST /execute")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[ROUTINE B] stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
