"""Integer factorisation and divisor enumeration.

Uses trial division up through ``sqrt(n)`` with a wheel after 5,
sufficient for the modest integers (up to ~10**12) targeted by this
library. Larger inputs work but are not the design point.
"""

from __future__ import annotations

from collections import Counter

from ._validate import require_positive_int


def _trial_division(target: int) -> list[int]:
    """Return prime factors of ``target`` by trial division.

    The caller guarantees ``target >= 2``.
    """
    factors: list[int] = []
    remainder = target
    for small in (2, 3):
        while remainder % small == 0:
            factors.append(small)
            remainder //= small
    candidate = 5
    step = 2
    while candidate * candidate <= remainder:
        while remainder % candidate == 0:
            factors.append(candidate)
            remainder //= candidate
        candidate += step
        step = 6 - step
    if remainder > 1:
        factors.append(remainder)
    return factors


def prime_factors(n: int) -> list[int]:
    """Return the prime factors of ``n`` with multiplicity, sorted ascending.

    ``prime_factors(12) == [2, 2, 3]``. ``prime_factors(1) == []``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    if target == 1:
        return []
    return _trial_division(target)


def factorise(n: int) -> dict[int, int]:
    """Return a ``{prime: exponent}`` mapping for ``n``.

    ``factorise(12) == {2: 2, 3: 1}``. ``factorise(1) == {}``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    return dict(Counter(prime_factors(n)))


def divisors(n: int) -> list[int]:
    """Return every positive divisor of ``n``, sorted ascending.

    ``divisors(12) == [1, 2, 3, 4, 6, 12]``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    target = require_positive_int("n", n)
    factor_map = factorise(target)
    result = [1]
    for prime, exponent in factor_map.items():
        power = 1
        new_chunk: list[int] = []
        for _ in range(exponent):
            power *= prime
            new_chunk.extend(existing * power for existing in result)
        result.extend(new_chunk)
    result.sort()
    return result
