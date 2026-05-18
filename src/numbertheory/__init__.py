"""numbertheory — pure-Python number-theory helpers.

Public surface:

    Greatest-common helpers
        gcd(a, b)                       -> int
        lcm(a, b)                       -> int
        gcd_extended(a, b)              -> tuple[int, int, int]

    Modular arithmetic
        mod_inverse(a, modulus)         -> int
        mod_pow(base, exponent, modulus) -> int
        chinese_remainder(remainders, moduli) -> tuple[int, int]

    Primality + primes
        is_prime(n)                     -> bool   # deterministic Miller-Rabin
        next_prime(n)                   -> int
        prev_prime(n)                   -> int | None
        primes_up_to(n)                 -> list[int]
        nth_prime(n)                    -> int

    Factorisation
        prime_factors(n)                -> list[int]
        factorise(n)                    -> dict[int, int]
        divisors(n)                     -> list[int]
        divisor_count(n)                -> int
        divisor_sum(n)                  -> int

    Multiplicative functions / symbols
        euler_phi(n)                    -> int
        mobius(n)                       -> int
        jacobi_symbol(a, n)             -> int
        legendre_symbol(a, p)           -> int

    Errors
        NumberTheoryError, InvalidInputError, NoSolutionError
"""

from ._errors import (
    InvalidInputError,
    NoSolutionError,
    NumberTheoryError,
)
from ._factor import (
    divisors,
    factorise,
    prime_factors,
)
from ._gcd import gcd, gcd_extended, lcm
from ._modular import chinese_remainder, mod_inverse, mod_pow
from ._multiplicative import (
    divisor_count,
    divisor_sum,
    euler_phi,
    mobius,
)
from ._primality import (
    is_prime,
    next_prime,
    nth_prime,
    prev_prime,
    primes_up_to,
)
from ._symbols import jacobi_symbol, legendre_symbol

__all__ = [
    "NumberTheoryError",
    "InvalidInputError",
    "NoSolutionError",
    "gcd",
    "gcd_extended",
    "lcm",
    "mod_inverse",
    "mod_pow",
    "chinese_remainder",
    "is_prime",
    "next_prime",
    "prev_prime",
    "primes_up_to",
    "nth_prime",
    "prime_factors",
    "factorise",
    "divisors",
    "divisor_count",
    "divisor_sum",
    "euler_phi",
    "mobius",
    "jacobi_symbol",
    "legendre_symbol",
]

__version__ = "0.1.0"
