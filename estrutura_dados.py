from collections import deque
from queue import PriorityQueue

class Pilha ():
    def __init__(self):
        self.items = deque()
    
    def push(self,item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()

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