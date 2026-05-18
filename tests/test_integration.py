"""Cross-module sanity checks — exercising compound identities."""

from numbertheory import (
    chinese_remainder,
    divisor_count,
    divisor_sum,
    divisors,
    euler_phi,
    factorise,
    gcd,
    gcd_extended,
    is_prime,
    jacobi_symbol,
    lcm,
    mobius,
    mod_inverse,
    primes_up_to,
)


def test_gcd_lcm_product_identity():
    # gcd(a, b) * lcm(a, b) == |a * b|
    for a, b in [(12, 18), (35, 49), (100, 75), (1, 1), (7, 13)]:
        assert gcd(a, b) * lcm(a, b) == abs(a * b)


def test_extended_gcd_identity():
    for a, b in [(240, 46), (35, 49), (100, 75), (7, 13), (1, 1)]:
        common, x, y = gcd_extended(a, b)
        assert a * x + b * y == common
        assert common == gcd(a, b)


def test_modular_inverse_is_consistent_with_pow():
    for a, m in [(3, 11), (5, 13), (7, 17), (9, 23)]:
        inv = mod_inverse(a, m)
        # By Fermat's little theorem, a^(m-2) is the inverse for prime m.
        assert inv == pow(a, m - 2, m)


def test_crt_round_trip_with_random_pairs():
    from functools import reduce
    cases = [
        ([1, 2, 3], [5, 7, 9]),
        ([0, 0, 0], [3, 5, 11]),
        ([4, 8, 14], [9, 11, 17]),
    ]
    for residues, moduli in cases:
        result, combined = chinese_remainder(residues, moduli)
        for residue, modulus in zip(residues, moduli):
            assert result % modulus == residue % modulus
        assert combined == reduce(lcm, moduli)
        assert 0 <= result < combined

def test_divisor_count_matches_divisors_length():
    for value in (1, 2, 6, 12, 100, 360, 720, 999):
        assert divisor_count(value) == len(divisors(value))


def test_divisor_sum_matches_divisors_total():
    for value in (1, 2, 6, 12, 100, 360, 720):
        assert divisor_sum(value) == sum(divisors(value))


def test_euler_phi_sum_over_divisors_equals_n():
    # Classical identity: sum_{d|n} phi(d) == n
    for value in (1, 2, 6, 12, 36, 100, 360):
        assert sum(euler_phi(divisor) for divisor in divisors(value)) == value


def test_factorise_recovers_n_via_product():
    for value in (1, 2, 12, 360, 999, 2520):
        product = 1
        for prime, exponent in factorise(value).items():
            product *= prime**exponent
        assert product == value


def test_mobius_inversion_identity():
    # sum_{d|n} mobius(d) == 1 if n == 1 else 0
    for value in (1, 2, 6, 12, 30, 100, 360):
        total = sum(mobius(divisor) for divisor in divisors(value))
        assert total == (1 if value == 1 else 0)


def test_jacobi_matches_eulers_criterion_for_prime():
    for prime in primes_up_to(50):
        if prime == 2:
            continue
        for a in range(1, prime):
            expected = pow(a, (prime - 1) // 2, prime)
            if expected == prime - 1:
                expected = -1
            assert jacobi_symbol(a, prime) == expected


def test_primes_up_to_matches_is_prime():
    sieve = primes_up_to(200)
    expected = [n for n in range(2, 201) if is_prime(n)]
    assert sieve == expected
