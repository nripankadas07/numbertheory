"""Error hierarchy for numbertheory.

All errors inherit from both ``NumberTheoryError`` and ``ValueError`` so
callers can catch either the package-specific exception or the standard
``ValueError`` base class.
"""

from __future__ import annotations


class NumberTheoryError(ValueError):
    """Base class for all errors raised by ``numbertheory``."""


class InvalidInputError(NumberTheoryError):
    """Raised when an argument has the wrong type or out-of-range value."""


class NoSolutionError(NumberTheoryError):
    """Raised when a solution does not exist (e.g. modular inverse of a
    non-coprime pair, or CRT with inconsistent residues)."""
