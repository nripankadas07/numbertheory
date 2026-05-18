"""Tests for is_prime, next_prime, prev_prime, primes_up_to, nth_prime."""

import pytest

from numbertheory import (
    InvalidInputError,
    is_prime,
    next_prime,
    nth_prime,
    prev_prime,
    primes_up_to,
)


class TestIsPrime:
    @pytest.mark.parametrize("value", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
    def test_small_primes_are_prime(self, value):
        assert is_prime(value) is True

    @pytest.mark.parametrize("value", [-7, -1, 0, 1, 4, 6, 8, 9, 12, 25, 27, 49])
    def test_non_primes_are_not_prime(self, value):
        assert is_prime(value) is False

    def test_carmichael_numbers_are_composite(self):
        # 561, 1105, 1729, 2465 are all Carmichael numbers — fool Fermat
        # but not Miller-Rabin.
        for carmichael in (561, 1105, 1729, 2465, 2821):
            assert is_prime(carmichael) is False

    def test_large_known_primes(self):
        # Mersenne 2**31 - 1 is prime; 2**31 is not.
        assert is_prime(2**31 - 1) is True
        assert is_prime(2**31) is False

    def test_64_bit_primes(self):
        # Known prime above 2**62.
        assert is_prime(4611686018427387847) is True

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            is_prime(1.5)
        with pytest.raises(InvalidInputError):
            is_prime("3")
        with pytest.raises(InvalidInputError):
            is_prime(True)


class TestNextPrime:
    def test_basic_examples(self):
        assert next_prime(0) == 2
        assert next_prime(1) == 2
        assert next_prime(2) == 3
        assert next_prime(3) == 5
        assert next_prime(10) == 11
        assert next_prime(20) == 23
        assert next_prime(100) == 101

    def test_below_two_returns_two(self):
        assert next_prime(-100) == 2
        assert next_prime(-1) == 2

    def test_strict_inequality(self):
        # next_prime(p) > p, never == p
        for prime in (2, 3, 5, 7, 11, 13, 9973):
            assert next_prime(prime) > prime

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            next_prime(1.5)


class TestPrevPrime:
    def test_basic_examples(self):
        assert prev_prime(3) == 2
        assert prev_prime(11) == 7
        assert prev_prime(12) == 11
        assert prev_prime(101) == 97

    def test_returns_none_when_below_three(self):
        assert prev_prime(2) is None
        assert prev_prime(1) is None
        assert prev_prime(0) is None
        assert prev_prime(-5) is None

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            prev_prime(1.5)


class TestPrimesUpTo:
    def test_classic_example(self):
        assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    def test_zero_and_one_return_empty(self):
        assert primes_up_to(0) == []
        assert primes_up_to(1) == []
        assert primes_up_to(-7) == []

    def test_two(self):
        assert primes_up_to(2) == [2]

    def test_count_matches_pi_function(self):
        # pi(100) == 25
        assert len(primes_up_to(100)) == 25
        # pi(1000) == 168
        assert len(primes_up_to(1000)) == 168

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            primes_up_to(1.5)


class TestNthPrime:
    def test_first_few_primes(self):
        assert nth_prime(1) == 2
        assert nth_prime(2) == 3
        assert nth_prime(3) == 5
        assert nth_prime(4) == 7
        assert nth_prime(10) == 29
        assert nth_prime(25) == 97

    def test_consistency_with_primes_up_to(self):
        sieve = primes_up_to(100)
        for index, prime in enumerate(sieve, start=1):
            assert nth_prime(index) == prime

    def test_rejects_non_positive(self):
        with pytest.raises(InvalidInputError):
            nth_prime(0)
        with pytest.raises(InvalidInputError):
            nth_prime(-3)

    def test_validation(self):
        with pytest.raises(InvalidInputError):
            nth_prime(1.5)
