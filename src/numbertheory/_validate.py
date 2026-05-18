"""Argument-validation helpers shared by every public function."""

from __future__ import annotations

from ._errors import InvalidInputError


def require_int(name: str, value: object) -> int:
    """Return ``value`` if it is a true ``int`` (not ``bool``).

    Python's ``bool`` is an ``int`` subclass; we reject it so callers
    cannot accidentally pass ``True`` / ``False`` as a number.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidInputError(
            f"{name} must be an int, got {type(value).__name__}"
        )
    return value


def require_positive_int(name: str, value: object) -> int:
    """Return ``value`` if it is a positive (``>= 1``) ``int``."""
    integer = require_int(name, value)
    if integer < 1:
        raise InvalidInputError(f"{name} must be >= 1, got {integer}")
    return integer


def require_modulus(name: str, value: object) -> int:
    """Return ``value`` if it is a modulus (``>= 2`` integer)."""
    integer = require_int(name, value)
    if integer < 2:
        raise InvalidInputError(f"{name} must be >= 2, got {integer}")
    return integer
