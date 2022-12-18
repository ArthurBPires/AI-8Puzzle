#!/usr/bin/python
# -*- coding: utf-8 -*-
ESQUERDA = "esquerda"
DIREITA = "direita"
ABAIXO = "abaixo"
ACIMA = "acima"
VAZIO = "_"
ESTADO_FINAL = "12345678_"
g_numero_expandidos = 0

from estrutura_dados import Pilha as Pilha
from estrutura_dados import Fila as Fila
from estrutura_dados import FilaPrioridades as FilaPrioridades
import time

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

def swap(estado, i1, i2):
    estado = list(estado)
    estado[i1], estado[i2] = estado[i2], estado[i1]
    return ''.join(estado)

def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    sucessores = []
    pos_vazio = estado.find('_')

    if pos_vazio - 3 >= 0:
        sucessores.append(("acima", swap(estado, pos_vazio, pos_vazio - 3)))
    if pos_vazio + 3 < 9:
        sucessores.append(("abaixo", swap(estado, pos_vazio, pos_vazio + 3)))    
    if pos_vazio % 3 == 0:
        sucessores.append(("direita", swap(estado, pos_vazio, pos_vazio + 1)))
    elif pos_vazio % 3 == 1:
        sucessores.append(("direita", swap(estado, pos_vazio, pos_vazio + 1)))
        sucessores.append(("esquerda", swap(estado, pos_vazio, pos_vazio - 1)))
    elif pos_vazio % 3 == 2:
        sucessores.append(("esquerda", swap(estado, pos_vazio, pos_vazio - 1)))

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
    
    novo_custo = pai.custo + 1
    movimentos = sucessor(pai.estado)

    filhos = []
    for (acao, estado) in movimentos:
        filho = Nodo(estado, pai, acao, novo_custo)

        if pai.pai is not None: #nodo não é raiz
            if estado == pai.pai.estado:#sucessor é igual ao movimento anterior. não adiciona na lista de filhos
                pass
            else:
                filhos.append(filho)
        else:
            filhos.append(filho)

    return filhos

def caminho(node_final):
    f = Pilha()
    caminho = []

    while node_final.pai != None:
        f.push((node_final.acao)) #f.push((node_final.estado,node_final.acao))
        node_final = node_final.pai
    
    while f.items:
        caminho.append(f.pop())
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

    fronteira = Fila()
    fronteira.enfileira(Nodo(estado,None,None,0))

    while fronteira.items:
        nodo = fronteira.desenfileira()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                fronteira.enfileira(n)
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

    fronteira = Pilha()
    fronteira.push(Nodo(estado,None,None,0))

    while fronteira.items:
        nodo = fronteira.pop()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                fronteira.push(n)
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

def calcula_heuristica_hamming(estado):
    h = 0
    if estado[0] != "1": 
        h += 1
    if estado[1] != "2": 
        h += 1
    if estado[2] != "3": 
        h += 1
    if estado[3] != "4": 
        h += 1
    if estado[4] != "5": 
        h += 1
    if estado[5] != "6": 
        h += 1
    if estado[6] != "7": 
        h += 1
    if estado[7] != "8": 
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

    fronteira = FilaPrioridades()
    fronteira.enfileira(calcula_heuristica_hamming(estado), Nodo(estado,None,None,0))

    while fronteira.items:
        f, nodo = fronteira.desenfileira()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = calcula_heuristica_hamming(n.estado)
                    fronteira.enfileira(custo + n.custo, n)
    return None

def calcula_heuristica_manhattan(estado):
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

    fronteira = FilaPrioridades()
    fronteira.enfileira(calcula_heuristica_manhattan(estado), Nodo(estado,None,None,0))

    while fronteira.items:
        f, nodo = fronteira.desenfileira()
        if nodo.estado == ESTADO_FINAL:
            return caminho(nodo)
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            vizinhos = expande(nodo)
            for n in vizinhos:
                    custo = calcula_heuristica_manhattan(n.estado)
                    fronteira.enfileira(custo + n.custo, n)
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
