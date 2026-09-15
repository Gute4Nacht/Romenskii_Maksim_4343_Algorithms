def wagner_fisher_with_trace(s1, s2, cost_replace, cost_insert, cost_delete):
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
    
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i-1] == s2[j-1] and dp[i][j] == dp[i-1][j-1]:
            ops.append(('M', s1[i-1], s2[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + cost_replace:
            ops.append(('R', s1[i-1], s2[j-1]))
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + cost_insert:
            ops.append(('I', ' ', s2[j-1]))
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + cost_delete:
            ops.append(('D', s1[i-1], ' '))
            i -= 1
    
    ops.reverse()
    return dp[m][n], ops

costs = list(map(int, input().split()))
cost_replace, cost_insert, cost_delete = costs[0], costs[1], costs[2]
string_a = input().strip()
string_b = input().strip()

result, ops = wagner_fisher_with_trace(string_a, string_b, 
                                        cost_replace, cost_insert, cost_delete)

op_string = ''.join(op[0] for op in ops)
str_a = ''.join(op[1] for op in ops)
str_b = ''.join(op[2] for op in ops)

print(op_string)
print(str_a)
print(str_b)