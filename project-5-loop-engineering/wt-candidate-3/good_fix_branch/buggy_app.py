def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    return True

if __name__ == "__main__":
    result = validate_age(25)
    print(f"Validation passed: {result}")
