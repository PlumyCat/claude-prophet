"""Math utility functions."""


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        The factorial of n (n!).

    Raises:
        ValueError: If n is negative.
        TypeError: If n is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError(f"factorial requires an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number.

    Args:
        n: The index in the Fibonacci sequence (0-indexed).
           fibonacci(0) = 0, fibonacci(1) = 1, fibonacci(2) = 1, etc.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
