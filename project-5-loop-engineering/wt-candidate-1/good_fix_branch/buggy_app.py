def safe_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    result = safe_divide(10, 2)
    print(f"Result: {result}")
