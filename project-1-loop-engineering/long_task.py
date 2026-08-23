import time
import datetime

def main():
    print("long_task.py: Starting simulated work...")
    print("long_task.py: Sleeping for 90 seconds to simulate a long task.")

    time.sleep(90)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Task successfully complete at {timestamp}"

    # TODO: add error handling for file write
    with open("output.txt", "w") as f:
        f.write(message)

    print(f"long_task.py: Done. Wrote '{message}' to output.txt")

if __name__ == "__main__":
    main()
