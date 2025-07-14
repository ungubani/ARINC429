from typing import List


def degree_polynomial(polynomial: List[int]) -> int:
    degree = len(polynomial) - 1

    while polynomial[degree] == 0 and degree != 0:
        degree = degree - 1

    return degree


def remainder_polynomials(divisible: List[int], divider: List[int]) -> List[int]:
    divisible_copy = divisible.copy()
    divider_copy = divider.copy()
    remainder = []

    divider_degree = degree_polynomial(divider)  # Определяем высшую степень делителя

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


def multiply_polynomials(multipliable: List[int], multiplier: List[int]) -> List[int]:
    result = [0 for _ in range(len(multipliable) + len(multiplier) - 1)]

    for i in range(len(multiplier)):
        for j in range(len(multipliable)):
            digit = multipliable[j] & multiplier[i]

            result[i + j] = result[i + j] ^ digit

    return result


def sum_polynomials(first: List[int], second: List[int]) -> List[int]:
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


def encode(message: List[int], generating_polinomial: List[int]) -> List[int]:
    gp_degree = degree_polynomial(generating_polinomial)

    # Кривенькая реализация m(x) * x^r
    shifted_message = [0 for _ in range(len(message) + gp_degree)]
    for i in range(len(message)):
        shifted_message[gp_degree + i] = message[i]

    check_sum = remainder_polynomials(shifted_message, generating_polinomial)
    code_word = sum_polynomials(shifted_message, check_sum)

    return code_word


def decoder(channel_word: List[int], generating_polinomial: List[int]) -> tuple[List[int], bool]:
    syndrome = remainder_polynomials(channel_word, generating_polinomial)
    # print(f"__syndrome__= {syndrome}")

    decision = False
    if sum(syndrome) != 0:
        decision = True

    decoded_message = []
    for i in range(len(channel_word) - degree_polynomial(generating_polinomial)):
        decoded_message.append(channel_word[i])

    return decoded_message, decision


if __name__ == "__main__":
    pass
