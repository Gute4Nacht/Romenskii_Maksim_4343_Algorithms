#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

struct Square {
    int x, y, w;
};

bool DEBUG = false;

int N, M;
int board[20][20];
int emptyArea;
int bestCount;
vector<Square> bestSolution;
vector<Square> currentSolution;
vector<Square> required;
vector<bool> requiredUsed;

string indent(int depth) {
    return string(depth * 2, ' ');
}

bool canPlace(int x, int y, int w) {
    if (x + w > N || y + w > N) return false;
    for (int i = x; i < x + w; ++i)
        for (int j = y; j < y + w; ++j)
            if (board[i][j]) return false;
    return true;
}

void setSquare(int x, int y, int w, int value) {
    for (int i = x; i < x + w; ++i)
        for (int j = y; j < y + w; ++j)
            board[i][j] = value;
    if (value) emptyArea -= w * w;
    else emptyArea += w * w;
}

bool findEmpty(int &x, int &y) {
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            if (!board[i][j]) {
                x = i;
                y = j;
                return true;
            }
    return false;
}

bool conflictsWithRequired(int x, int y, int w) {
    for (int idx = 0; idx < M; ++idx) {
        if (requiredUsed[idx]) continue;
        int rx = required[idx].x;
        int ry = required[idx].y;
        int rw = required[idx].w;
        if (rx == x && ry == y && rw == w) continue;
        if (!(x + w <= rx || rx + rw <= x || y + w <= ry || ry + rw <= y))
            return true;
    }
    return false;
}

int findRequiredIndex(int x, int y, int w) {
    for (int idx = 0; idx < M; ++idx) {
        if (required[idx].x == x && required[idx].y == y && required[idx].w == w)
            return idx;
    }
    return -1;
}

void backtrack(int count, int depth) {
    if (DEBUG) {
        cout << indent(depth) << "Шаг " << count
             << ", свободная площадь " << emptyArea
             << ", лучший результат " << bestCount << "\n";
    }

    if (count >= bestCount && emptyArea > 0) {
        if (DEBUG) cout << indent(depth) << "Отсечение: уже не лучше рекорда\n";
        return;
    }

    if (emptyArea == 0) {
        bool allUsed = true;
        for (int idx = 0; idx < M; ++idx)
            if (!requiredUsed[idx]) { allUsed = false; break; }
        if (!allUsed) {
            if (DEBUG) cout << indent(depth) << "Поле заполнено, но не все обязательные квадраты использованы\n";
            return;
        }
        if (count < bestCount) {
            bestCount = count;
            bestSolution = currentSolution;
            if (DEBUG) cout << indent(depth) << "Найден новый рекорд: " << count << "\n";
        }
        return;
    }

    int x, y;
    if (!findEmpty(x, y)) return;

    if (DEBUG) cout << indent(depth) << "Первая свободная клетка: (" << x + 1 << ", " << y + 1 << ")\n";

    int maxSide = min(N - x, N - y);
    if (maxSide > N - 1) maxSide = N - 1;

    int lowerBound = (emptyArea + maxSide * maxSide - 1) / (maxSide * maxSide);
    if (count + lowerBound >= bestCount) {
        if (DEBUG) cout << indent(depth) << "Отсечение по нижней оценке: " << count << " + " << lowerBound << " >= " << bestCount << "\n";
        return;
    }

    for (int w = maxSide; w >= 1; --w) {
        if (!canPlace(x, y, w)) continue;
        if (conflictsWithRequired(x, y, w)) {
            if (DEBUG) cout << indent(depth) << "Квадрат " << w << "x" << w << " конфликтует с обязательным\n";
            continue;
        }

        int reqIdx = findRequiredIndex(x, y, w);

        if (DEBUG) {
            cout << indent(depth) << "Ставим квадрат " << w << "x" << w
                 << " в (" << x + 1 << ", " << y + 1 << ")";
            if (reqIdx != -1) cout << " (обязательный №" << reqIdx << ")";
            cout << "\n";
        }

        setSquare(x, y, w, 1);
        currentSolution.push_back({x, y, w});
        if (reqIdx != -1) requiredUsed[reqIdx] = true;

        backtrack(count + 1, depth + 1);

        if (reqIdx != -1) requiredUsed[reqIdx] = false;
        currentSolution.pop_back();
        setSquare(x, y, w, 0);

        if (DEBUG) cout << indent(depth) << "Убираем квадрат " << w << "x" << w
                        << " из (" << x + 1 << ", " << y + 1 << ")\n";
    }
}

int main() {
    cin >> N >> M;

    required.clear();
    requiredUsed.assign(M, false);
    for (int i = 0; i < M; ++i) {
        int x, y, w;
        cin >> x >> y >> w;
        required.push_back({x - 1, y - 1, w});
    }

    if (DEBUG) {
        cout << "N = " << N << ", M = " << M << "\n";
        for (int i = 0; i < M; ++i)
            cout << "Обязательный №" << i << ": (" << required[i].x + 1
                 << ", " << required[i].y + 1 << "), сторона " << required[i].w << "\n";
    }

    bestCount = N * N + 1;
    emptyArea = N * N;
    bestSolution.clear();
    currentSolution.clear();

    bool valid = true;
    for (int i = 0; i < M; ++i) {
        int rx = required[i].x;
        int ry = required[i].y;
        int rw = required[i].w;
        if (rw < 1 || rw > N - 1 || rx < 0 || ry < 0 || rx + rw > N || ry + rw > N) {
            valid = false;
            break;
        }
    }
    if (valid) {
        for (int i = 0; i < M && valid; ++i) {
            for (int j = i + 1; j < M; ++j) {
                int ax = required[i].x, ay = required[i].y, aw = required[i].w;
                int bx = required[j].x, by = required[j].y, bw = required[j].w;
                if (!(ax + aw <= bx || bx + bw <= ax || ay + aw <= by || by + bw <= ay)) {
                    valid = false;
                    break;
                }
            }
        }
    }

    if (!valid) {
        if (DEBUG) cout << "Обязательные квадраты заданы некорректно — решения нет\n";
        cout << "No solution\n";
        return 0;
    }

    if (N % 2 == 0 && M == 0) {
        if (DEBUG) cout << "Чётный N без обязательных квадратов — оптимально 4 квадрата\n";
        int half = N / 2;
        bestCount = 4;
        bestSolution.push_back({0, 0, half});
        bestSolution.push_back({0, half, half});
        bestSolution.push_back({half, 0, half});
        bestSolution.push_back({half, half, half});
    } else {
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                board[i][j] = 0;

        for (int first = N - 1; first >= 1; --first) {
            if (conflictsWithRequired(0, 0, first)) continue;

            int reqIdx = findRequiredIndex(0, 0, first);

            if (DEBUG) {
                cout << "\nПробуем первый квадрат " << first << "x" << first
                     << " в (1, 1)";
                if (reqIdx != -1) cout << " (обязательный №" << reqIdx << ")";
                cout << "\n";
            }

            setSquare(0, 0, first, 1);
            currentSolution.push_back({0, 0, first});
            if (reqIdx != -1) requiredUsed[reqIdx] = true;

            backtrack(1, 1);

            if (reqIdx != -1) requiredUsed[reqIdx] = false;
            currentSolution.pop_back();
            setSquare(0, 0, first, 0);
        }
    }

    if (DEBUG) cout << "\nЛучшее решение: " << bestCount << " квадратов\n";

    if (bestCount > N * N) {
        cout << "No solution\n";
    } else {
        cout << bestCount << "\n";
        for (const auto &sq : bestSolution) {
            cout << sq.x + 1 << " " << sq.y + 1 << " " << sq.w << "\n";
        }
    }

    return 0;
}