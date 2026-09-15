def wagner_fisher(s1, s2, cost_replace, cost_insert, cost_delete):
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
    
    return dp[m][n]

costs = list(map(int, input().split()))
cost_replace, cost_insert, cost_delete = costs[0], costs[1], costs[2]
string_a = input().strip()
string_b = input().strip()

result = wagner_fisher(string_a, string_b, cost_replace, cost_insert, cost_delete)
print(result)