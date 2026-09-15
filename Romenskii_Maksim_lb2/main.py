import sys

DEBUG_MODE = False

INF = float('inf')


def log(*args):
    if DEBUG_MODE:
        print(*args)


def read_tokens():
    return sys.stdin.read().split()


def heap_push(heap, item):
    heap.append(item)
    i = len(heap) - 1
    while i > 0:
        p = (i - 1) // 2
        if heap[p] <= heap[i]:
            break
        heap[i], heap[p] = heap[p], heap[i]
        i = p


def heap_pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i = 0
        n = len(heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n and heap[left] < heap[smallest]:
                smallest = left
            if right < n and heap[right] < heap[smallest]:
                smallest = right
            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
    return top


def nearest_neighbor(graph, n):
    """Метод 1: Приближённый алгоритм (АБС / Ближайший сосед)."""
    if n == 0:
        return INF, []

    path = [0]
    visited = {0}
    cost = 0.0
    curr = 0

    log("[АБС] Запуск приближённого алгоритма. Старт из вершины 0.")

    for step in range(n - 1):
        best_w = INF
        best_v = -1

        for v in range(n):
            if v not in visited and graph[curr][v] < best_w:
                best_w = graph[curr][v]
                best_v = v

        if best_v == -1:
            log("[АБС] Тупик! Граф несвязен, путь не найден.")
            return INF, []

        path.append(best_v)
        visited.add(best_v)
        cost += best_w
        log("[АБС] Шаг " + str(step + 1) + ": " + str(curr) + " -> " + str(best_v) + " (вес " + str(best_w) + ")")
        curr = best_v

    if graph[curr][0] == INF:
        log("[АБС] Нет обратного ребра в стартовую вершину 0.")
        return INF, []

    cost += graph[curr][0]
    log("[АБС] Возврат: " + str(curr) + " -> 0 (вес " + str(graph[curr][0]) + ")")
    log("[АБС] Итоговый маршрут: " + str(path))
    log("[АБС] Итоговая стоимость: " + str(cost))
    log()

    return cost, path


def get_remainder_lb(path, forbidden, graph, n):
    """
    Нижняя оценка остатка пути.
    Берётся максимум из двух оценок:
    1) Полусумма весов двух легчайших допустимых рёбер по всем кускам.
    2) Вес минимального остовного дерева (МОД) на кускаx.
    """
    pieces = [(path[0], path[-1])]

    for v in range(n):
        if v not in path:
            pieces.append((v, v))

    m = len(pieces)

    if m == 1:
        s, e = pieces[0]
        if graph[e][s] != INF and (e, s) not in forbidden:
            return graph[e][s]
        return INF

    total = 0.0
    for i in range(m):
        s_i, e_i = pieces[i]
        weights = []

        for j in range(m):
            if i == j:
                continue
            s_j, e_j = pieces[j]

            w = graph[e_i][s_j]
            if w != INF and (e_i, s_j) not in forbidden:
                weights.append(w)

            w = graph[e_j][s_i]
            if w != INF and (e_j, s_i) not in forbidden:
                weights.append(w)

        if len(weights) < 2:
            return INF

        weights.sort()
        total += weights[0] + weights[1]

    half = total / 2.0

    edges = []
    for i in range(m):
        for j in range(i + 1, m):
            e_i = pieces[i][1]
            s_i = pieces[i][0]
            e_j = pieces[j][1]
            s_j = pieces[j][0]

            w1 = graph[e_i][s_j]
            if (e_i, s_j) in forbidden:
                w1 = INF

            w2 = graph[e_j][s_i]
            if (e_j, s_i) in forbidden:
                w2 = INF

            w = w1 if w1 < w2 else w2

            if w != INF:
                edges.append((w, i, j))

    edges.sort()
    parent = list(range(m))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst = 0.0
    used = 0

    for w, i, j in edges:
        ri = find(i)
        rj = find(j)

        if ri != rj:
            parent[ri] = rj
            mst += w
            used += 1

            if used == m - 1:
                break

    if used < m - 1:
        return INF

    return half if half > mst else mst


def solve():
    tokens = read_tokens()

    if not tokens:
        return

    n = int(tokens[0])

    if n <= 0:
        return

    if n == 1:
        if DEBUG_MODE:
            log("=" * 55)
            log("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
            log("=" * 55)
            log("Метод 1 (АБС):       0 | Стоимость: 0.0")
            log("Метод 2 (МВиГ):      0 | Стоимость: 0.0")
            log("=" * 55)
        else:
            print(0)
            print(0.0)
        return

    graph = []
    idx = 1

    for _ in range(n):
        row = []
        for _ in range(n):
            val = float(tokens[idx])
            idx += 1
            if val < 0:
                row.append(INF)
            else:
                row.append(val)
        graph.append(row)

    if DEBUG_MODE:
        log("[ВВОД] Считана матрица " + str(n) + "x" + str(n))
        for r in range(n):
            row_str = ""
            for c in range(n):
                v = graph[r][c]
                if v == INF:
                    s = "  INF"
                else:
                    s = str(v)
                    while len(s) < 5:
                        s = " " + s
                if c < n - 1:
                    row_str += s + " "
                else:
                    row_str += s
            log("  " + row_str)
        log()

    nn_cost, nn_path = nearest_neighbor(graph, n)
    best_cost = nn_cost
    best_path = nn_path if nn_path else []

    if DEBUG_MODE:
        log("-" * 55)
        log("[МВиГ] Запуск точного метода (ветвей и границ).")
        if best_cost != INF:
            log("[МВиГ] Начальный рекорд из АБС: " + str(best_cost))
        else:
            log("[МВиГ] АБС не нашёл путь. Рекорд = бесконечность.")
        log()

    pq = []
    counter = 0
    nodes = 0

    rem = get_remainder_lb((0,), frozenset(), graph, n)

    if rem != INF:
        heap_push(pq, (rem, counter, 0.0, (0,), frozenset()))

    while pq:
        lb, _, cost, path, forbidden = heap_pop(pq)
        nodes += 1

        if lb >= best_cost:
            continue

        u = path[-1]

        for v in range(n):
            if v not in path and (u, v) not in forbidden and graph[u][v] != INF:
                new_cost = cost + graph[u][v]
                new_path = path + (v,)

                if len(new_path) == n:
                    if graph[v][path[0]] != INF and (v, path[0]) not in forbidden:
                        final_cost = new_cost + graph[v][path[0]]

                        if final_cost < best_cost:
                            best_cost = final_cost
                            best_path = list(new_path)
                            if DEBUG_MODE:
                                log("[МВиГ] Найден новый рекорд! Маршрут: " +
                                    " ".join(str(x) for x in best_path) +
                                    " | Стоимость: " + str(best_cost))
                else:
                    new_forbidden = set(forbidden)
                    new_forbidden.add((v, path[0]))

                    rem = get_remainder_lb(new_path, frozenset(new_forbidden), graph, n)

                    if rem == INF:
                        continue

                    new_lb = new_cost + rem

                    if new_lb < best_cost:
                        counter += 1
                        heap_push(pq, (new_lb, counter, new_cost, new_path, frozenset(new_forbidden)))

    if DEBUG_MODE:
        log()
        log("[МВиГ] Поиск завершён. Обработано узлов: " + str(nodes))
        log()
        log("=" * 55)
        log("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
        log("=" * 55)
        if nn_cost == INF:
            log("Метод 1 (АБС):       решение не найдено")
        else:
            log("Метод 1 (АБС):       " +
                " ".join(str(x) for x in nn_path) +
                " | Стоимость: " + str(float(nn_cost)))
        if best_cost == INF:
            log("Метод 2 (МВиГ):      решение не найдено")
        else:
            log("Метод 2 (МВиГ):      " +
                " ".join(str(x) for x in best_path) +
                " | Стоимость: " + str(float(best_cost)))
        log("=" * 55)
    else:
        if best_cost == INF:
            print("Решение не найдено")
        else:
            print(" ".join(map(str, best_path)))
            print(float(best_cost))


if __name__ == '__main__':
    solve()