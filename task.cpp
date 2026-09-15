#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Square {
    int x, y, w;
};

int n;
int grid[20][20];
int emptyCells;
int bestCount;
vector<Square> bestAnswer;
vector<Square> currentAnswer;

bool canPlace(int x, int y, int w) {
    if (x + w > n || y + w > n) return false;
    for (int i = x; i < x + w; ++i)
        for (int j = y; j < y + w; ++j)
            if (grid[i][j]) return false;
    return true;
}

void fillSquare(int x, int y, int w, int value) {
    for (int i = x; i < x + w; ++i)
        for (int j = y; j < y + w; ++j)
            grid[i][j] = value;

    if (value)
        emptyCells -= w * w;
    else
        emptyCells += w * w;
}

bool findEmpty(int &x, int &y) {
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            if (!grid[i][j]) {
                x = i;
                y = j;
                return true;
            }
    return false;
}

void dfs(int used) {
    if (used >= bestCount && emptyCells > 0) return;

    if (emptyCells == 0) {
        if (used < bestCount) {
            bestCount = used;
            bestAnswer = currentAnswer;
        }
        return;
    }

    int x, y;
    if (!findEmpty(x, y)) return;

    int maxSide = min(n - x, n - y);
    maxSide = min(maxSide, n - 1);

    int lowerBound = (emptyCells + maxSide * maxSide - 1) / (maxSide * maxSide);
    if (used + lowerBound >= bestCount) return;

    for (int w = maxSide; w >= 1; --w) {
        if (!canPlace(x, y, w)) continue;

        fillSquare(x, y, w, 1);
        currentAnswer.push_back({x, y, w});

        dfs(used + 1);

        currentAnswer.pop_back();
        fillSquare(x, y, w, 0);
    }
}

int main() {
    cin >> n;

    bestCount = n * n + 1;
    emptyCells = n * n;
    bestAnswer.clear();
    currentAnswer.clear();

    if (n % 2 == 0) {
        int half = n / 2;
        bestCount = 4;
        bestAnswer.push_back({0, 0, half});
        bestAnswer.push_back({0, half, half});
        bestAnswer.push_back({half, 0, half});
        bestAnswer.push_back({half, half, half});
    } else {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                grid[i][j] = 0;

        for (int first = n - 1; first >= 1; --first) {
            fillSquare(0, 0, first, 1);
            currentAnswer.push_back({0, 0, first});

            dfs(1);

            currentAnswer.pop_back();
            fillSquare(0, 0, first, 0);
        }
    }

    cout << bestCount << '\n';
    for (const auto &sq : bestAnswer) {
        cout << sq.x + 1 << ' ' << sq.y + 1 << ' ' << sq.w << '\n';
    }

    return 0;
}