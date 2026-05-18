"""Tests for jacobi_symbol and legendre_symbol."""

import pytest

from numbertheory import (
    InvalidInputError,
    jacobi_symbol,
    legendre_symbol,
    is_prime,
)


class TestJacobiSymbol:
    def test_classic_legendre_residues_mod_7(self):
        # Quadratic residues mod 7 are {1, 2, 4}
        assert jacobi_symbol(1, 7) == 1
        assert jacobi_symbol(2, 7) == 1
        assert jacobi_symbol(3, 7) == -1
        assert jacobi_symbol(4, 7) == 1
        assert jacobi_symbol(5, 7) == -1
        assert jacobi_symbol(6, 7) == -1

    def test_jacobi_one_one(self):
        assert jacobi_symbol(0, 1) == 1
        assert jacobi_symbol(5, 1) == 1

    def test_jacobi_zero_is_zero_for_n_above_one(self):
        # When gcd(0, n) = n > 1, the symbol is 0.
        assert jacobi_symbol(0, 3) == 0
        assert jacobi_symbol(0, 9) == 0
        assert jacobi_symbol(0, 15) == 0

    def test_jacobi_with_shared_factor_is_zero(self):
        assert jacobi_symbol(6, 9) == 0
        assert jacobi_symbol(15, 15) == 0
        assert jacobi_symbol(21, 35) == 0

    def test_jacobi_negative_numerator(self):
        # (-1 / n) = +1 if n % 4 == 1, -1 if n % 4 == 3
        assert jacobi_symbol(-1, 5) == 1
        assert jacobi_symbol(-1, 7) == -1

    def test_jacobi_composite_denominator(self):
        # 9 = 3^2, so (a / 9) = (a / 3)^2 in {0, 1}
        assert jacobi_symbol(2, 9) == 1
        assert jacobi_symbol(3, 9) == 0

    def test_rejects_even_denominator(self):
        with pytest.raises(InvalidInputError):
            jacobi_symbol(3, 4)

    def test_rejects_zero_denominator(self):
        with pytest.raises(InvalidInputError):
            jacobi_symbol(3, 0)

    def test_rejects_negative_denominator(self):
        with pytest.raises(InvalidInputError):
            jacobi_symbol(3, -5)

    def test_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            jacobi_symbol(1.5, 7)
        with pytest.raises(InvalidInputError):
            jacobi_symbol(3, 7.0)


class TestLegendreSymbol:
    def test_classic_quadratic_residues_mod_11(self):
        # QRs mod 11: {1, 3, 4, 5, 9}
        for residue in (1, 3, 4, 5, 9):
            assert legendre_symbol(residue, 11) == 1
        for non_residue in (2, 6, 7, 8, 10):
            assert legendre_symbol(non_residue, 11) == -1

    def test_zero_is_zero(self):
        assert legendre_symbol(11, 11) == 0
        assert legendre_symbol(0, 7) == 0

    def test_consistency_with_eulers_criterion(self):
        # For odd prime p, (a/p) ≡ a^((p-1)/2) mod p
        for prime in (3, 5, 7, 11, 13, 23, 47):
            assert is_prime(prime)
            for a in range(1, prime):
                expected = pow(a, (prime - 1) // 2, prime)
                if expected == prime - 1:
                    expected = -1
                assert legendre_symbol(a, prime) == expected

    def test_rejects_two_as_prime(self):
        # Legendre is defined for odd primes only.
        with pytest.raises(InvalidInputError):
            legendre_symbol(1, 2)

    def test_rejects_composite_p(self):
        with pytest.raises(InvalidInputError):
            legendre_symbol(3, 9)

    def test_rejects_non_prime_p(self):
        with pytest.raises(InvalidInputError):
            legendre_symbol(3, 1)

    def test_rejects_negative_p(self):
        with pytest.raises(InvalidInputError):
            legendre_symbol(3, -7)

    def test_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            legendre_symbol(1.5, 7)
        with pytest.raises(InvalidInputError):
            legendre_symbol(3, 7.0)
