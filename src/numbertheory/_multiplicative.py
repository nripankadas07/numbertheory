"""Multiplicative functions: divisor count/sum, Euler phi, Mobius."""

from __future__ import annotations

from ._factor import factorise
from ._validate import require_positive_int


def divisor_count(n: int) -> int:
    """Return the number of positive divisors of ``n``.

    ``divisor_count(12) == 6``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    factor_map = factorise(target)
    count = 1
    for exponent in factor_map.values():
        count *= exponent + 1
    return count


def divisor_sum(n: int) -> int:
    """Return the sum of every positive divisor of ``n``.

    ``divisor_sum(12) == 1+2+3+4+6+12 == 28``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    factor_map = factorise(target)
    total = 1
    for prime, exponent in factor_map.items():
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def euler_phi(n: int) -> int:
    """Return Euler's totient function: ``|{k : 1 <= k <= n, gcd(k,n)==1}|``.

    ``euler_phi(1) == 1``. ``euler_phi(p) == p - 1`` for prime ``p``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    if target == 1:
        return 1
    factor_map = factorise(target)
    total = target
    for prime in factor_map:
        total = total // prime * (prime - 1)
    return total


def mobius(n: int) -> int:
    """Return the Mobius function: ``-1``, ``0``, or ``+1``.

    ``mobius(1) == 1``. Returns ``0`` if ``n`` is divisible by any
    squared prime; otherwise returns ``(-1) ** k`` where ``k`` is the
    number of distinct prime factors.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    if target == 1:
        return 1
    factor_map = factorise(target)
    for exponent in factor_map.values():
        if exponent >= 2:
            return 0
    return -1 if len(factor_map) % 2 else 1
