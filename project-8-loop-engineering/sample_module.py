#!/usr/bin/env python3
"""Sample module with TODO comments for testing"""

import os

def process_data(data):
    # TODO: Add input validation
    result = []
    for item in data:
        # FIXME: Handle None values
        result.append(item * 2)
    return result

def save_results(results, filename):
    # TODO: Add error handling
    with open(filename, 'w') as f:
        f.write(str(results))

def load_config():
    # HACK: Hardcoded path for now
    config_path = "/etc/app/config.json"
    # TODO: Make configurable
    if os.path.exists(config_path):
        return config_path
    return None

# XXX: This function needs refactoring
def old_function():
    pass
