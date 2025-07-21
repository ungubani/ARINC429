from Arinc429 import Arinc429

import matplotlib.pyplot as plt
import numpy as np
import time


def time_check_CRC_arinc(bits_sequences: np.ndarray, number=1) -> list:
    if number < 1: raise ValueError("Неверное число повторений для одной последовательности")

    arinc = Arinc429()

    start = time.time()
    for i in range(len(bits_sequences)):
        bits_sequence = bits_sequences[i]
        subseq = list(bits_sequence[::-1])

        for _ in range(number):

            has_errors = arinc.check_CRC(subseq)

    end = time.time()

    return end - start

def check_crc_polynum(bits_sequence: np.ndarray, tab_remainder_CRC) -> list:
    summa_0 = 0
    bits = np.append(bits_sequence, np.array([0] * 16))
    for j in range(0, 16):
        bits[j] ^= 1

    for i in range(len(bits)):
        if bits[i]:
            two_pow = len(bits) - 1 - i
            summa_0 ^= tab_remainder_CRC[two_pow]

    return summa_0

def time_check_crc_polynum(bits_sequences: np.ndarray, tab_remainder_CRC, number=1) -> list:
    if number < 1: raise ValueError("Неверное число повторений для одной последовательности")

    start = time.time()
    for i in range(len(bits_sequences)):
        bit_sequence = bits_sequences[i]

        for _ in range(number):
            summa_0 = check_crc_polynum(bit_sequence, tab_remainder_CRC)

    end = time.time()

    return end - start


if __name__ == "__main__":
    _LENGTHS_MESSAGES = [32, 48, 72, 144, 272, 528]  # Длина ЗАКОДИРОВАННЫХ блоков (последовательность битов для данных на 16 меньше)
    _COUNT_MESSAGES = 1000
    _LENGTH_CRC = 16

    # ------------------------------------------------------------------------------------------------------------------
    # (1) БЛОК С ПРЕДВЫЧИСЛЕНИЯМИ ТАБЛИЦЫ ДЛЯ ОСТАТКОВ 2^i при делении на полином для CRC
    _LENGTH_SEQ = 15540 + 16
    _POLYNOMIAL = 0x1021
    _MASK_FIRST_BIT = 0x8000
    _REMAINDER_IF_CORRECT = 0x1d0f

    tab_remainder_CRC = np.zeros(_LENGTH_SEQ,
                                 dtype=np.uint32)  # Таблица остатков при делении полиномов 2^i mod _POLYNOMIAL

    tab_remainder_CRC[0] = 1

    for j in range(1, _LENGTH_SEQ):
        tab_remainder_CRC[j] = (tab_remainder_CRC[j - 1] << 1) & 0xffff
        if tab_remainder_CRC[j - 1] & _MASK_FIRST_BIT:
            tab_remainder_CRC[j] ^= _POLYNOMIAL
    # (1) КОНЕЦ
    # ------------------------------------------------------------------------------------------------------------------

    arinc = Arinc429()
    TIMES_table = []
    TIMES_arinc = []

    for len_message in _LENGTHS_MESSAGES:
        len_data = len_message - _LENGTH_CRC
        messages = np.random.randint(2, size=(_COUNT_MESSAGES, len_message))
        # messages = np.array([arinc.encode(np.random.randint(2, size=(len_data,))) for _ in range(_COUNT_MESSAGES)])

        time_table = time_check_crc_polynum(messages, tab_remainder_CRC) / _COUNT_MESSAGES * 1000
        TIMES_table.append(time_table)

        time_arinc = time_check_CRC_arinc(messages) / _COUNT_MESSAGES * 1000
        TIMES_arinc.append(time_arinc)

        print(len_message, time_table, time_arinc)

        temp = 0

    fig_time = plt.figure(figsize=(7, 4.67))
    fig_time.suptitle(f"Сравнение времени проверки контрольной суммы")
    plt.ylabel("t, мс")
    plt.xlabel("Длина сообщения (с учетом CRC)")

    plt.plot(_LENGTHS_MESSAGES, TIMES_table, marker="o", linestyle=":", label="Таблица остатков")
    plt.plot(_LENGTHS_MESSAGES, TIMES_arinc, marker="x", linestyle="-", label="Списки")

    plt.grid()
    plt.legend()
    plt.show()
