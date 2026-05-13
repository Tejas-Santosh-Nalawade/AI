from collections  import defaultdict, deque

class Graph:        
    def __init__(self):
        # Adjacent List is made for the graph 
        self.graph = defaultdict(list)

    def addEdge(self, u ,v):    
        self.graph[u].append(v)

    def BFS(self, s):
        # visited set 
        visited = set()
        # Deque 
        queue = deque()

        visited.add(s)
        queue.append(s)

        while queue:
            s= queue.popleft()
            print(s, end=" ")
        
            for i in self.graph[s]:
                if i not in  visited:
                        queue.append(i)
                        visited.add(i)

if __name__ == '__main__':
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 2)
    g.addEdge(2, 4)
    g.addEdge(1, 3)
    g.addEdge(3, 4)

    print("BFS from vetex 2")
    g.BFS(0)
