"""Tests for divisor_count, divisor_sum, euler_phi, mobius."""

import pytest

from numbertheory import (
    InvalidInputError,
    divisor_count,
    divisor_sum,
    euler_phi,
    mobius,
)


class TestDivisorCount:
    def test_classic_examples(self):
        assert divisor_count(1) == 1
        assert divisor_count(2) == 2
        assert divisor_count(12) == 6
        assert divisor_count(36) == 9
        assert divisor_count(720) == 30

    def test_prime_returns_two(self):
        for prime in (2, 3, 5, 7, 9973):
            assert divisor_count(prime) == 2

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            divisor_count(0)


class TestDivisorSum:
    def test_classic_examples(self):
        assert divisor_sum(1) == 1
        assert divisor_sum(6) == 12  # 1+2+3+6 (perfect number test)
        assert divisor_sum(12) == 28
        assert divisor_sum(28) == 56  # 28 perfect: sum-of-proper = 28

    def test_prime_returns_p_plus_one(self):
        for prime in (2, 3, 7, 9973):
            assert divisor_sum(prime) == prime + 1

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            divisor_sum(0)


class TestEulerPhi:
    def test_classic_examples(self):
        assert euler_phi(1) == 1
        assert euler_phi(2) == 1
        assert euler_phi(9) == 6
        assert euler_phi(10) == 4
        assert euler_phi(36) == 12

    def test_prime_returns_p_minus_one(self):
        for prime in (2, 3, 7, 13, 97, 9973):
            assert euler_phi(prime) == prime - 1

    def test_prime_power_formula(self):
        # phi(p^k) = p^(k-1) * (p-1)
        assert euler_phi(8) == 4
        assert euler_phi(27) == 18
        assert euler_phi(49) == 42

    def test_multiplicative(self):
        # phi(m*n) = phi(m)*phi(n) when gcd(m,n)=1
        assert euler_phi(35) == euler_phi(5) * euler_phi(7)
        assert euler_phi(143) == euler_phi(11) * euler_phi(13)

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            euler_phi(0)


class TestMobius:
    def test_one_is_one(self):
        assert mobius(1) == 1

    @pytest.mark.parametrize("prime", [2, 3, 5, 7, 11, 13])
    def test_prime_returns_minus_one(self, prime):
        assert mobius(prime) == -1

    def test_squarefree_with_two_factors_is_one(self):
        assert mobius(6) == 1   # 2 * 3
        assert mobius(10) == 1  # 2 * 5
        assert mobius(15) == 1  # 3 * 5
        assert mobius(35) == 1  # 5 * 7

    def test_squarefree_with_three_factors_is_minus_one(self):
        assert mobius(30) == -1  # 2 * 3 * 5
        assert mobius(42) == -1  # 2 * 3 * 7

    def test_non_squarefree_is_zero(self):
        assert mobius(4) == 0   # 2^2
        assert mobius(8) == 0   # 2^3
        assert mobius(9) == 0   # 3^2
        assert mobius(12) == 0  # 2^2 * 3
        assert mobius(50) == 0  # 2 * 5^2

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            mobius(0)
        with pytest.raises(InvalidInputError):
            mobius(-3)
