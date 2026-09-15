import random

def generate_matrix(n, symmetric=False, min_w=1.0, max_w=100.0, seed=None):
    if seed is not None:
        random.seed(seed)
    matrix = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if symmetric and j < i:
                matrix[i][j] = matrix[j][i]
                continue
            if random.random() < 0.9:
                matrix[i][j] = int(round(random.uniform(min_w, max_w), 0))
    return matrix

def save_matrix(matrix, filepath):
    n = len(matrix)
    f = open(filepath, 'w', encoding='utf-8')
    f.write(str(n) + "\n")
    for row in matrix:
        f.write(" ".join(str(v) for v in row) + "\n")
    f.close()
    print("Saved " + str(n) + "x" + str(n) + " matrix to " + filepath)

def print_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            v = matrix[i][j]
            s = str(v)
            while len(s) < 5:
                s = " " + s
            if j < n - 1:
                print(s, end=" ")
            else:
                print(s)

def main():
    args = []
    i = 0
    while True:
        try:
            args = input("generate <N> <file> [--sym] [--seed S] [--min M] [--max M]: ").split()
            break
        except EOFError:
            return

    if len(args) < 2:
        print("Need at least: <N> <file>")
        return

    n = int(args[0])
    filepath = args[1]
    sym = "--sym" in args
    seed = None
    min_w = 1
    max_w = 100

    for i in range(len(args)):
        if args[i] == "--seed" and i + 1 < len(args):
            seed = int(args[i + 1])
        if args[i] == "--min" and i + 1 < len(args):
            min_w = int(args[i + 1])
        if args[i] == "--max" and i + 1 < len(args):
            max_w = int(args[i + 1])

    matrix = generate_matrix(n, symmetric=sym, min_w=min_w, max_w=max_w, seed=seed)
    print_matrix(matrix)
    save_matrix(matrix, filepath)

if __name__ == '__main__':
    main()