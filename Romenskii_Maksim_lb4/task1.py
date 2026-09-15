import sys

def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m

    for i in range(1, m):
        j = pi[i - 1]

        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    return pi


def kmp_search(pattern, text):
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return []

    pi = compute_prefix_function(pattern)
    occurrences = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            occurrences.append(i - m + 1)
            j = pi[j - 1]

    return occurrences


def main():
    P = sys.stdin.readline().strip()
    T = sys.stdin.readline().strip()

    result = kmp_search(P, T)

    if result:
        print(','.join(map(str, result)))
    else:
        print(-1)


if __name__ == '__main__':
    main()