# -*- coding: utf-8 -*-
#!/usr/bin/python

g_numero_expandidos = 0
VAZIO = "_"
ESTADO_FINAL = "12345678_"

import time

from queue import LifoQueue
from queue import PriorityQueue
from collections import deque

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado, pai, acao, custo):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __lt__(self, other):
        return False

def mover(estado, pos1, pos2):
    novo_estado = list(estado)
    novo_estado[pos1], novo_estado[pos2] = novo_estado[pos2], novo_estado[pos1]
    return ''.join(novo_estado)

def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    posicao_vazia = estado.find('_')
    sucessores = []

    if posicao_vazia >= 3:
        sucessores.append(("acima", mover(estado, posicao_vazia, posicao_vazia - 3)))
    if posicao_vazia < 6:
        sucessores.append(("abaixo", mover(estado, posicao_vazia, posicao_vazia + 3)))    
    if (posicao_vazia + 1) % 3 != 0:
        sucessores.append(("direita", mover(estado, posicao_vazia, posicao_vazia + 1)))
    if posicao_vazia % 3 != 0:
        sucessores.append(("esquerda", mover(estado, posicao_vazia, posicao_vazia - 1)))

    return sucessores


def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    global g_numero_expandidos
    g_numero_expandidos = g_numero_expandidos + 1

    pai = nodo
    filhos = []
    novo_custo = pai.custo + 1
    

    movimentos = sucessor(pai.estado)
    for (acao, estado) in movimentos:
        filho = Nodo(estado, nodo, acao, novo_custo)

        if pai.pai is not None:
            if estado == pai.pai.estado:
                pass
            else:
                filhos.append(filho)
        else:
            filhos.append(filho)

    return filhos

def sequencia_passos(node_final):
    sequencia = deque()

    while node_final.pai != None:
        sequencia.appendleft(node_final.acao)
        node_final = node_final.pai
    
    return list(sequencia)

def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """

    explorados = set()
    fronteira = deque()
    fronteira.append(Nodo(estado,None,None,0))

    while fronteira:
        nodo = fronteira.popleft()
        if nodo.estado == ESTADO_FINAL:
            return sequencia_passos(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                fronteira.append(n)
    return None


def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    explorados = set()
    fronteira = LifoQueue()
    fronteira.put(Nodo(estado,None,None,0))

    while not fronteira.empty():
        nodo = fronteira.get()
        if nodo.estado == ESTADO_FINAL:
            return sequencia_passos(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                fronteira.put(n)
    return None

def sem_solucao (estado):
    numero_inversoes = 0

    for i, valor in enumerate(estado):
        if valor == VAZIO:
            continue
        for k, proximo in enumerate(estado):
            if proximo == VAZIO:
                continue
            if k > i:
                if valor > proximo:
                    numero_inversoes += 1

    return (numero_inversoes % 2 != 0)

def heuristica_hamming(estado):
    h = 0
    
    for i in range(8):
        if estado[i] != ESTADO_FINAL[i]:
            h += 1
    return h


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if sem_solucao(estado):
        return None

    explorados = set()

    fronteira = PriorityQueue()
    fronteira.put((heuristica_hamming(estado), Nodo(estado,None,None,0)))

    while fronteira:
        f, nodo = fronteira.get()
        if nodo.estado == ESTADO_FINAL:
            return sequencia_passos(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = heuristica_hamming(n.estado)
                    fronteira.put((custo + n.custo, n))
    return None

def heuristica_manhattan(estado):
    h = 0

    for i, valor in enumerate(estado):
        if valor == VAZIO:
            continue

        x_inicial = i % 3
        y_inicial = i // 3

        x_final = (int(valor)-1) % 3
        y_final = (int(valor)-1) // 3

        delta_x = abs(x_final - x_inicial)
        delta_y = abs(y_final - y_inicial)
        
        h += delta_x + delta_y
    return h


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if sem_solucao(estado):
        return None

    explorados = set()

    fronteira = PriorityQueue()

    fronteira.put((heuristica_manhattan(estado), Nodo(estado,None,None,0)))

    while fronteira:
        a, nodo = fronteira.get()
        if nodo.estado == ESTADO_FINAL:
            return sequencia_passos(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = heuristica_manhattan(n.estado)
                    fronteira.put((custo + n.custo, n))
    return None

def testes_de_algoritmo(algoritmo, valor_inicial):

    inicio = time.time()
    resultado = algoritmo(valor_inicial)
    fim = time.time()


    custo = len(resultado)
    tempo = fim-inicio
    global g_numero_expandidos

    print(f'\n Algoritmo: {algoritmo.__name__} \n Tempo: {tempo} segundos\n Custo: {custo}\n Número de Explorados: {g_numero_expandidos} nodos')

    g_numero_expandidos = 0

def analize_algoritmos() :
    valor_inicial_de_teste = "2_3541687"
    testes_de_algoritmo(dfs,valor_inicial_de_teste)
    testes_de_algoritmo(bfs,valor_inicial_de_teste)
    testes_de_algoritmo(astar_hamming,valor_inicial_de_teste)
    testes_de_algoritmo(astar_manhattan,valor_inicial_de_teste)

#analize_algoritmos()