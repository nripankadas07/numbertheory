"""GCD / LCM and the extended Euclidean algorithm."""

from __future__ import annotations

from ._validate import require_int


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of two integers.

    The result is always non-negative (``gcd(-6, 9) == 3``).
    ``gcd(0, 0)`` is defined as ``0``.

    Raises ``InvalidInputError`` if either argument is not an int.
    """
    first = require_int("a", a)
    second = require_int("b", b)
    while second:
        first, second = second, first % second
    return abs(first)


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of two integers.

    ``lcm(0, anything)`` is defined as ``0``. The result is always
    non-negative.

    Raises ``InvalidInputError`` if either argument is not an int.
    """
    first = require_int("a", a)
    second = require_int("b", b)
    if first == 0 or second == 0:
        return 0
    return abs(first // gcd(first, second) * second)


def gcd_extended(a: int, b: int) -> tuple[int, int, int]:
    """Return ``(g, x, y)`` with ``a*x + b*y == g`` and ``g == gcd(a, b)``.

    The returned ``g`` is always non-negative.

    Raises ``InvalidInputError`` if either argument is not an int.
    """
    require_int("a", a)
    require_int("b", b)
    old_g, current_g = a, b
    old_x, current_x = 1, 0
    old_y, current_y = 0, 1
    while current_g != 0:
        quotient = old_g // current_g
        old_g, current_g = current_g, old_g - quotient * current_g
        old_x, current_x = current_x, old_x - quotient * current_x
        old_y, current_y = current_y, old_y - quotient * current_y
    if old_g < 0:
        return -old_g, -old_x, -old_y
    return old_g, old_x, old_y
