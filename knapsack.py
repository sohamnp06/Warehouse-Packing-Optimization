def fractional_knapsack(items, capacity):
    n = len(items)
    ratio = [(item['profit'] / item['weight'], i) for i, item in enumerate(items)]
    ratio.sort(reverse=True)
    
    total_profit = 0
    total_weight = 0
    fractions = [0] * n
    
    for r, i in ratio:
        if total_weight + items[i]['weight'] <= capacity:
            fractions[i] = 1
            total_profit += items[i]['profit']
            total_weight += items[i]['weight']
        else:
            remain = capacity - total_weight
            if remain > 0:
                fractions[i] = remain / items[i]['weight']
                total_profit += fractions[i] * items[i]['profit']
                total_weight += remain
            break  # capacity reached

    result = []
    for i, item in enumerate(items):
        if fractions[i] > 0:
            result.append({
                'name': item['name'],
                'weight': item['weight'],
                'profit': item['profit'],
                'fraction': fractions[i]
            })
    
    return total_profit, result
def knapsack_01(items, capacity):
    capacity = int(capacity)
    n = len(items)
    
    int_weights = [int(item['weight']) for item in items]
    int_profits = [int(item['profit']) for item in items]

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if int_weights[i-1] <= w:
                dp[i][w] = max(int_profits[i-1] + dp[i-1][w - int_weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    w = capacity
    included_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            included_items.append(items[i-1])
            w -= int_weights[i-1]

    return dp[n][capacity], included_items
