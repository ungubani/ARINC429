from Arinc429 import Arinc429

import numpy as np
import timeit


def decode_sequency(bits_sequency: np.ndarray):
    arinc = Arinc429()

    seq_len = len(bits_sequency)
    start_pos = 0
    start_size = 8 * 3

    while start_pos < seq_len:
        end_pos = start_pos + start_size  # Будет указывать ЗА последний элемент диапазона

        while end_pos <= seq_len:
            subseq = list(bits_sequency[start_pos:end_pos])
            subseq.reverse()

            has_errors, data = arinc.decode(subseq)
            if not has_errors:
                correct_subseq = list(reversed(subseq))
                # print("EURICA!!!", start_pos, end_pos, correct_subseq)
                start_pos = end_pos
                break
            end_pos += 8
        else:
            start_pos += 8


_LENGTH_SEQ = 540 + 16
_POLYNOMIAL = 0x1021
_MASK_FIRST_BIT = 0x8000
_REMAINDER_IF_CORRECT = 0x1d0f


tab_remainder_CRC = np.zeros(_LENGTH_SEQ, dtype=np.uint32)  # Таблица остатков при делении полиномов 2^i mod _POLYNOMIAL

tab_remainder_CRC[0] = 1

for j in range(1, _LENGTH_SEQ):
    tab_remainder_CRC[j] = (tab_remainder_CRC[j - 1] << 1) & 0xffff
    if tab_remainder_CRC[j - 1] & _MASK_FIRST_BIT:
        tab_remainder_CRC[j] ^= _POLYNOMIAL

def check_crc_polynum(bits: np.ndarray):
    summa_0 = 0
    bits = np.append(bits, np.array([0] * 16))
    for j in range(0, 16):
        bits[j] ^= 1

    for i in range(len(bits)):
        if bits[i]:
            two_pow = len(bits) - 1 - i
            summa_0 ^= tab_remainder_CRC[two_pow]

    return summa_0

def decode_sequency_polynum(bits_sequency: np.ndarray):
    global tab_remainder_CRC

    start_pos = 0

    while start_pos < len(bits_sequency):
        end_pos = start_pos + 8 * 3

        while end_pos <= len(bits_sequency):
            bits = bits_sequency[start_pos:end_pos]
            summa_0 = check_crc_polynum(bits)

            if summa_0 == _REMAINDER_IF_CORRECT:
                # print("WITH_MASKS", start_pos, end_pos)
                start_pos = end_pos
                break
            else:
                # print(start_pos, end_pos, bin(summa_0)[2:])
                end_pos += 8
        else:
            start_pos += 8

if __name__ == "__main__":
    file = "mes_01.npy"
    # file = "mes_02.npy"

    data_array = np.load(file)

    decode_sequency(data_array)

    print(timeit.timeit("decode_sequency_polynum(data_array)", "from __main__ import decode_sequency_polynum, data_array", number=1000))

    print(timeit.timeit("decode_sequency(data_array)", "from __main__ import decode_sequency, data_array; from Arinc429 import Arinc429", number=1000))
