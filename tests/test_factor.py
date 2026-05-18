"""Tests for prime_factors, factorise, divisors."""

import pytest

from numbertheory import (
    InvalidInputError,
    divisors,
    factorise,
    prime_factors,
)


class TestPrimeFactors:
    def test_classic_examples(self):
        assert prime_factors(1) == []
        assert prime_factors(2) == [2]
        assert prime_factors(3) == [3]
        assert prime_factors(12) == [2, 2, 3]
        assert prime_factors(60) == [2, 2, 3, 5]
        assert prime_factors(100) == [2, 2, 5, 5]
        assert prime_factors(1024) == [2] * 10

    def test_prime_input_returns_self(self):
        for prime in (5, 7, 11, 13, 9973):
            assert prime_factors(prime) == [prime]

    def test_large_composite(self):
        # 2^3 * 3^2 * 5 * 7 = 2520
        assert prime_factors(2520) == [2, 2, 2, 3, 3, 5, 7]

    def test_factors_are_sorted(self):
        for value in (1, 2, 6, 30, 360, 720720):
            factors = prime_factors(value)
            assert factors == sorted(factors)

    def test_product_of_factors_equals_input(self):
        for value in [2, 3, 6, 12, 100, 360, 999, 12345]:
            factors = prime_factors(value)
            product = 1
            for factor in factors:
                product *= factor
            assert product == value

    def test_rejects_zero(self):
        with pytest.raises(InvalidInputError):
            prime_factors(0)

    def test_rejects_negative(self):
        with pytest.raises(InvalidInputError):
            prime_factors(-12)

    def test_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            prime_factors(3.0)


class TestFactorise:
    def test_classic_examples(self):
        assert factorise(1) == {}
        assert factorise(2) == {2: 1}
        assert factorise(12) == {2: 2, 3: 1}
        assert factorise(360) == {2: 3, 3: 2, 5: 1}

    def test_prime_input_has_one_entry(self):
        assert factorise(13) == {13: 1}

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            factorise(0)


class TestDivisors:
    def test_classic_examples(self):
        assert divisors(1) == [1]
        assert divisors(2) == [1, 2]
        assert divisors(12) == [1, 2, 3, 4, 6, 12]
        assert divisors(28) == [1, 2, 4, 7, 14, 28]
        assert divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]

    def test_prime_input_returns_one_and_self(self):
        for prime in (2, 3, 7, 13, 9973):
            assert divisors(prime) == [1, prime]

    def test_count_matches_divisor_count_for_factorial(self):
        # 6! = 720 has 30 divisors
        assert len(divisors(720)) == 30

    def test_largest_divisor_is_input(self):
        for value in (1, 2, 6, 12, 100, 360, 999):
            assert divisors(value)[-1] == value

    def test_smallest_divisor_is_one(self):
        for value in (1, 2, 6, 12, 100, 360, 999):
            assert divisors(value)[0] == 1

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            divisors(0)
        with pytest.raises(InvalidInputError):
            divisors(-12)
