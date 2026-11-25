import hashlib
import json
import math
from fractions import Fraction


MAX_INDEX = 256
RATIONAL_MAX_INDEX = 128
FIRST_TERMS = [1, 1, 17, 865, 88865, 15335425, 3993275825,
               1462392957025, 716611617346625, 452780458211706625,
               358439197464543820625]


def manyama_values(max_index, column=1):
    previous = {power: 1 for power in range(column, 8 * max_index + column + 1, 2)}
    values = [1]
    for index in range(1, max_index + 1):
        current = {
            power: power * (power + 4) * previous[power + 8]
            - power * (power + 3) * previous[power + 6]
            for power in range(column, 8 * (max_index - index) + column + 1, 2)
        }
        values.append(current[column])
        previous = current
    return values


def kotesovec_values(max_index):
    values = [1, 1]
    for index in range(2, max_index + 1):
        first = 288 * index**2 - 576 * index + 317
        second = 9 * (2 * index - 3)**2 * (6 * index - 11) * (6 * index - 7)
        numerator = first * values[-1] - second * values[-2]
        assert numerator % 16 == 0
        values.append(numerator // 16)
    return values[:max_index + 1]


def inverse_cubic_values(max_index):
    square_coefficients = [Fraction(math.comb(3 * index, index), 3**index)
                           for index in range(max_index + 1)]
    coefficients = [Fraction(1)]
    values = [1]
    for index in range(1, max_index + 1):
        lower = sum((coefficients[left] * coefficients[index - left]
                     for left in range(1, index)), Fraction(0))
        coefficient = (square_coefficients[index] - lower) / 2
        coefficients.append(coefficient)
        normalized = coefficient * math.factorial(2 * index)
        assert normalized.denominator == 1
        values.append(normalized.numerator)
        denominator = coefficient.denominator
        for prime in (2, 3):
            while denominator % prime == 0:
                denominator //= prime
        assert denominator == 1
    return values


def primes_through(bound):
    return [candidate for candidate in range(2, bound + 1)
            if all(candidate % divisor for divisor in range(2, math.isqrt(candidate) + 1))]


def valuation(integer, prime):
    assert integer != 0
    exponent = 0
    while integer % prime == 0:
        integer //= prime
        exponent += 1
    return exponent


def factorial_threshold(modulus):
    degree = 0
    residue = 1 % modulus
    while residue:
        degree += 1
        residue = residue * degree % modulus
    return (degree + 1) // 2


def multiply(left, right, max_degree):
    result = [Fraction(0)] * (max_degree + 1)
    for first_index, first in enumerate(left):
        for second_index, second in enumerate(right[:max_degree - first_index + 1]):
            result[first_index + second_index] += first * second
    return result


def companion_checks(primes):
    max_index = 64
    values = inverse_cubic_values(max_index)
    coefficients = [Fraction(value, math.factorial(2 * index))
                    for index, value in enumerate(values)]
    power_coefficients = [Fraction(1)] + [Fraction(0)] * max_index
    comparisons = 0
    valuation_comparisons = 0
    for column in range(1, 9):
        power_coefficients = multiply(power_coefficients, coefficients, max_index)
        column_values = manyama_values(max_index, column)
        for index, coefficient in enumerate(power_coefficients):
            assert coefficient * math.factorial(2 * index) == column_values[index]
            comparisons += 1
            for prime in primes:
                assert valuation(column_values[index], prime) >= valuation(math.factorial(2 * index), prime)
                valuation_comparisons += 1
    inverse_coefficients = [Fraction(math.comb(3 * index, index), (2 * index + 1) * 3**index)
                            for index in range(max_index + 1)]
    odd_coefficients = multiply(inverse_coefficients, coefficients, max_index)
    odd_values = manyama_values(max_index, 5)
    for index, coefficient in enumerate(odd_coefficients):
        assert coefficient * math.factorial(2 * index + 1) == odd_values[index]
        assert math.gcd(odd_values[index], 6) == 1
        assert odd_values[index] % 3 == (1 if index % 2 == 0 else 2)
        for prime in primes:
            assert valuation(odd_values[index], prime) >= valuation(math.factorial(2 * index + 1), prime)
            valuation_comparisons += 1
    squares = multiply(coefficients, coefficients, max_index)
    square_values = manyama_values(max_index, 2)
    for index, coefficient in enumerate(squares):
        value = math.factorial(3 * index) // (3**index * math.factorial(index))
        assert coefficient * math.factorial(2 * index) == value == square_values[index]
        assert value % 3 != 0
        for prime in [2] + primes:
            assert valuation(value, prime) >= valuation(math.factorial(2 * index), prime)
            valuation_comparisons += 1
    return {'indices': [0, max_index], 'columns': [1, 8],
            'column_coefficient_comparisons': comparisons,
            'valuation_comparisons': valuation_comparisons,
            'A281427_source_indices': [1, max_index + 1],
            'A052502_source_indices': [0, max_index],
            'methods': ['integer column recurrence', 'inverse-cubic rational products',
                        'A052502 factorial quotient']}


def differential_identity_certificate():
    terms = [
        multiply([17, 28], multiply([4, -1], [4, -1], 3), 3),
        [-18 * value for value in multiply(multiply([3, -1], [4, -1], 3), [1, 4], 3)],
        [59 * value for value in multiply([0, 1], multiply([3, -1], [3, -1], 3), 3)],
        [-101, 0, 0, 0],
        [15 * value for value in multiply([3, -1], multiply([1, -1], [1, -1], 3), 3)],
    ]
    coefficients = [sum(term[index] for term in terms) for index in range(4)]
    assert coefficients == [0, 0, 0, 0]
    return {'polynomial_variable': 't = u^2', 'degree_bound': 3,
            'coefficients_ascending': [int(value) for value in coefficients]}


def main():
    values = manyama_values(MAX_INDEX)
    assert values == kotesovec_values(MAX_INDEX)
    assert values[:RATIONAL_MAX_INDEX + 1] == inverse_cubic_values(RATIONAL_MAX_INDEX)
    assert values[:len(FIRST_TERMS)] == FIRST_TERMS
    primes = [prime for prime in primes_through(101) if prime >= 5]
    valuation_checks = 0
    for index, value in enumerate(values):
        assert math.gcd(value, 6) == 1
        if index:
            assert value % 3 == (1 if index % 2 else 2)
        factorial = math.factorial(2 * index)
        for prime in primes:
            assert valuation(value, prime) >= valuation(factorial, prime)
            valuation_checks += 1
    modulus_checks = 0
    for modulus in range(1, 513):
        if math.gcd(modulus, 6) != 1:
            continue
        onset = factorial_threshold(modulus)
        for index in range(onset, MAX_INDEX + 1):
            assert values[index] % modulus == 0
            modulus_checks += 1
    assert factorial_threshold(385) == 6
    assert values[5] % 385 == 105
    assert [value % 385 for value in values[:11]] == [1, 1, 17, 95, 315, 105, 0, 0, 0, 0, 0]
    for index in range(2, MAX_INDEX - 18 + 1):
        assert (values[index + 18] - values[index]) % 27 == 0
    residues = [1, 1]
    for index in range(2, 22):
        residues.append((22 * ((18 * index**2 + 18 * index + 20) * residues[-1]
                               + 9 * index**2 * residues[-2])) % 27)
    assert residues == [value % 27 for value in values[:22]]
    assert residues[2:4] == residues[20:22] == [17, 1]
    assert residues[1] == 1 and residues[19] == 10
    assert residues[2] != residues[8] and residues[2] != residues[11]
    for exponent in range(1, 6):
        period = 2 * 3**(exponent - 1)
        for index in range(exponent, MAX_INDEX - period + 1):
            assert (values[index + period] - values[index]) % 3**exponent == 0
    for exponent in range(7):
        period = 2**exponent
        for index in range(MAX_INDEX - period + 1):
            assert (values[index + period] - values[index]) % 2**(exponent + 2) == 0
    result = {
        'status': 'PASS',
        'sequence': 'OEIS A281428',
        'integer_recurrences_equal': {'indices': [0, MAX_INDEX],
                                     'methods': ['Manyama column recurrence', 'Kotesovec recurrence']},
        'inverse_cubic_square_root_equal': {'indices': [0, RATIONAL_MAX_INDEX]},
        'displayed_initial_terms_equal': len(FIRST_TERMS),
        'denominator_support': {'indices': [0, RATIONAL_MAX_INDEX], 'allowed_primes': [2, 3]},
        'factorial_valuation_inequalities': {'indices': [0, MAX_INDEX],
                                           'primes': primes, 'comparisons': valuation_checks},
        'coprime_modulus_checks': {'moduli': [1, 512], 'comparisons': modulus_checks},
        'coprime_to_six': {'indices': [0, MAX_INDEX]},
        'companion_checks': companion_checks(primes),
        'differential_identity_certificate': differential_identity_certificate(),
        'mod_385': {'proved_sufficient_onset': 6, 'last_nonzero_index': 5,
                    'residue_at_5': 105, 'initial_residues': [value % 385 for value in values[:11]]},
        'su_period_congruences': {
            'two_primary': {'exponents_t': [0, 6], 'indices_with_both_terms_at_most': MAX_INDEX},
            'three_primary': {'exponents_r': [1, 5], 'indices_with_both_terms_at_most': MAX_INDEX},
            'mod_27': {'period': 18, 'tested_base_indices': [2, MAX_INDEX - 18],
                       'recurrence_certificate': {'modulus': 27, 'inverse_of_16': 22,
                           'coefficient_period': 3, 'seed_pairs_at_2_and_20': [17, 1],
                           'residues_at_0_through_21': residues,
                           'onset_obstruction': {'indices': [1, 19], 'residues': [1, 10]},
                           'period_6_obstruction': {'indices': [2, 8], 'residues': [17, 26]},
                           'period_9_obstruction': {'indices': [2, 11], 'residues': [17, 10]}}},
        },
        'coefficient_at_256': {'decimal_digits': len(str(values[-1])),
                               'first_12_digits': str(values[-1])[:12],
                               'last_12_digits': str(values[-1])[-12:],
                               'decimal_sha256': hashlib.sha256(str(values[-1]).encode()).hexdigest()},
        'coverage': 'Exact finite coefficient and congruence checks; infinite assertions have written proofs in note.tex or the cited theorem of Su.',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
