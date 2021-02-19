from math import floor 
from copy import deepcopy

class No:
    def __init__(self, no, cor=None, movimentacao=None, heuristica=0):
        self.val = no
        self.cor = cor
        self.mov = movimentacao
        self.heu = heuristica
    
    def __repr__(self):
        return "Grafo: {0}\nCor: {1}\nMovimentacoes: {2}\nHeuristica: {3}\n".format(self.val,self.cor,self.mov,self.heu)

def print_vertice(grafo, v, cor, pai):
    print(v)
    print(grafo[v])
    print(pai[v])
    if cor[v] == -1:
        print("branco")
    if cor[v] == 0:
        print("cinza")
    else:
        print("preto")

def troca_pecas(grafo, s, d):
    adjS = []
    adjS = deepcopy(grafo[s])
    grafo[s] = deepcopy(grafo[d])
    grafo[d] = adjS
    
    grafo[s].insert(grafo[s].index(s), d)
    grafo[s].remove(s)
    grafo[d].insert(grafo[d].index(d), s)
    grafo[d].remove(d)

    for vadjs in grafo[s]:
        if vadjs == d:
            continue
        grafo[vadjs].insert(grafo[vadjs].index(d), s)
        grafo[vadjs].remove(d)
    
    for vadjd in grafo[d]:
        if vadjd == s:
            continue
        grafo[vadjd].insert(grafo[vadjd].index(s), d)
        grafo[vadjd].remove(s)

def finalizado(grafo):
    fim = {
            0:[8,6],
            1:[4,2],
            2:[1,5,3],
            3:[2,6],
            4:[7,5,1],
            5:[4,8,6,2],
            6:[5,0,3],
            7:[8,4],
            8:[7,0,5]
    }
    if fim == grafo:
        return True
    return False

def viz_esquerda(grafo, u, v):
    adj = (grafo[v])[:]
    if adj.pop(0) != u:
        return False
    return True

def viz_baixo(grafo, u, v):
    adj = (grafo[v])[:]
    if adj.pop() != u:
        return False
    return True

def viz_direita(grafo, u, v):
    return viz_esquerda(grafo, v, u)

def viz_cima(grafo, u, v):
    return viz_baixo(grafo, v, u)

def n_pecas_deslocadas(grafo):
    qtd = 0
    '''
    esquerda = primeiro
    baixo = segundo
    direita = penultimo
    cima = ultimo
                                    1 = cima, esquerda 
    2 = direita, cima, esquerda
                                    3 = direita, cima
    4 = cima, esquerda, baixo
                                                        5 = esquerda, cima, direita, baixo
    6 = esquerda, cima, baixo
                                    7 = esquerda, baixo
    8 = esquerda, direita, baixo
                                    0 = direita, baixo
    '''
    fim = {
            0:[8,6],
            1:[4,2],
            2:[1,5,3],
            3:[2,6],
            4:[7,5,1],
            5:[4,8,6,2],
            6:[5,0,3],
            7:[8,4],
            8:[7,0,5]
    }
    for i in range(len(fim)):
        # print("{0} - {1}".format(fim[i], grafo[i]))
        if fim[i] != grafo[i]:
            if i == 1 or i == 3 or i == 7 or i == 0:
                if len(grafo[i]) > 2: # com certeza o vertice esta fora de posicao
                    qtd = qtd+1 
                else: 
                    adj = (grafo[i])[:]
                    if i == 1 and not (viz_cima(grafo,i,adj.pop(0)) and viz_esquerda(grafo,i,adj.pop())):
                        qtd = qtd+1
                    elif i == 3 and not (viz_direita(grafo,i,adj.pop(0)) and viz_cima(grafo,i,adj.pop())):
                        qtd = qtd+1
                    elif i == 7 and not (viz_esquerda(grafo,i,adj.pop(0)) and viz_baixo(grafo,i,adj.pop())):
                        qtd = qtd+1
                    elif i == 0 and not (viz_direita(grafo,i,adj.pop(0)) and viz_baixo(grafo,i,adj.pop())):
                        qtd = qtd+1
            elif i == 2 or i == 4 or i == 6 or i == 8: 
                if len(grafo[i]) != 3:
                    qtd = qtd+1
                else:
                    adj = (grafo[i])[:]
                    if i == 2 and not viz_cima(grafo,i,adj.pop(1)):
                        qtd = qtd+1
                    elif i == 4 and not viz_esquerda(grafo,i,adj.pop(1)):
                        qtd = qtd+1
                    elif i == 6 and not viz_direita(grafo,i,adj.pop(1)):
                        qtd = qtd+1
                    elif i == 8 and not viz_baixo(grafo,i,adj.pop(1)):
                        qtd = qtd+1
            else:
                if len(grafo[i]) != 4:
                    qtd = qtd+1

    return qtd

def BuscaEmLargura(grafo, vf, h=None):
    arv  = {} # cada no representa uma movimentacao; no pai significa movimentacao anterior
    fila = []
    cor  = {}
    adj  = []
    mov  = 0 # movimentacao real
    qtdma = -1

    for vertice in grafo:
        cor[vertice] = -1 # branco
    
    cor[vf] = 0 # cinza
    fila.append(vf)
    grafo_atual = grafo.copy()

    while not finalizado(grafo_atual):
        qtdma = qtdma+1
        vu = fila.pop(0)
        
        if qtdma > 0:
            no = arv[floor((qtdma-1)/2)] # movimentacao real anterior
            grafo_atual = deepcopy(no.val)
            cor = deepcopy(no.cor)
            mov = deepcopy(no.mov)
            # print("Troca entre s=%d d=%d" % (vu, 0))
            troca_pecas(grafo_atual, vu, 0)
            cor[vu] = 1 # preto
            mov = mov+1
            vu = 0
    
        adj = (grafo_atual[vu])[:] # copia das adj do vertice u

        for i in range(len(adj)):
            v = adj.pop(0)
            if cor[v] == -1: # branco
                cor[v] = 0  # cinza
                fila.append(v)
                # if h is not None:
                '''
                criar dicionario (vertice,peso)
                peso = h(0)+h(vertice)
                ordernar decrescentemente o dicionario por pesos
                retornar em forma de lista
                obs: atualizar (v,w) para cada troca feita
                '''

        arv[qtdma] = No(deepcopy(grafo_atual), cor=deepcopy(cor), movimentacao=deepcopy(mov))
        # print('Fila: {0}'.format(fila))
        # print(arv[qtdma])

    return arv[qtdma].val
        
def main():
    '''
    1 - 2 - 0 
    |   |   | 
    4 - 5 - 3
    |   |   |
    7 - 8 - 6
    '''
    qb = {0:[2,3],        # Cabeca.
          1:[4,2],        # Vizinhos do vertice 1.
          2:[1,5,0],      # Vizinhos do vertice 2.
          3:[5,6,0],      # Vizinhos do vertice 3.
          4:[7,5,1],      # Vizinhos do vertice 4.
          5:[4,8,3,2],    # Vizinhos do vertice 5.
          6:[8,3],        # Vizinhos do vertice 6.
          7:[8,4],        # Vizinhos do vertice 7.
          8:[7,6,5]       # Vizinhos do vertice 8.
    }
    
    print(n_pecas_deslocadas(qb))

    qb = BuscaEmLargura(qb, 0)

    # qb = BuscaEmLargura(qb, 0, h=dt)

    print(n_pecas_deslocadas(qb))

if __name__ == '__main__':
   main()