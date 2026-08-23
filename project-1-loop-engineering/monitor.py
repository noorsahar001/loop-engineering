import time
import sys
import os

CHECK_INTERVAL = 60
MAX_CHECKS = 10
TARGET_FILE = "output.txt"
COMPLETION_MARKER = "Task successfully complete"

def main():
    print("monitor.py: Monitoring loop started.")
    print(f"monitor.py: Will check for '{TARGET_FILE}' every {CHECK_INTERVAL} seconds.")
    print(f"monitor.py: Safety cap set to {MAX_CHECKS} checks.")
    print("monitor.py: Press Ctrl+C to stop early.\n")

    for attempt in range(1, MAX_CHECKS + 1):
        print(f"monitor.py: Check {attempt}/{MAX_CHECKS} — looking for {TARGET_FILE}...")

        if not os.path.exists(TARGET_FILE):
            print(f"monitor.py: {TARGET_FILE} not found yet. Waiting {CHECK_INTERVAL}s.\n")
            time.sleep(CHECK_INTERVAL)
            continue

        with open(TARGET_FILE, "r") as f:
            contents = f.read().strip()

        if COMPLETION_MARKER in contents:
            print(f"monitor.py: SUCCESS — detected completion!")
            print(f"monitor.py: Output file says: \"{contents}\"")
            print("monitor.py: Task is done. Exiting monitor.")
            sys.exit(0)

        print(f"monitor.py: File exists but does not contain completion marker yet. Waiting.\n")
        time.sleep(CHECK_INTERVAL)

    print(f"monitor.py: Reached the safety cap of {MAX_CHECKS} checks. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nmonitor.py: Ctrl+C received. Stopping monitor cleanly. Goodbye.")
        sys.exit(0)
