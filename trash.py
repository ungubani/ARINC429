import time
import random


def compare_list_creation_methods(size: int, probability: float, trials: int = 100) -> None:
    """
    Сравнивает скорость создания списка двумя способами:
    1. Генератор списков (List Comprehension)
    2. Создание пустого списка и заполнение через .append()

    :param size: Длина списка
    :param probability: Вероятность появления 1 (иначе 0)
    :param trials: Количество повторений эксперимента для усреднения времени
    """
    # Время для List Comprehension
    lc_times = []
    for _ in range(trials):
        start_time = time.time()
        lst1 = [1 if random.random() <= probability else 0 for _ in range(size)]
        lc_times.append(time.time() - start_time)

    # Время для .append()
    append_times = []
    for _ in range(trials):
        start_time = time.time()
        lst2 = []
        for _ in range(size):
            lst2.append(1 if random.random() <= probability else 0)
        append_times.append(time.time() - start_time)

    # Усреднённое время
    avg_lc_time = sum(lc_times) / trials
    avg_append_time = sum(append_times) / trials

    # Вывод результатов
    print(f"Среднее время List Comprehension: {avg_lc_time:.6f} сек.")
    print(f"Среднее время .append(): {avg_append_time:.6f} сек.")
    print(f"{'List Comprehension' if avg_lc_time < avg_append_time else '.append()'} быстрее!")


if __name__ == "__main__":
    compare_list_creation_methods(size=1_00, probability=0.5)
