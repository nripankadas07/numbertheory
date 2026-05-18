"""Legendre and Jacobi symbols.

Both routines are computed by the standard reciprocity-driven loop —
no factorisation required. They run in ``O(log min(a, n))`` time.
"""

from __future__ import annotations

from ._errors import InvalidInputError
from ._primality import is_prime
from ._validate import require_int


def jacobi_symbol(a: int, n: int) -> int:
    """Return the Jacobi symbol ``(a / n)``: one of ``-1``, ``0``, ``+1``.

    The denominator ``n`` must be a positive odd integer. The Jacobi
    symbol generalises the Legendre symbol to composite odd ``n``.

    Raises ``InvalidInputError`` if ``n`` is not a positive odd int,
    or if either argument is not an int.
    """
    numerator = require_int("a", a)
    denominator = require_int("n", n)
    if denominator < 1 or denominator % 2 == 0:
        raise InvalidInputError(
            f"n must be a positive odd int, got {denominator}"
        )
    numerator %= denominator
    result = 1
    while numerator != 0:
        while numerator % 2 == 0:
            numerator //= 2
            residue = denominator % 8
            if residue == 3 or residue == 5:
                result = -result
        numerator, denominator = denominator, numerator
        if numerator % 4 == 3 and denominator % 4 == 3:
            result = -result
        numerator %= denominator
    if denominator == 1:
        return result
    return 0


def legendre_symbol(a: int, p: int) -> int:
    """Return the Legendre symbol ``(a / p)`` for an odd prime ``p``.

    The result is ``-1`` if ``a`` is a non-residue mod ``p``, ``0``
    if ``p`` divides ``a``, and ``+1`` if ``a`` is a quadratic residue.

    Raises ``InvalidInputError`` if ``p`` is not an odd prime, or if
    either argument is not an int.
    """
    require_int("a", a)
    prime = require_int("p", p)
    if prime < 3 or prime % 2 == 0 or not is_prime(prime):
        raise InvalidInputError(
            f"p must be an odd prime, got {prime}"
        )
    return jacobi_symbol(a, prime)
