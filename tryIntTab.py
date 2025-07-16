import numpy as np


_LENGTH_SEQ = 540 + 16
_POLYNOMIAL = 0x11021
_MASK_FIRST_BIT = 0x10000


tab_remainder_CRC = np.zeros(_LENGTH_SEQ, dtype=np.uint32)  # Таблица остатков при делении полиномов 2^i mod _POLYNOMIAL

tab_remainder_CRC[0] = 1

for j in range(1, _LENGTH_SEQ):
    tab_remainder_CRC[j] = (tab_remainder_CRC[j - 1] << 1) & 0x1ffff
    if tab_remainder_CRC[j - 1] & _MASK_FIRST_BIT:
        tab_remainder_CRC[j] ^= _POLYNOMIAL



if __name__ == "__main__":
    print(tab_remainder_CRC)
# print(tab_CRC)
# print(tab_remainder_CRC)
