import subprocess
import sys

def measure_one_beat():
    """Measure token usage for one beat (one run of gather.py)."""
    print("=== Measuring cost of one beat ===\n")
    
    # Run gather.py once
    result = subprocess.run(
        [sys.executable, 'gather.py'],
        capture_output=True,
        text=True
    )
    
    stdout = result.stdout
    stderr = result.stderr
    
    # Rough token estimation: ~4 chars per token
    input_tokens = len(stdout) // 4 if stdout else 0
    output_tokens = len(stderr) // 4 if stderr else 0
    total_tokens = input_tokens + output_tokens
    
    print(f"One beat (gather.py run) produces:")
    print(f"  Output length: {len(stdout)} chars -> ~{input_tokens} tokens")
    print(f"  Stderr length: {len(stderr)} chars -> ~{output_tokens} tokens")
    print(f"  Total estimated tokens: ~{total_tokens}")
    
    # Pricing (Claude Sonnet approximate rates)
    cost_per_1k_input = 0.003
    cost_per_1k_output = 0.015
    
    # Monthly cost calculation
    cadence = 24  # runs per day (every hour)
    days = 30
    total_beats = cadence * days
    
    monthly_input_cost = (input_tokens * total_beats * cost_per_1k_input) / 1000
    monthly_output_cost = (output_tokens * total_beats * cost_per_1k_output) / 1000
    monthly_total = monthly_input_cost + monthly_output_cost
    
    print(f"\n=== Monthly Cost Projection ===")
    print(f"Cadence: {cadence} beats/day")
    print(f"Total beats per month: {total_beats}")
    print(f"\nClaude Sonnet rates:")
    print(f"  Input:  ${cost_per_1k_input}/1K tokens")
    print(f"  Output: ${cost_per_1k_output}/1K tokens")
    print(f"\nEstimated monthly cost:")
    print(f"  Input tokens:  ${monthly_input_cost:.4f}")
    print(f"  Output tokens: ${monthly_output_cost:.4f}")
    print(f"  TOTAL:         ${monthly_total:.4f}")
    
    return total_tokens, monthly_total

if __name__ == "__main__":
    tokens, cost = measure_one_beat()
