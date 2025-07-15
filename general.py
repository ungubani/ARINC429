from typing import List


def adding_errors(code_word: List[int], errors: List[int]) -> List[int]:
    if len(code_word) != len(errors):
        raise ValueError("Длины кодового слова и вектора ошибок не равны")

    channel_word = []
    for i in range(len(code_word)):
        channel_word.append(code_word[i] ^ errors[i])

    return channel_word

def bits_is_equal(lhs_bits: List[int], rhs_bits: List[int]) -> bool:
    if len(lhs_bits) != len(rhs_bits): return False

    for i in range(len(lhs_bits)):
        if lhs_bits[i] != rhs_bits[i]:
            return False

    return True

def complement_bits(bits: List[int]) -> List[int]:
    bits_copy = bits.copy()
    for i in range(len(bits_copy)):
        bits_copy[i] ^= 1
    return bits_copy

def degree_polynomial_math(polynomial: List[int]) -> int:
    # В этой функции степень полинома определяется как "степень" первого ненулевого бита
    degree = len(polynomial) - 1
    while polynomial[degree] == 0 and degree != 0:
        degree = degree - 1
    return degree

def error_vec_has_errors(errors: List[int]) -> True:
    return sum(errors) != 0

def extension_msb_zeros(bits: List[int], length: int = 16) -> List[int]:
    # Добавляет нули в старшие биты, расширяя bits до длины length
    bits_copy = bits.copy()
    while len(bits_copy) < length:
        bits_copy.append(0)
    return bits_copy

def number_bits_represent_data(data: List[int]) -> int:
    # Сколько битов задействовано в представлении данных
    return len(data)

def multiply_polynomials(multipliable: List[int], multiplier: List[int]) -> List[int]:
    result = [0 for _ in range(len(multipliable) + len(multiplier) - 1)]

    for i in range(len(multiplier)):
        for j in range(len(multipliable)):
            digit = multipliable[j] & multiplier[i]

            result[i + j] = result[i + j] ^ digit

    return result

def remainder_polynomials(divisible: List[int], divider: List[int]) -> List[int]:
    # Возвращает остаток БЕЗ нулей в MSB (MostSignificantBits)
    divisible_copy = divisible.copy()
    divider_copy = divider.copy()
    remainder = []

    divider_degree = degree_polynomial_math(divider)  # Определяем высшую степень делителя

    if divider_degree >= len(divisible_copy):  # Если степень делителя больше степени делимого, результат уже известен
        for i in range(len(divisible_copy)):
            remainder.append(divisible_copy[i])
        while len(remainder) != len(divider) - 1:
            remainder.append(0)

        return remainder


    for i in range(len(divider_copy) - 1, 0, -1):
        if divider_copy[i] != 0:
            divider_degree = i
            break

    for i in range(len(divisible_copy) - 1, divider_degree - 1, -1):
        if divisible_copy[i] != 0:
            # print("Pered", divisible_copy, divider_copy)
            for j in range(divider_degree + 1):
                divisible_copy[i - j] = divisible_copy[i - j] ^ divider_copy[divider_degree - j]

            # print("Posle", divisible_copy, divider_copy)
    for i in range(len(divider) - 1):
        remainder.append(divisible_copy[i])

    return remainder



def sum_polynomials(first: List[int], second: List[int]) -> List[int]:
    # В этой функции нет проверки на "ведущие нули", так что ее можно легко использовать
    result = [0 for _ in range(max(len(first), len(second)))]

    i = 0
    while i < min(len(first), len(second)):
        result[i] = first[i] ^ second[i]
        i = i + 1

    while i < len(first):
        result[i] = first[i]
        i = i + 1
    while i < len(second):
        result[i] = second[i]
        i = i + 1

    return result


