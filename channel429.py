"""
    Симметричный канал представляет собой:
    '0' -> '1': p (вер-ть ошибки)
    '0' -> '0': 1-p (вер-ть отсутствия ошибки)
    '1' -> '0': p (вер-ть ошибки)
    '1' -> '1': 1-p (вер-ть отсутствия ошибки)

    Асимметричный канал представляет собой:
    '0' -> '1': 0 (ошибок нет)
    '0' -> '0': 1 (ошибок нет)
    '1' -> '0': p (вер-ть ошибки)
    '1' -> '1': 1-p (вер-ть отсутствия ошибки)
"""


from typing import List
import random


def errors_vector_generator(_code_word: List[int], pe_bit: float, mode="S") -> List[int]:
    """ Для асимметричного канала mode='A'; по умолчанию реализуется генерация ошибок в симметричном канале """
    errors = []

    for i in range(len(_code_word)):
        error = 0

        if mode == "A" and _code_word[i] == 0:
            errors.append(0)
            continue

        if random.random() < pe_bit:
            error = 1

        errors.append(error)

    return errors


def adding_errors(code_word: List[int], errors: List[int]) -> List[int]:
    if len(code_word) != len(errors):
        raise ValueError("Длины кодового слова и вектора ошибок не равны")

    channel_word = []
    for i in range(len(code_word)):
        channel_word.append(code_word[i] ^ errors[i])

    return channel_word


def has_errors(errors: List[int]) -> True:
    return sum(errors) != 0
