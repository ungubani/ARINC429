from Arinc429 import Arinc429

import numpy as np

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
                print("EURICA!!!", start_pos, end_pos, correct_subseq)
                start_pos = end_pos
                break
            end_pos += 8
        else:
            start_pos += 8


if __name__ == "__main__":
    # TODO Сделать вариант, если не был найден со start_pos, то смещать на байт
    #  (для проверки можно инвертировать первый бит последовательности)
    # file = "mes_01.npy"
    file = "mes_02.npy"

    data_array = np.load(file)

    decode_sequency(data_array)

