def count_range(start, end):
    return list(range(start, end + 1))

if __name__ == "__main__":
    numbers = count_range(1, 5)
    print(f"Numbers: {numbers}")
