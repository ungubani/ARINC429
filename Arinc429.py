from typing import List
import general

class Arinc429:
    _GENERATOR_POLYNOMIAL = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]  # x^16 + x^12 + x^5 + 1
    _INVERTING_POLYNOMIAL = [1] * 16
    _LENGTH_CRC = 16
    _LENGTH_COMMON_WORD = 32  # Что?
    _LENGTH_COMMON_DATA = _LENGTH_COMMON_WORD - _LENGTH_CRC
    _REMAINDER_IF_CORRECT = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]
    _X_IN_16 = [0] * 16 + [1]

    def __init__(self):
        pass

    def remainder_to_CRC(self, remainder: List[int]):
        if len(remainder) > self._LENGTH_CRC: raise ValueError(f"В остатке больше, чем {self._LENGTH_CRC} битов!")
        extended_remainder = general.extension_msb_zeros(remainder, length=self._LENGTH_CRC)
        CRC = general.complement_bits(extended_remainder)

        return CRC


    def encode(self, data_bits: List[int]):
        bits = data_bits.copy()

        k = general.number_bits_represent_data(bits)
        if k < self._LENGTH_COMMON_DATA:
            bits = general.extension_msb_zeros(bits, self._LENGTH_COMMON_DATA)
            k = self._LENGTH_COMMON_DATA

        shifted_data = general.multiply_polynomials(bits, self._X_IN_16)
        x_in_k = [0] * k + [1]  # x^k
        invert_mask = general.multiply_polynomials(x_in_k, Arinc429._INVERTING_POLYNOMIAL)

        numerator = general.sum_polynomials(shifted_data, invert_mask)
        remainder = general.remainder_polynomials(numerator, Arinc429._GENERATOR_POLYNOMIAL)

        CRC = self.remainder_to_CRC(remainder)

        return general.sum_polynomials(shifted_data, CRC)

    def decode(self, message_bits: List[int]):
        bits = message_bits.copy()

        n = general.number_bits_represent_data(bits)
        if n < self._LENGTH_CRC + 1:
            raise ValueError(f"Попытка декодировать сообщение длины меньшей, чем 1 + {self._LENGTH_CRC}")

        shifted_message = general.multiply_polynomials(bits, self._X_IN_16)
        x_in_n = [0] * n + [1]  # x^n
        invert_mask = general.multiply_polynomials(x_in_n, self._INVERTING_POLYNOMIAL)

        numerator = general.sum_polynomials(shifted_message, invert_mask)
        remainder = general.remainder_polynomials(numerator, self._GENERATOR_POLYNOMIAL)

        extended_remainder = general.extension_msb_zeros(remainder, self._LENGTH_CRC)  # Приводим остаток к 16 битам

        has_error = not general.bits_is_equal(extended_remainder, self._REMAINDER_IF_CORRECT)  # Если остатки не равны, то решение декодера будет E = 1
        data = message_bits[self._LENGTH_CRC::]

        return has_error, data


if __name__ == "__main__":
    coder_decoder = Arinc429()

    data_exmpl = [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1]
    mes_exmpl = [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1]


    after_encoder = coder_decoder.encode(data_exmpl)

    print(data_exmpl)
    print(after_encoder)
    # print(mes_exmpl)

    has_error, after_decoder = coder_decoder.decode(after_encoder)
    print(has_error, after_decoder)

    #  1010 0111 1000 0111 1010 1100 1111 1101 0000 0110
    #  10100111 / 10000111 / 10101100
