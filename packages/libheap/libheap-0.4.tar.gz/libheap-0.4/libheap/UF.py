class UF:
    def __init__(self, capacity):
        self.parent = list(range(capacity))
        self.rank = [0] * capacity
        self.count = capacity

    def find(self, p):
        self.__validate(p)
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        return p

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return
        if self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        elif self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        else:
            self.parent[rootP] = rootQ
            self.rank[rootP] += 1
        self.count -= 1

    def connected_component(self):
        return self.count

    def __validate(self, p):
        n = len(self.parent)
        if p < 0 or p >= n:
            raise ValueError("index " + p + " is not between 0 and " + (n - 1))
