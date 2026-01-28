"""Unit tests for utils/math.py."""

import pytest

from utils.math import factorial, fibonacci


class TestFactorial:
    """Tests for the factorial function."""

    def test_factorial_zero(self):
        """factorial(0) should return 1."""
        assert factorial(0) == 1

    def test_factorial_one(self):
        """factorial(1) should return 1."""
        assert factorial(1) == 1

    def test_factorial_small_numbers(self):
        """Test factorial for small positive integers."""
        assert factorial(2) == 2
        assert factorial(3) == 6
        assert factorial(4) == 24
        assert factorial(5) == 120

    def test_factorial_larger_number(self):
        """Test factorial for a larger number."""
        assert factorial(10) == 3628800

    def test_factorial_negative_raises_value_error(self):
        """factorial of negative numbers should raise ValueError."""
        with pytest.raises(ValueError, match="not defined for negative"):
            factorial(-1)
        with pytest.raises(ValueError):
            factorial(-5)

    def test_factorial_float_raises_type_error(self):
        """factorial of float should raise TypeError."""
        with pytest.raises(TypeError, match="requires an integer"):
            factorial(3.5)

    def test_factorial_string_raises_type_error(self):
        """factorial of string should raise TypeError."""
        with pytest.raises(TypeError, match="requires an integer"):
            factorial("5")

    def test_factorial_none_raises_type_error(self):
        """factorial of None should raise TypeError."""
        with pytest.raises(TypeError):
            factorial(None)

    def test_factorial_bool_accepted(self):
        """bool is a subclass of int in Python, so should work."""
        # True == 1, False == 0
        assert factorial(True) == 1
        assert factorial(False) == 1


class TestFibonacci:
    """Tests for the fibonacci function."""

    def test_fibonacci_zero(self):
        """fibonacci(0) should return 0."""
        assert fibonacci(0) == 0

    def test_fibonacci_one(self):
        """fibonacci(1) should return 1."""
        assert fibonacci(1) == 1

    def test_fibonacci_sequence(self):
        """Test the first several Fibonacci numbers."""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, val in enumerate(expected):
            assert fibonacci(i) == val

    def test_fibonacci_larger_number(self):
        """Test fibonacci for a larger index."""
        assert fibonacci(20) == 6765
        assert fibonacci(30) == 832040

    def test_fibonacci_negative_raises_value_error(self):
        """fibonacci of negative numbers should raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            fibonacci(-1)
        with pytest.raises(ValueError):
            fibonacci(-10)

    def test_fibonacci_float_raises_type_error(self):
        """fibonacci of float should raise TypeError due to range()."""
        with pytest.raises(TypeError):
            fibonacci(3.5)

    def test_fibonacci_string_raises_type_error(self):
        """fibonacci of string should raise TypeError."""
        with pytest.raises(TypeError):
            fibonacci("5")
