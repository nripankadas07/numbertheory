"""Tests for mod_inverse, mod_pow, chinese_remainder."""

import pytest

from numbertheory import (
    InvalidInputError,
    NoSolutionError,
    chinese_remainder,
    mod_inverse,
    mod_pow,
)


class TestModInverse:
    def test_classic_examples(self):
        assert mod_inverse(3, 11) == 4  # 3*4 = 12 = 1 mod 11
        assert mod_inverse(7, 26) == 15
        assert mod_inverse(2, 7) == 4

    def test_inverse_property(self):
        for a, m in [(3, 11), (7, 26), (5, 17), (9, 23)]:
            inv = mod_inverse(a, m)
            assert (a * inv) % m == 1
            assert 0 <= inv < m

    def test_inverse_of_negative_argument(self):
        assert (mod_inverse(-3, 11) * -3) % 11 == 1

    def test_no_inverse_when_not_coprime(self):
        with pytest.raises(NoSolutionError):
            mod_inverse(4, 8)
        with pytest.raises(NoSolutionError):
            mod_inverse(6, 9)

    def test_rejects_modulus_below_two(self):
        with pytest.raises(InvalidInputError):
            mod_inverse(3, 1)
        with pytest.raises(InvalidInputError):
            mod_inverse(3, 0)

    def test_rejects_non_int_args(self):
        with pytest.raises(InvalidInputError):
            mod_inverse(1.5, 7)
        with pytest.raises(InvalidInputError):
            mod_inverse(3, 7.0)


class TestModPow:
    def test_basic_examples(self):
        assert mod_pow(2, 10, 1000) == 24
        assert mod_pow(3, 4, 5) == 1
        assert mod_pow(7, 0, 13) == 1

    def test_zero_base(self):
        assert mod_pow(0, 5, 7) == 0
        assert mod_pow(0, 0, 7) == 1  # convention: 0**0 == 1

    def test_negative_exponent_with_coprime_base(self):
        assert mod_pow(3, -1, 11) == 4  # equals mod_inverse(3, 11)
        assert (mod_pow(7, -2, 13) * pow(7, 2, 13)) % 13 == 1

    def test_negative_exponent_with_non_coprime_raises(self):
        with pytest.raises(NoSolutionError):
            mod_pow(4, -1, 8)

    def test_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            mod_pow(1.5, 3, 7)
        with pytest.raises(InvalidInputError):
            mod_pow(2, 1.5, 7)
        with pytest.raises(InvalidInputError):
            mod_pow(2, 3, 1.5)

    def test_rejects_modulus_below_two(self):
        with pytest.raises(InvalidInputError):
            mod_pow(2, 3, 1)


class TestChineseRemainder:
    def test_classic_pairwise_coprime_example(self):
        x, modulus = chinese_remainder([2, 3, 2], [3, 5, 7])
        assert modulus == 105
        assert x == 23  # x % 3 == 2, x % 5 == 3, x % 7 == 2

    def test_two_pair_example(self):
        x, modulus = chinese_remainder([1, 2], [4, 5])
        assert modulus == 20
        assert x % 4 == 1
        assert x % 5 == 2

    def test_non_coprime_consistent(self):
        x, modulus = chinese_remainder([2, 8], [6, 12])
        assert modulus == 12
        assert x % 6 == 2
        assert x % 12 == 8

    def test_inconsistent_raises(self):
        with pytest.raises(NoSolutionError):
            chinese_remainder([2, 3], [6, 12])  # 2 mod 6 implies 2 or 8 mod 12

    def test_single_congruence(self):
        x, modulus = chinese_remainder([7], [12])
        assert (x, modulus) == (7, 12)

    def test_negative_remainders_normalised(self):
        x, modulus = chinese_remainder([-1, -1], [3, 5])
        assert (x, modulus) == (14, 15)

    def test_length_mismatch_rejected(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([1, 2], [3])

    def test_empty_input_rejected(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([], [])

    def test_first_modulus_validated(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([0], [1])

    def test_remainder_must_be_int(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([1.5], [3])

    def test_later_modulus_validated(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([1, 2], [3, 1])

    def test_later_remainder_must_be_int(self):
        with pytest.raises(InvalidInputError):
            chinese_remainder([1, 1.5], [3, 5])
