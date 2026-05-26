class Node:
    def __init__(self, id_index, name, x, y):
        self.id = id_index
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.id}, {self.name}"

class Edge:
    def __init__(self, from_id, to_id, weight):
        self.from_node = from_id
        self.to_node = to_id
        self.weight = weight

    def __repr__(self):
        return f"Edge({self.from_node} -> {self.to_node}, w = {self.weight:.2f})"

class Graph:
    def __init__(self):
        self.nodes = []
        self.adjList = []

    def addNode(self, node):
        self.nodes.append(node)
        self.adjList.append([])

    def addEdge(self, edge):
        self.adjList[edge.from_node].append(edge)

    def getNeighbors(self, node_id):
        return self.adjList[node_id]