import heapq


class MinHeap:
    def __init__(self, items=tuple()):
        self._heap = list(items)
        heapq.heapify(self._heap)

    def push(self, val):
        heapq.heappush(self._heap, val)

    def pop(self):
        return heapq.heappop(self._heap)

    def pushpop(self, val):
        return heapq.heappushpop(self._heap, val)

    def clear(self):
        self._heap.clear()

    def __iter__(self):
        return iter(self._heap)

    def __bool__(self):
        return bool(self._heap)

    def __len__(self):
        return len(self._heap)
