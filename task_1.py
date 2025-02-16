from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Алгоритм (жадібний підхід):
      1) Сортуємо завдання за зростанням пріоритету (1 -> найвищий).
      2) Проходимося по відсортованих завданнях, формуючи групу, доки це не перевищує
         обмеження принтера (обсяг і максимальна кількість).
      3) Щойно чергове завдання перевищує обмеження, «закриваємо» поточну групу:
         - додаємо у загальний час максимальний час друку з цієї групи,
         - «скидаємо» лічильники
         - починаємо нову групу.
      4) Після проходження всіх завдань додаємо час останньої групи.
      5) Формуємо послідовність (print_order) як список ID у порядку групування.

    Args:
        print_jobs: Список завдань (dict), кожне з ключами id, volume, priority, print_time
        constraints: Обмеження принтера (dict), містить max_volume, max_items

    Returns:
        Dict з ключами:
            "print_order": список ID завдань у порядку друку
            "total_time": загальний час друку всіх груп
    """
    # Крок 1: Перетворюємо dict у список об’єктів PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]

    # Сортуємо за зростанням пріоритету (1 - найвищий, тому просто за .priority)
    jobs.sort(key=lambda j: j.priority)

    max_volume = constraints["max_volume"]
    max_items = constraints["max_items"]

    print_order = []
    total_time = 0

    # Тимчасові змінні для поточної групи
    current_group = []
    current_group_volume = 0
    current_group_max_time = 0

    for job in jobs:
        # Перевіряємо, чи можна додати завдання в поточну групу,
        # не порушуючи обмеження принтера
        if (len(current_group) < max_items and
                current_group_volume + job.volume <= max_volume):
            # Додаємо завдання в поточну групу
            current_group.append(job)
            current_group_volume += job.volume
            current_group_max_time = max(current_group_max_time, job.print_time)
        else:
            # Якщо обмеження перевищені, «закриваємо» поточну групу:
            total_time += current_group_max_time

            # Додаємо ID завдань цієї групи в загальний порядок
            for grp_job in current_group:
                print_order.append(grp_job.id)

            # Створюємо нову групу з поточним завданням
            current_group = [job]
            current_group_volume = job.volume
            current_group_max_time = job.print_time

    # Після обходу всіх завдань додаємо час останньої групи
    if current_group:
        total_time += current_group_max_time
        for grp_job in current_group:
            print_order.append(grp_job.id)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
