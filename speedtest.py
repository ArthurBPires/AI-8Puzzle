from solucao import *
import time

ESTADO_INICIAL = "2_3541687"


def teste_alg(version, initial_state):
    inicio = time.time()
    a = version(initial_state)
    print(len(a))
    fim = time.time()
    print(fim-inicio)


if __name__ == '__main__':
    print("\nDFS")
    print("custo / tempo")
    teste_alg(dfs,ESTADO_INICIAL)

    print("\nBFS")
    print("custo / tempo")
    teste_alg(bfs,ESTADO_INICIAL)

    print("\nAstar Hamming")
    print("custo / tempo")
    teste_alg(astar_hamming,ESTADO_INICIAL)

    print("\nAstar Manhattan")
    print("custo / tempo")
    teste_alg(astar_manhattan,ESTADO_INICIAL)

    