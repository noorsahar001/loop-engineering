import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='schedule.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_beat():
    """Execute one beat of the scheduled loop."""
    logging.info("=== BEAT STARTED ===")
    
    # Step 1: Read spine (progress.md)
    logging.info("Reading progress.md")
    try:
        with open('progress.md') as f:
            old_content = f.read()
        logging.info("progress.md read successfully")
    except FileNotFoundError:
        logging.error("FAILURE: progress.md not found!")
        logging.error("NEEDS HUMAN: Check if progress.md was deleted or missing")
        print("ERROR: progress.md not found! Check schedule.log for details.")
        exit(1)
    except Exception as e:
        logging.error(f"FAILURE: Unexpected error reading progress.md: {e}")
        logging.error("NEEDS HUMAN: Unknown error accessing spine file")
        print(f"ERROR: {e}. Check schedule.log for details.")
        exit(1)

    # Step 2: Gather data
    logging.info("Running gather.py")
    try:
        result = subprocess.run(
            ['python', 'gather.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        new_findings = result.stdout.strip()
        if result.returncode != 0:
            logging.error(f"FAILURE: gather.py failed with return code {result.returncode}")
            logging.error(f"STDERR: {result.stderr}")
            logging.error("NEEDS HUMAN: gather.py crashed during data collection")
            # Update spine with failure before exiting
            update_spine(old_content, "FAILED", "gather.py crashed", "None")
            print("ERROR: gather.py failed. Check schedule.log for details.")
            exit(1)
        logging.info(f"gather.py completed successfully, output length: {len(new_findings)} chars")
    except subprocess.TimeoutExpired:
        logging.error("FAILURE: gather.py timed out after 30 seconds")
        logging.error("NEEDS HUMAN: gather.py hung or is too slow")
        update_spine(old_content, "FAILED", "gather.py timed out", "None")
        print("ERROR: gather.py timed out. Check schedule.log for details.")
        exit(1)
    except FileNotFoundError:
        logging.error("FAILURE: gather.py not found!")
        logging.error("NEEDS HUMAN: gather.py was deleted or moved")
        update_spine(old_content, "FAILED", "gather.py not found", "None")
        print("ERROR: gather.py not found. Check schedule.log for details.")
        exit(1)

    # Step 3: Compare old vs new
    logging.info("Comparing old vs new findings")
    if new_findings in old_content:
        new_count = 0
        logging.info("No new findings since last beat")
    else:
        new_count = new_findings.count('\n') + 1
        logging.info(f"Found {new_count} new finding(s), updating spine")

    # Step 4: Update spine
    logging.info("Writing to progress.md")
    update_spine(old_content, "SUCCESS", new_findings, "None")
    logging.info("=== BEAT COMPLETED SUCCESSFULLY ===")
    print("SUCCESS: Beat completed. Check progress.md and schedule.log.")


def update_spine(old_content, status, new_findings, error):
    """Update progress.md with the latest beat info."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build the new latest beat section
    latest_beat = f"""## Latest Beat
- Timestamp: {timestamp}
- Status: {"SUCCESS" if status == "SUCCESS" else "FAILED"}
- Findings: {new_findings if status == "SUCCESS" else "0 new items"}
- Error: {error}
"""
    
    # Extract previous beats (everything after "## Previous Beats" and before "## Issues Log")
    if "## Previous Beats" in old_content:
        prev_section_start = old_content.index("## Previous Beats")
        issues_section_start = old_content.index("## Issues Log") if "## Issues Log" in old_content else len(old_content)
        previous_beats = old_content[prev_section_start:issues_section_start].strip()
    else:
        previous_beats = "## Previous Beats\n(no previous beats)"
        issues_section_start = old_content.index("## Issues Log") if "## Issues Log" in old_content else len(old_content)
    
    # Extract old latest beat and add it to previous beats
    if "## Latest Beat" in old_content:
        old_latest_start = old_content.index("## Latest Beat")
        old_latest = old_content[old_latest_start:prev_section_start].strip()
        if "(no beats yet)" not in old_latest:
            previous_beats += f"\n{old_latest}\n"
    
    # Extract issues log
    if "## Issues Log" in old_content:
        issues_log = old_content[issues_section_start:].strip()
    else:
        issues_log = "## Issues Log"
    
    # Add new issue if this was a failure
    if status == "FAILED":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        issues_log += f"\n- {timestamp} FAILED: {new_findings}"
    
    # Write it all back
    new_content = f"""# Progress Log

{latest_beat}
{previous_beats}

{issues_log}
"""
    
    with open('progress.md', 'w') as f:
        f.write(new_content)


if __name__ == "__main__":
    run_beat()
