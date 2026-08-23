"""Tests for buggy_code.py - these tests will FAIL due to the planted bug."""

from buggy_code import get_list_item, divide, is_admin, process_data


class MockUser:
    """Mock user for testing."""

    def __init__(self, role):
        self.role = role


def test_get_list_item_first():
    """This test FAILS because of the off-by-one bug."""
    result = get_list_item([1, 2, 3], 0)
    assert result == 1, f"Expected 1 but got {result}"  # FAILS: returns 2


def test_get_list_item_second():
    """This test also FAILS because of the off-by-one bug."""
    result = get_list_item([1, 2, 3], 1)
    assert result == 2, f"Expected 2 but got {result}"  # FAILS: returns 3


def test_get_list_item_out_of_bounds():
    """This test FAILS with IndexError due to the off-by-one bug."""
    result = get_list_item([1, 2, 3], 2)
    assert result == 3  # FAILS: IndexError because index 3 is out of range


def test_divide_normal():
    """Test normal division - this passes."""
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    """Test division by zero - this raises ZeroDivisionError."""
    try:
        divide(10, 0)
        assert False, "Should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass


def test_is_admin():
    """Test admin check."""
    admin = MockUser("admin")
    user = MockUser("user")
    assert is_admin(admin) is True
    assert is_admin(user) is False


def test_process_data():
    """Test data processing."""
    result = process_data([1, 2, 3, 4, 5])
    assert result["sum"] == 15
    assert result["average"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 5
