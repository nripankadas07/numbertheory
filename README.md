# numbertheory

Pure-Python number-theory helpers — gcd, lcm, extended Euclidean,
modular inverse, Miller-Rabin primality, integer factorisation,
Euler's totient, Möbius, Chinese Remainder Theorem, Jacobi/Legendre
symbols, Sieve of Eratosthenes. **Zero runtime dependencies.**

- 174 tests, **100 % line + 100 % branch coverage**
- `mypy --strict` clean
- `Python 3.9+`
- Every public function validates its input and raises a descriptive
  `NumberTheoryError` (a subclass of `ValueError`) on bad data —
  never silently coerces

## Installation

```bash
pip install numbertheory
```

Or from source:

```bash
git clone https://github.com/nripankadas07/numbertheory
cd numbertheory
pip install -e .
```

## Quick example

```python
from numbertheory import (
    gcd, lcm, gcd_extended,
    mod_inverse, mod_pow, chinese_remainder,
    is_prime, next_prime, primes_up_to, nth_prime,
    factorise, divisors, divisor_count, divisor_sum,
    euler_phi, mobius,
    jacobi_symbol, legendre_symbol,
)

gcd(48, 18)                             # 6
lcm(4, 6)                               # 12
gcd_extended(240, 46)                   # (2, -9, 47)  -- 240 * -9 + 46 * 47 == 2

mod_inverse(3, 11)                      # 4    -- (3 * 4) % 11 == 1
mod_pow(7, -2, 13)                      # 4    -- inverse of 49 mod 13
chinese_remainder([2, 3, 2], [3, 5, 7]) # (23, 105)

is_prime(2**31 - 1)                     # True (Mersenne prime)
next_prime(100)                         # 101
primes_up_to(30)                        # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
nth_prime(25)                           # 97

factorise(360)                          # {2: 3, 3: 2, 5: 1}
divisors(28)                            # [1, 2, 4, 7, 14, 28]
divisor_count(720)                      # 30
divisor_sum(28)                         # 56  (28 is perfect)

euler_phi(36)                           # 12
mobius(30)                              # -1  (squarefree, 3 distinct primes)
jacobi_symbol(2, 7)                     # 1   (2 is a QR mod 7)
legendre_symbol(3, 11)                  # 1
```

## API reference

### GCD helpers

| Function | Returns | Notes |
| --- | --- | --- |
| `gcd(a, b)` | `int` | Always `>= 0`; `gcd(0, 0) == 0` |
| `lcm(a, b)` | `int` | `lcm(0, _) == 0` |
| `gcd_extended(a, b)` | `tuple[int, int, int]` | `(g, x, y)` with `a*x + b*y == g`, `g >= 0` |

### Modular arithmetic

| Function | Returns | Notes |
| --- | --- | --- |
| `mod_inverse(a, m)` | `int` in `[0, m)` | Raises `NoSolutionError` if `gcd(a, m) != 1` |
| `mod_pow(b, e, m)` | `int` | Negative `e` requires `gcd(b, m) == 1` |
| `chinese_remainder(rs, ms)` | `tuple[int, int]` | `(x, M)`; non-coprime moduli OK; raises `NoSolutionError` if inconsistent |

### Primality + primes

| Function | Returns |
| --- | --- |
| `is_prime(n)` | `bool` (deterministic Miller-Rabin, exact for every realistic `n`) |
| `next_prime(n)` | smallest prime `> n` |
| `prev_prime(n)` | largest prime `< n`, or `None` |
| `primes_up_to(n)` | `list[int]` (Sieve of Eratosthenes) |
| `nth_prime(n)` | the `n`-th prime, 1-indexed |

### Factorisation

| Function | Returns |
| --- | --- |
| `prime_factors(n)` | `list[int]` with multiplicity, sorted ascending |
| `factorise(n)` | `dict[int, int]` mapping prime -> exponent |
| `divisors(n)` | `list[int]` of every positive divisor, sorted ascending |

### Multiplicative functions

| Function | Returns |
| --- | --- |
| `divisor_count(n)` | number of positive divisors |
| `divisor_sum(n)` | sum of every positive divisor |
| `euler_phi(n)` | Euler's totient |
| `mobius(n)` | one of `-1`, `0`, `+1` |

### Symbols

| Function | Returns |
| --- | --- |
| `jacobi_symbol(a, n)` | one of `-1`, `0`, `+1`; `n` must be positive odd |
| `legendre_symbol(a, p)` | one of `-1`, `0`, `+1`; `p` must be an odd prime |

### Errors

```
NumberTheoryError(ValueError)
├── InvalidInputError
└── NoSolutionError
```

Every public function raises `InvalidInputError` for bad arguments
(non-integer, out-of-range, length mismatch) and `NoSolutionError`
when the requested mathematical operation has no solution (e.g.
modular inverse of a non-coprime pair, inconsistent CRT system).

## Running tests

```bash
pip install -e .
pip install pytest pytest-cov mypy
pytest                                                  # all 174 tests
pytest --cov=numbertheory --cov-report=term-missing    # coverage
mypy --strict src/numbertheory                          # types
```

## License

MIT — see [LICENSE](LICENSE).
