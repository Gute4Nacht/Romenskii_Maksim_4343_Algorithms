def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j-1], curr[j-1], prev[j])
        prev, curr = curr, prev
    
    return prev[n]

s = input().strip()
t = input().strip()

result = levenshtein_distance(s, t)
print(result)
