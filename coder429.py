from typing import List
import general

class Arinc429:
    _GENERATOR_POLYNOMIAL = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]  # x^16 + x^12 + x^5 + 1
    _INVERTING_POLYNOMIAL = [1] * 16
    def __init__(self):
        pass

    @staticmethod
    def encode(source_data: List[int]):
        k = general.degree_polynomial(source_data)
        shifted_data = general.multiply_polynomials(source_data, [0] * 16 + [1])
        invert_mask = general.multiply_polynomials([0] * k + [1], Arinc429._INVERTING_POLYNOMIAL)

        numerator = general.sum_polynomials(shifted_data, invert_mask)
        remainder = general.remainder_polynomials(numerator, Arinc429._GENERATOR_POLYNOMIAL)

        return general.sum_polynomials(shifted_data, remainder)




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
