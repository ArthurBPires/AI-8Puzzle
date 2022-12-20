#!/usr/bin/python
# -*- coding: utf-8 -*-
ESQUERDA = "esquerda"
DIREITA = "direita"
ABAIXO = "abaixo"
ACIMA = "acima"
VAZIO = "_"
ESTADO_FINAL = "12345678_"
g_numero_expandidos = 0

import time

from queue import LifoQueue
from collections import deque
from queue import PriorityQueue

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

    def __le__(self, other):
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
    sucessores = []
    posicao_vazio = estado.find(VAZIO)

    if posicao_vazio != 0 and posicao_vazio != 1 and posicao_vazio != 2:
        sucessores.append(("acima", mover(estado, posicao_vazio, posicao_vazio - 3)))
    if posicao_vazio != 6 and posicao_vazio != 7 and posicao_vazio != 8:
        sucessores.append(("abaixo", mover(estado, posicao_vazio, posicao_vazio + 3)))    
    if posicao_vazio != 2 and posicao_vazio != 5 and posicao_vazio != 8:
        sucessores.append(("direita", mover(estado, posicao_vazio, posicao_vazio + 1)))
    if posicao_vazio != 0 and posicao_vazio != 3 and posicao_vazio != 6:
        sucessores.append(("esquerda", mover(estado, posicao_vazio, posicao_vazio - 1)))

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

    
    novo_custo = nodo.custo + 1
    movimentos = sucessor(nodo.estado)

    filhos = []
    for (acao, estado) in movimentos:
        filho = Nodo(estado, nodo, acao, novo_custo)

        if nodo.pai: #não é raiz
            if estado == nodo.pai.estado: #se movimento sucessor é igual ao anterior, não é adicionado aos filhos
                pass
            else:
                filhos.append(filho)
        else:
            filhos.append(filho)

    return filhos


def caminho(node_final):

    #monta o caminho até a solução encontrada

    pilha = LifoQueue()
    caminho = []
    node = node_final

    while node.pai: #do nodo solução até o nodo raiz
        pilha.put((node.acao))
        node = node.pai
    
    while not pilha.empty():
        caminho.append(pilha.get())
    return caminho


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
            return caminho(nodo)
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
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                fronteira.put(n)
    return None

def _tem_solucao(estado):
    inversoes = 0
    for i, valor in enumerate(estado):
        if valor == VAZIO:
            continue
        for k, posterior in enumerate(estado):
            if posterior == VAZIO:
                continue
            if k > i:
                if valor > posterior:
                    inversoes += 1
    return (inversoes % 2 == 0)

def calcula_hamming(estado):
    h = 0
    for n in range(8):
        if estado[n] != str(n):
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
    if not _tem_solucao(estado):
        return None

    explorados = set()

    fronteira = PriorityQueue()
    fronteira.put((calcula_hamming(estado), Nodo(estado,None,None,0)))

    while fronteira:
        f, nodo = fronteira.get()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = calcula_hamming(n.estado)
                    fronteira.put((custo + n.custo, n))
    return None

def calcula_manhattan(estado):
    h = 0
    for i, valor in enumerate(estado):
        if valor == VAZIO:
            continue
        valor_int = int(valor)
        valor_x = i % 3
        valor_y = i // 3

        final_x = (valor_int-1) % 3
        final_y = (valor_int-1) // 3

        delta_x = abs(final_x - valor_x)
        delta_y = abs(final_y - valor_y)
        delta = delta_x + delta_y
        h += delta
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
    if not _tem_solucao(estado):
        return None

    explorados = set()

    fronteira = PriorityQueue()
    fronteira.put((calcula_manhattan(estado), Nodo(estado,None,None,0)))

    while fronteira:
        f, nodo = fronteira.get()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = calcula_manhattan(n.estado)
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
