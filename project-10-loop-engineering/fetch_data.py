"""Routine that needs a token to run"""

import os
import sys


def fetch_with_token():
    """Try to get token and use it"""

    # Try method 1: Look for .env file (WRONG way)
    print("Attempting to read .env file...")
    try:
        with open('.env') as f:
            for line in f:
                if line.startswith('API_TOKEN='):
                    token = line.split('=')[1].strip()
                    print(f"✓ Found token in .env: {token[:10]}...")
                    return 0
    except FileNotFoundError:
        print("✗ .env file not found (expected in cloud)")

    # Try method 2: Look in environment (RIGHT way)
    print("\nAttempting to read from environment variables...")
    token = os.getenv('API_TOKEN')
    if token:
        print(f"✓ Found token in environment: {token[:10]}...")
        print("✓ SUCCESS: Using token from environment")
        return 0
    else:
        print("✗ No token found in environment variables")
        print("NEEDS HUMAN: Set API_TOKEN in environment panel")
        return 1


if __name__ == '__main__':
    sys.exit(fetch_with_token())
