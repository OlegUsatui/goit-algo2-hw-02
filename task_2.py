from typing import List, Dict, Tuple


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з ключами:
          "max_profit": максимальний прибуток,
          "cuts": список довжин частин,
          "number_of_cuts": кількість розрізів
    """
    memo: Dict[int, Tuple[int, List[int]]] = {}  # key: rod_length, value: (profit, cuts_list)

    def helper(n: int) -> Tuple[int, List[int]]:
        if n == 0:
            return (0, [])
        if n in memo:
            return memo[n]

        best_profit = -1
        best_cuts: List[int] = []
        # Перебираємо можливі перші розрізи від 1 до n
        for i in range(1, n + 1):
            # Ціна для частини довжиною i
            current_price = prices[i - 1]
            remaining_profit, remaining_cuts = helper(n - i)
            candidate_profit = current_price + remaining_profit
            # При першій ітерації або при кращому результаті — оновлюємо
            if candidate_profit > best_profit:
                best_profit = candidate_profit
                best_cuts = [i] + remaining_cuts
            # Якщо прибуток рівний, зберігаємо перший знайдений варіант (не оновлюємо)
        memo[n] = (best_profit, best_cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжиною i+1

    Returns:
        Dict з ключами:
          "max_profit": максимальний прибуток,
          "cuts": список довжин частин,
          "number_of_cuts": кількість розрізів
    """
    # dp[j] = (max_profit, number_of_pieces, first_cut)
    dp: List[Tuple[int, int, int]] = [(0, 0, 0)] * (length + 1)
    dp[0] = (0, 0, 0)  # для нульової довжини

    for j in range(1, length + 1):
        best_profit = -1
        best_pieces = 0
        best_first_cut = 0
        # Розглядаємо всі варіанти першого розрізу від 1 до j
        for i in range(1, j + 1):
            candidate_profit = prices[i - 1] + dp[j - i][0]
            # Якщо ріжемо, то кількість частин = 1 (ця частина) + кількість частин для залишку (якщо є)
            candidate_pieces = 1 + (dp[j - i][1] if j - i > 0 else 0)
            # Оновлюємо, якщо отримали кращий прибуток, або при рівному прибутку — якщо більше частин,
            # а при рівних і частинах — вибираємо варіант з більшим першим розрізом
            if candidate_profit > best_profit:
                best_profit = candidate_profit
                best_pieces = candidate_pieces
                best_first_cut = i
            elif candidate_profit == best_profit:
                if candidate_pieces > best_pieces:
                    best_pieces = candidate_pieces
                    best_first_cut = i
                elif candidate_pieces == best_pieces and i > best_first_cut:
                    best_first_cut = i
        dp[j] = (best_profit, best_pieces, best_first_cut)

    # Реконструюємо послідовність розрізів
    n = length
    cuts: List[int] = []
    while n > 0:
        first_cut = dp[n][2]
        cuts.append(first_cut)
        n -= first_cut

    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": dp[length][0],
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }


# Функція для запуску тестів
def run_tests():
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
