import heapq

def prim(n, adj):
    vis = [False]*n
    pq = [(0, 0)] 
    mst = 0

    while pq:
        w, u = heapq.heappop(pq)

        if vis[u]:
            continue

        vis[u] = True
        mst += w

        for v, wt in adj[u]:
            if not vis[v]:
                heapq.heappush(pq, (wt, v))

    return mst


# Example usage
n = 4
adj = {
    0: [(1,10),(2,6),(3,5)],
    1: [(0,10),(3,15)],
    2: [(0,6),(3,4)],
    3: [(0,5),(1,15),(2,4)]
}

print(prim(n, adj))