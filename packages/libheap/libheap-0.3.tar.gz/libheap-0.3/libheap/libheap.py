class Heap:
    def __init__(self, keys: list = None, min=True, compare=None):
        self.compare = compare
        # denote whether it's a min heap
        self.min = min
        if keys:
            self.pq = [0] + keys
            self.qp = dict(zip(keys, range(1, len(self.pq))))
            k = len(keys) // 2
            while k >= 1:
                self.__sink(k)
                k -= 1
        else:
            self.pq = [0]
            self.qp = {}

    def insert(self, key):
        self.pq.append(key)
        self.qp[key] = self.size()
        self.__swim(self.size())

    def pop(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        m = self.pq[1]
        self.__exch(1, self.size())
        self.pq.pop()
        self.__sink(1)
        del self.qp[m]
        return m

    def top(self):
        if self.empty():
            raise Exception('Priority queue underflow')
        return self.pq[1]

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.pq) - 1

    def delete(self, key):
        self.validate(key)
        i = self.qp[key]
        if i == self.size():
            self.pq.pop()
            del self.qp[key]
	    return
        self.__exch(i, self.size())
        self.pq.pop()
        self.__swim(i)
        self.__sink(i)
        del self.qp[key]

    def validate(self, key):
        if key not in self:
            raise ValueError("index is not in the priority queue")

    def __contains__(self, item):
        return item in self.qp

    def __compare(self, i, j):
        if self.compare:
            comp = self.compare(self.pq[i], self.pq[j]) > 0
        else:
            comp = self.pq[i] > self.pq[j]
        return comp if self.min else not comp

    def __exch(self, i, j):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def __swim(self, k):
        while k > 1 and self.__compare(k // 2, k):
            self.__exch(k, k // 2)
            k = k // 2

    def __sink(self, k):
        while 2 * k <= self.size():
            j = 2 * k
            if j < self.size() and self.__compare(j, j + 1):
                j += 1
            if not self.__compare(k, j):
                break
            self.__exch(k, j)
            k = j


# order (key,value) pairs by value
class IndexHeap(Heap):
    def __init__(self, keys: list = None, values: list = None, min=True, compare=None):
        if values or keys:
            if not (values and keys):
                raise ValueError('illegal arguments')
            self.keys = dict(zip(keys, values))
        else:
            self.keys = {}
        super().__init__(keys, min, compare)

    def pop(self):
        m = super().pop()
        key = self.keys[m]
        del self.keys[m]
        return m, key

    def top(self):
        m = super().top()
        return m, self.keys[m]

    def insert(self, key, value):
        if key in self:
            raise ValueError("index is already in the priority queue")
        super().insert(key)
        self.keys[key] = value

    def changeKey(self, key, value):
        self.validate(key)
        self.keys[key] = value
        self.__swim(self.qp[key])
        self.__sink(self.qp[key])

    def valueOf(self, key):
        self.validate(key)
        return self.keys[key]

    def delete(self, key):
        super().delete(key)
        del self.keys[key]

    def __compare(self, i, j):
        if self.compare:
            comp = self.compare(self.keys[self.pq[i]], self.keys[self.pq[j]]) > 0
        else:
            comp = self.keys[self.pq[i]] > self.keys[self.pq[j]]
        return comp if self.min else not comp
