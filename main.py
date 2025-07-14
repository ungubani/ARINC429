import coder
import channel

from matplotlib import pyplot as plt
from typing import List
import math
import numpy as np
import random


def message_random_generator(length: int, probability: float = 0.5) -> List[int]:
    # probability - вероятность "1" на i-й позиции

    message = []
    for i in range(length):
        if random.random() < probability:
            message.append(1)
        else:
            message.append(0)

    return message


def pe_decoder_imitation(numbers_experiments: int, pe_bit: int, channel_mode="S"):
    """ Для (!) асимметричного канала mode='A'; по умолчанию реализуется генерация ошибок в симметричном канале """

    decoder_error_counter = 0  # Количество ошибок декодирования

    for _ in range(numbers_experiments):
        # Источник
        source_message = message_random_generator(length)

        # Кодер
        code_word = coder.encode(source_message, _GENERATING_POLYNOMIAL)

        # Канальный уровень
        errors = channel.errors_vector_generator(code_word, pe_bit, mode=channel_mode)
        channel_has_errors = channel.has_errors(errors)
        channel_word = channel.adding_errors(code_word, errors)

        # Декодер
        decoder_message, decoder_decision = coder.decoder(channel_word, _GENERATING_POLYNOMIAL)

        if decoder_decision != channel_has_errors:
            decoder_error_counter += 1

    pe_decoder = decoder_error_counter / numbers_experiments  # Вероятность ошибки декодирования

    return pe_decoder


if __name__ == "__main__":
    _GENERATING_POLYNOMIAL = [1, 1, 0, 1]  # Порождающий многочлен (младший индекс соответствует младшей степени)
    _Pe_BIT = np.linspace(0, 1, 11)  # Вероятности ошибки на бит (в случае log масштаба нужно избегать 0)

    epsilon = 0.01  # 0.01 - 22500 экспериментов; 0.005 - 90000 экспериментов
    numbers_experiments = math.ceil(9 / (4 * epsilon ** 2))
    print(f"Точность = {epsilon}, количество экспериментов = {numbers_experiments}")

    lengths = [3, 4, 6]  # Длина кодируемой последовательности

    plt.figure(figsize=(12, 8))

    for length in lengths:
        print(f"Обрабатывается длина сообщения {length}")
        pe_decoder_values_symmetrical = []  # Сброс списка для текущей длины
        pe_decoder_values_asymmetrical = []
        # pe_decoder_theor = [p ** ((length + coder.degree_polynomial(_GENERATING_POLYNOMIAL)) / 2) for p in _Pe_BIT]  # Само собой не верно

        for pe_bit in _Pe_BIT:
            # Вероятность ошибки декодирования в симметричном канале
            pe_decoder_symmetrical = pe_decoder_imitation(numbers_experiments, pe_bit, channel_mode="S")
            pe_decoder_values_symmetrical.append(pe_decoder_symmetrical)

            # Вероятность ошибки декодирования в (!) асимметричном канале
            pe_decoder_asymmetrical = pe_decoder_imitation(numbers_experiments, pe_bit, channel_mode="A")
            pe_decoder_values_asymmetrical.append(pe_decoder_asymmetrical)

        plt.plot(_Pe_BIT, pe_decoder_values_symmetrical, marker='o', linestyle='-', label=f"Симметричный, длина = {length}")
        plt.plot(_Pe_BIT, pe_decoder_values_asymmetrical, marker='x', linestyle='--', label=f"Асимметричный, длина = {length}")
        # plt.plot(_Pe_BIT, pe_decoder_theor, marker='+', linestyle=':', label=f"Асимм. теоретич, длина = {length}")

    plt.title(f"Вероятность ошибки декодирования CRC-{coder.degree_polynomial(_GENERATING_POLYNOMIAL)}")
    plt.xlabel("Вероятность ошибки на бит (Pe)")
    plt.ylabel("Вероятность ошибки декодирования (Pe)")

    plt.legend()
    plt.grid()
    plt.show()

