"""Tests for gcd, lcm, gcd_extended."""

import pytest

from numbertheory import gcd, gcd_extended, lcm
from numbertheory import InvalidInputError


class TestGcdHappyPath:
    def test_gcd_returns_classic_examples(self):
        assert gcd(12, 18) == 6
        assert gcd(48, 18) == 6
        assert gcd(54, 24) == 6

    def test_gcd_with_zero_returns_other_argument(self):
        assert gcd(0, 7) == 7
        assert gcd(7, 0) == 7

    def test_gcd_of_zero_zero_is_zero(self):
        assert gcd(0, 0) == 0

    def test_gcd_with_one_is_one(self):
        assert gcd(1, 999) == 1
        assert gcd(999, 1) == 1

    def test_gcd_handles_coprime_pair(self):
        assert gcd(7, 13) == 1

    def test_gcd_handles_negative_inputs(self):
        assert gcd(-12, 18) == 6
        assert gcd(12, -18) == 6
        assert gcd(-12, -18) == 6

    def test_gcd_with_equal_values(self):
        assert gcd(15, 15) == 15
        assert gcd(-15, -15) == 15


class TestGcdInputValidation:
    @pytest.mark.parametrize("invalid", [1.5, "5", None, [1], True, False])
    def test_gcd_rejects_non_int_first_arg(self, invalid):
        with pytest.raises(InvalidInputError):
            gcd(invalid, 5)

    @pytest.mark.parametrize("invalid", [1.5, "5", None, [1], True, False])
    def test_gcd_rejects_non_int_second_arg(self, invalid):
        with pytest.raises(InvalidInputError):
            gcd(5, invalid)


class TestLcm:
    def test_lcm_returns_classic_examples(self):
        assert lcm(4, 6) == 12
        assert lcm(21, 6) == 42
        assert lcm(15, 20) == 60

    def test_lcm_with_zero_is_zero(self):
        assert lcm(0, 7) == 0
        assert lcm(7, 0) == 0
        assert lcm(0, 0) == 0

    def test_lcm_handles_negatives(self):
        assert lcm(-4, 6) == 12
        assert lcm(4, -6) == 12
        assert lcm(-4, -6) == 12

    def test_lcm_of_coprime_is_product(self):
        assert lcm(7, 11) == 77

    def test_lcm_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            lcm(1.5, 3)
        with pytest.raises(InvalidInputError):
            lcm(3, 1.5)


class TestGcdExtended:
    def test_returns_classic_bezout_pair(self):
        gcd_val, x, y = gcd_extended(240, 46)
        assert gcd_val == 2
        assert 240 * x + 46 * y == 2

    def test_with_zero_first(self):
        gcd_val, x, y = gcd_extended(0, 7)
        assert gcd_val == 7
        assert 0 * x + 7 * y == 7

    def test_with_zero_second(self):
        gcd_val, x, y = gcd_extended(7, 0)
        assert gcd_val == 7
        assert 7 * x + 0 * y == 7

    def test_with_zero_zero(self):
        gcd_val, x, y = gcd_extended(0, 0)
        assert gcd_val == 0
        assert (x, y) == (1, 0)

    def test_with_negative_first(self):
        gcd_val, x, y = gcd_extended(-12, 18)
        assert gcd_val == 6
        assert -12 * x + 18 * y == 6

    def test_with_negative_second(self):
        gcd_val, x, y = gcd_extended(12, -18)
        assert gcd_val == 6
        assert 12 * x + -18 * y == 6

    def test_with_both_negative(self):
        gcd_val, x, y = gcd_extended(-12, -18)
        assert gcd_val == 6
        assert -12 * x + -18 * y == 6

    def test_with_coprime_pair(self):
        gcd_val, x, y = gcd_extended(7, 13)
        assert gcd_val == 1
        assert 7 * x + 13 * y == 1

    def test_validation_rejects_non_int(self):
        with pytest.raises(InvalidInputError):
            gcd_extended(1.5, 7)
        with pytest.raises(InvalidInputError):
            gcd_extended(7, 1.5)
