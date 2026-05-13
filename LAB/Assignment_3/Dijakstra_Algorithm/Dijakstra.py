g = [
	[0, 10, 0, 5, 0],
	[0, 0, 1, 2, 0],
	[0, 0, 0, 0, 4],
	[0, 3, 9, 0, 2],
	[7, 0, 6, 0, 0]
]
n = len(g)
s = 0

INF = 10**9
d = [INF] * n
used = [False] * n
d[s] = 0

for _ in range(n):
	u = -1
	for i in range(n):
		if not used[i] and (u == -1 or d[i] < d[u]):
			u = i
	if u == -1 or d[u] == INF:
		break
	used[u] = True
	for v in range(n):
		if g[u][v] > 0 and d[u] + g[u][v] < d[v]:
			d[v] = d[u] + g[u][v]

print(*[-1 if x == INF else x for x in d])
