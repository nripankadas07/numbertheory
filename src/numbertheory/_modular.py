"""Modular arithmetic: inverse, exponentiation, Chinese Remainder."""

from __future__ import annotations

from collections.abc import Sequence

from ._errors import InvalidInputError, NoSolutionError
from ._gcd import gcd_extended
from ._validate import require_int, require_modulus


def mod_inverse(a: int, modulus: int) -> int:
    """Return the modular multiplicative inverse of ``a`` modulo ``modulus``.

    The inverse is the unique integer ``x`` in ``[0, modulus)`` such
    that ``(a * x) % modulus == 1``.

    Raises ``InvalidInputError`` if ``modulus < 2`` or arguments are
    not ints. Raises ``NoSolutionError`` if ``gcd(a, modulus) != 1``.
    """
    integer = require_int("a", a)
    base = require_modulus("modulus", modulus)
    common, x_coeff, _ = gcd_extended(integer, base)
    if common != 1:
        raise NoSolutionError(
            f"{integer} has no inverse modulo {base} (gcd is {common})"
        )
    return x_coeff % base


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Return ``(base ** exponent) % modulus``.

    Negative exponents are supported when ``base`` is coprime to
    ``modulus``; the result is the inverse raised to the absolute
    value of the exponent.

    Raises ``InvalidInputError`` if ``modulus < 2`` or arguments are
    not ints. Raises ``NoSolutionError`` if ``exponent < 0`` and
    ``base`` is not coprime to ``modulus``.
    """
    base_int = require_int("base", base)
    exponent_int = require_int("exponent", exponent)
    modulus_int = require_modulus("modulus", modulus)
    if exponent_int < 0:
        inverse = mod_inverse(base_int, modulus_int)
        return pow(inverse, -exponent_int, modulus_int)
    return pow(base_int, exponent_int, modulus_int)


def _crt_pair(
    remainder_a: int,
    modulus_a: int,
    remainder_b: int,
    modulus_b: int,
) -> tuple[int, int]:
    """Combine two ``(remainder, modulus)`` pairs into one.

    Returns ``(x, lcm)`` where ``x % modulus_a == remainder_a`` and
    ``x % modulus_b == remainder_b``. Raises ``NoSolutionError`` if
    the constraints are inconsistent on the gcd of the two moduli.
    """
    common, multiplier_a, _ = gcd_extended(modulus_a, modulus_b)
    difference = remainder_b - remainder_a
    if difference % common != 0:
        raise NoSolutionError(
            "remainders are inconsistent on the moduli's gcd"
        )
    step = modulus_b // common
    offset = (multiplier_a * (difference // common)) % step
    combined_modulus = modulus_a // common * modulus_b
    combined = (remainder_a + modulus_a * offset) % combined_modulus
    return combined, combined_modulus


def _normalised_pair(
    label: str,
    index: int,
    remainders: Sequence[int],
    moduli: Sequence[int],
) -> tuple[int, int]:
    """Validate and normalise the ``index``-th congruence pair."""
    modulus = require_modulus(f"{label}[{index}]:modulus", moduli[index])
    remainder = require_int(f"{label}[{index}]:remainder", remainders[index])
    return remainder % modulus, modulus


def _validate_crt_input(
    remainders: Sequence[int],
    moduli: Sequence[int],
) -> None:
    """Reject mismatched-length and empty CRT inputs."""
    if len(remainders) != len(moduli):
        raise InvalidInputError(
            "remainders and moduli must have the same length"
        )
    if len(remainders) == 0:
        raise InvalidInputError("at least one congruence is required")


def chinese_remainder(
    remainders: Sequence[int],
    moduli: Sequence[int],
) -> tuple[int, int]:
    """Solve a system of simultaneous congruences via CRT.

    Returns ``(x, M)`` such that ``x % m_i == r_i`` for every pair
    ``(r_i, m_i)`` in the input, with ``0 <= x < M``. Inconsistent
    systems raise ``NoSolutionError``; bad input raises
    ``InvalidInputError``.
    """
    _validate_crt_input(remainders, moduli)
    current_remainder, current_modulus = _normalised_pair(
        "crt", 0, remainders, moduli,
    )
    for index in range(1, len(remainders)):
        next_remainder, next_modulus = _normalised_pair(
            "crt", index, remainders, moduli,
        )
        current_remainder, current_modulus = _crt_pair(
            current_remainder, current_modulus,
            next_remainder, next_modulus,
        )
    return current_remainder, current_modulus
