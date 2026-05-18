"""Primality testing and prime enumeration.

``is_prime`` uses a deterministic Miller-Rabin test that is exact for
all 64-bit integers (and well beyond — the chosen witness set is
deterministic for ``n < 3.317 * 10**24``).
"""

from __future__ import annotations

from ._validate import require_int, require_positive_int

# Witness set proven deterministic for n < 3.317 * 10**24.
# Reference: Sorenson and Webster, 2017 — extends the 7-witness
# 64-bit-deterministic set to a 12-witness 81-bit-deterministic set.
_MILLER_RABIN_WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _miller_rabin_round(witness: int, candidate: int, exponent: int, twos: int) -> bool:
    """Return True if ``candidate`` passes one Miller-Rabin round."""
    state = pow(witness, exponent, candidate)
    if state == 1 or state == candidate - 1:
        return True
    for _ in range(twos - 1):
        state = (state * state) % candidate
        if state == candidate - 1:
            return True
    return False


def is_prime(n: int) -> bool:
    """Return whether ``n`` is prime.

    Negative integers, ``0`` and ``1`` are not prime. Uses a
    deterministic Miller-Rabin test that is exact for every ``n``
    used in practice.

    Raises ``InvalidInputError`` if ``n`` is not an int.
    """
    candidate = require_int("n", n)
    if candidate < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if candidate == prime:
            return True
        if candidate % prime == 0:
            return False
    exponent = candidate - 1
    twos = 0
    while exponent % 2 == 0:
        exponent //= 2
        twos += 1
    # Past the small-prime sieve, candidate is necessarily > 37, so
    # every Miller-Rabin witness in the table is strictly smaller.
    for witness in _MILLER_RABIN_WITNESSES:
        if not _miller_rabin_round(witness, candidate, exponent, twos):
            return False
    return True


def next_prime(n: int) -> int:
    """Return the smallest prime strictly greater than ``n``.

    Raises ``InvalidInputError`` if ``n`` is not an int.
    """
    candidate = require_int("n", n)
    if candidate < 2:
        return 2
    # n >= 2 here, so candidate = n + 1 >= 3; bump even values up by 1
    # to start the search on an odd number.
    candidate += 1
    if candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def prev_prime(n: int) -> int | None:
    """Return the largest prime strictly less than ``n``, or ``None``.

    Returns ``None`` when no such prime exists (``n <= 2``).

    Raises ``InvalidInputError`` if ``n`` is not an int.
    """
    candidate = require_int("n", n)
    if candidate <= 2:
        return None
    if candidate == 3:
        return 2
    candidate -= 1
    if candidate % 2 == 0:
        candidate -= 1
    while candidate >= 2 and not is_prime(candidate):
        candidate -= 2
    return candidate if candidate >= 2 else None


def primes_up_to(n: int) -> list[int]:
    """Return all primes ``p`` with ``2 <= p <= n`` via Sieve of Eratosthenes.

    Returns an empty list when ``n < 2``.

    Raises ``InvalidInputError`` if ``n`` is not an int.
    """
    upper = require_int("n", n)
    if upper < 2:
        return []
    sieve = bytearray(b"\x01") * (upper + 1)
    sieve[0] = 0
    sieve[1] = 0
    for index in range(2, int(upper**0.5) + 1):
        if sieve[index]:
            sieve[index * index : upper + 1 : index] = bytearray(
                len(range(index * index, upper + 1, index))
            )
    return [index for index, flag in enumerate(sieve) if flag]


def nth_prime(n: int) -> int:
    """Return the ``n``-th prime (1-indexed).

    ``nth_prime(1) == 2``.

    Raises ``InvalidInputError`` if ``n < 1`` or is not an int.
    """
    index = require_positive_int("n", n)
    candidate = 1
    found = 0
    while found < index:
        candidate = next_prime(candidate)
        found += 1
    return candidate
