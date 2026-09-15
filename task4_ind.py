def wagner_fisher_full_table(s1, s2, cost_replace, cost_insert, cost_delete):
    """Возвращает полную DP-таблицу и расстояние."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * cost_delete
    for j in range(n + 1):
        dp[0][j] = j * cost_insert

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j-1] + cost_replace,
                    dp[i][j-1] + cost_insert,
                    dp[i-1][j] + cost_delete
                )

    return dp, dp[m][n]


def extend_string(dp, s1, s2, cost_replace, cost_insert, cost_delete,
                   extend_which, extension):
    """
    Расширяет одну из строк и дозаполняет DP-таблицу без копирования
    и без пересчёта уже вычисленных значений.

    extend_which: 1 — расширяем s1, 2 — расширяем s2
    extension: строка-продолжение

    Сложность:
      extend_which == 1: O(k * n)  — не зависит от исходной длины s1
      extend_which == 2: O(m * k)  — не зависит от исходной длины s2
    где k = len(extension).

    ВАЖНО: dp мутируется на месте (это и даёт нужную асимптотику).
    Если понадобится вернуться к исходной таблице — сохраните
    свою копию заранее, вне замеряемой операции расширения.
    """
    m, n = len(s1), len(s2)
    k = len(extension)

    if k == 0:
        # Расширение пустой строкой — таблица не меняется
        if extend_which == 1:
            return dp, s1, s2, dp[m][n]
        else:
            return dp, s1, s2, dp[m][n]

    if extend_which == 1:
        # Расширяем s1: добавляем k новых строк, БЕЗ копирования старых
        new_s1 = s1 + extension
        new_m = m + k

        dp.extend([[0] * (n + 1) for _ in range(k)])

        # Базовые случаи для новых строк (столбец 0)
        for i in range(m + 1, new_m + 1):
            dp[i][0] = i * cost_delete

        # Заполняем новые строки — O(k * n)
        for i in range(m + 1, new_m + 1):
            for j in range(1, n + 1):
                if new_s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j-1] + cost_replace,
                        dp[i][j-1] + cost_insert,
                        dp[i-1][j] + cost_delete
                    )

        return dp, new_s1, s2, dp[new_m][n]

    else:  # extend_which == 2
        # Расширяем s2: добавляем k новых столбцов, БЕЗ копирования старых
        new_s2 = s2 + extension
        new_n = n + k

        for row in dp:
            row.extend([0] * k)

        # Базовые случаи для новых столбцов (строка 0)
        for j in range(n + 1, new_n + 1):
            dp[0][j] = j * cost_insert

        # Заполняем новые столбцы — O(m * k)
        for i in range(1, m + 1):
            for j in range(n + 1, new_n + 1):
                if s1[i-1] == new_s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j-1] + cost_replace,
                        dp[i][j-1] + cost_insert,
                        dp[i-1][j] + cost_delete
                    )

        return dp, s1, new_s2, dp[m][new_n]


# ===== Самопроверка: сравниваем результат с полным пересчётом =====
def _self_test():
    import random
    import string

    alphabet = string.ascii_lowercase[:4]
    for _ in range(200):
        s1 = ''.join(random.choice(alphabet) for _ in range(random.randint(0, 6)))
        s2 = ''.join(random.choice(alphabet) for _ in range(random.randint(0, 6)))
        ext = ''.join(random.choice(alphabet) for _ in range(random.randint(0, 4)))
        cr, ci, cd = (random.randint(1, 3) for _ in range(3))
        which = random.choice([1, 2])

        dp, _ = wagner_fisher_full_table(s1, s2, cr, ci, cd)
        _, new_s1, new_s2, incremental_dist = extend_string(
            [row[:] for row in dp], s1, s2, cr, ci, cd, which, ext
        )

        _, full_dist = wagner_fisher_full_table(new_s1, new_s2, cr, ci, cd)

        assert incremental_dist == full_dist, (
            f"Mismatch! s1={s1!r}, s2={s2!r}, ext={ext!r}, which={which}, "
            f"costs=({cr},{ci},{cd}): incremental={incremental_dist}, "
            f"full={full_dist}"
        )

    print("Самопроверка пройдена: 200/200 случайных тестов совпали.")


# ===== Основная программа =====
if __name__ == "__main__":
    # Раскомментируйте, чтобы прогнать самопроверку перед сдачей:
    # _self_test()

    costs = list(map(int, input().split()))
    cost_replace, cost_insert, cost_delete = costs[0], costs[1], costs[2]
    s1 = input().strip()
    s2 = input().strip()

    dp, dist = wagner_fisher_full_table(s1, s2, cost_replace, cost_insert, cost_delete)
    print(f"Базовое расстояние: {dist}")

    which = int(input("Какую строку расширить? (1 или 2): "))
    extension = input("Введите продолжение строки: ").strip()

    dp, s1, s2, new_dist = extend_string(
        dp, s1, s2, cost_replace, cost_insert, cost_delete, which, extension
    )
    print(f"Новое расстояние: {new_dist}")