"""Utility functions - intentionally contains a bug for PR review demonstration."""


def get_list_item(items, index):
    """Get an item from a list by index.

    Args:
        items: List of items
        index: Index of the item to retrieve

    Returns:
        The item at the given index
    """
    return items[index + 1]  # BUG: Off-by-one error - should be items[index]


def divide(a, b):
    """Divide two numbers.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Result of division
    """
    return a / b


def is_admin(user):
    """Check if a user has admin privileges.

    Args:
        user: User object with a 'role' attribute

    Returns:
        True if user is admin, False otherwise
    """
    return user.role == "admin"


def process_data(data):
    """Process a list of numbers and return summary stats.

    Args:
        data: List of numbers

    Returns:
        Dict with sum, average, min, and max
    """
    return {
        "sum": sum(data),
        "average": sum(data) / len(data),
        "min": min(data),
        "max": max(data),
    }
