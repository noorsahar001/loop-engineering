#!/usr/bin/env python3
"""Budget state updater - tracks usage across runs"""

import json
import sys
from datetime import datetime, timedelta

STATE_FILE = 'budget_state.json'

def update_budget(tokens_used, monthly_cost, runs_this_week):
    """Update budget state"""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if 'week_start' not in state or datetime.fromisoformat(state['week_start']) < week_start:
        state['runs_this_week'] = 0
        state['week_start'] = week_start.isoformat()
    
    state['tokens_used'] = tokens_used + 1500
    state['monthly_cost'] = monthly_cost + 0.005
    state['runs_this_week'] = runs_this_week + 1
    state['last_run'] = now.isoformat()
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"Budget updated: tokens={state['tokens_used']}, cost=${state['monthly_cost']:.3f}, runs={state['runs_this_week']}")

if __name__ == '__main__':
    tokens = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    cost = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    runs = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    update_budget(tokens, cost, runs)
