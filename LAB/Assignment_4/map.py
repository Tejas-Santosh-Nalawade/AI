graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B']
}

colors = ['Red', 'Green', 'Blue']

result = {}

def isSafe(node, color):

    for neighbor in graph[node]:

        if neighbor in result and result[neighbor] == color:
            return False

    return True

def solve(nodeIndex):

    nodes = list(graph.keys())

    if nodeIndex == len(nodes):
        return True

    node = nodes[nodeIndex]

    for color in colors:

        if isSafe(node, color):

            result[node] = color

            if solve(nodeIndex + 1):
                return True

            del result[node]

    return False

solve(0)

print(result)