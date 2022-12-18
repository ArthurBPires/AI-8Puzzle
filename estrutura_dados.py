from collections import deque
from queue import PriorityQueue


class Fila():
    def __init__(self):
        self.items = deque()

    def enfileira(self, item):
        self.items.append(item)
    
    def desenfileira(self):
        return self.items.popleft()

class FilaPrioridades():
    def __init__(self):
        self.items = PriorityQueue()

    def enfileira(self, prioridade:int, item):
        self.items.put_nowait((prioridade, item))
    
    def desenfileira(self):
        return self.items.get()