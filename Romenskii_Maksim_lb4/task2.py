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


def main():
    A = sys.stdin.readline().strip()
    B = sys.stdin.readline().strip()

    n = len(A)
    m = len(B)

    if n != m:
        print(-1)
        return

    if n == 0:
        print(0)
        return

    pi = compute_prefix_function(B)

    j = 0

    for i in range(2 * n - 1):
        char = A[i % n]

        while j > 0 and char != B[j]:
            j = pi[j - 1]

        if char == B[j]:
            j += 1

        if j == m:
            start_index = i - m + 1
            print(start_index)
            return

    print(-1)


if __name__ == '__main__':
    main()