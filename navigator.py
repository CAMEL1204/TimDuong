class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, distance, node_idx):
        self.heap.append([distance, node_idx])
        i = len(self.heap) - 1
        while i > 0 and self.heap[i][0] < self.heap[(i - 1)//2][0]:
            self.heap[i], self.heap[(i - 1)//2] = self.heap[(i - 1)//2], self.heap[i]
            i = (i - 1) // 2

    def pop(self):
        if len(self.heap) == 0:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_item = self.heap.pop()

        i = 0
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

        return min_item

class Navigator:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start_id, end_id):
        n = len(self.graph.nodes)
        distances = [float('inf')] * n
        previous = [-1] * n
        distances[start_id] = 0

        pq = MinHeap()
        pq.push(0, start_id)

        while len(pq.heap) > 0:
            current_item = pq.pop()
            current_dist = current_item[0]
            u = current_item[1]

            if u == end_id:
                break

            if current_dist > distances[u]:
                continue

            for edges in self.graph.getNeighbors(u):
                v = edges.to_node
                new_dist = current_dist + edges.weight

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    pq.push(new_dist, v)

        return distances, previous

    def getPath(self, start_id, end_id, previous):
        path = []
        current = end_id

        while current != -1:
            path.append(current)
            current = previous[current]

        n = len(path)
        for i in range(n // 2):
            path[i], path[n - i - 1] = path[n - i - 1], path[i]

        return path