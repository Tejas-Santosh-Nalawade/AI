class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def unite(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True
n = 4
edges = [(10,0,1),(6,0,2),(5,0,3),(15,1,3),(4,2,3)]
edges.sort()
dsu = DSU(n)
mst = 0
for w,u,v in edges:
    if dsu.unite(u,v):
        mst += w
print(mst)