"""Lock the public re-export list."""

import numbertheory


def test_dunder_all_lists_every_public_name():
    expected = {
        "NumberTheoryError", "InvalidInputError", "NoSolutionError",
        "gcd", "gcd_extended", "lcm",
        "mod_inverse", "mod_pow", "chinese_remainder",
        "is_prime", "next_prime", "prev_prime",
        "primes_up_to", "nth_prime",
        "prime_factors", "factorise", "divisors",
        "divisor_count", "divisor_sum", "euler_phi", "mobius",
        "jacobi_symbol", "legendre_symbol",
    }
    assert set(numbertheory.__all__) == expected


def test_every_exported_name_is_importable():
    for name in numbertheory.__all__:
        assert hasattr(numbertheory, name), f"missing: {name}"


def test_version_is_a_string():
    assert isinstance(numbertheory.__version__, str)
    assert numbertheory.__version__ == "0.1.0"


def test_error_hierarchy():
    assert issubclass(numbertheory.InvalidInputError, numbertheory.NumberTheoryError)
    assert issubclass(numbertheory.NoSolutionError, numbertheory.NumberTheoryError)
    assert issubclass(numbertheory.NumberTheoryError, ValueError)


def test_validate_helpers_reject_bool():
    import pytest
    with pytest.raises(numbertheory.InvalidInputError):
        numbertheory.gcd(True, 5)
    with pytest.raises(numbertheory.InvalidInputError):
        numbertheory.gcd(4, False)
