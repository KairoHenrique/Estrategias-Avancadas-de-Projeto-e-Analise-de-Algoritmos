"""
Algoritmo de aproximação para o Caixeiro-Viajante Métrico (TSP com desigualdade triangular).
Capítulo 35.2.1 (Cormen et al.) — APPROX-TSP-TOUR via Árvore Geradora Mínima.

Pseudocódigo (Cormen):
    APPROX-TSP-TOUR(G, c)
    1  selecione um vértice r ∈ G.V para ser a raiz
    2  calcule uma árvore geradora mínima T para G a partir da raiz r
       usando MST-PRIM(G, c, r)
    3  seja H uma lista de vértices, ordenada de acordo com a primeira visita
       de cada vértice em um percurso em pré-ordem de T
    4  return o ciclo hamiltoniano H

Garantia (Teorema 35.2): para instâncias com desigualdade triangular,
APPROX-TSP-TOUR é uma 2-aproximação polinomial.
    1. Removendo uma aresta do tour ótimo H* obtém-se uma árvore geradora,
       logo c(T) <= c(H*).
    2. O passeio completo W (que percorre cada aresta de T duas vezes) custa 2·c(T).
    3. H é obtido de W pulando vértices repetidos; pela desigualdade triangular,
       atalhos não aumentam o custo: c(H) <= c(W) = 2·c(T) <= 2·c(H*).

ATENÇÃO: sem a desigualdade triangular não há garantia de fator constante
(Teorema 35.3: o TSP geral não admite ρ-aproximação polinomial, salvo P = NP).

Complexidade:
    Tempo: Θ(V²) — MST-PRIM com vetor de chaves sobre grafo completo (matriz n x n)
           + percurso em pré-ordem O(V).
    Espaço: Θ(V) além da matriz de entrada.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from ..exact.tsp import _validate_distance_matrix, calculate_tour_cost


def mst_prim(distance_matrix: List[List[float]], root: int = 0) -> Tuple[List[Optional[int]], float]:
    """
    MST-PRIM (Cormen, Seção 23.2) sobre um grafo completo dado por matriz de distâncias.

    Versão com vetor de chaves (sem heap): a cada iteração extrai o vértice fora da
    árvore com menor chave em O(V) e relaxa seus vizinhos em O(V). Para grafos
    completos (|E| = Θ(V²)) esta versão é assintoticamente ótima: Θ(V²).

    Complexidade:
        Tempo: Θ(V²)
        Espaço: Θ(V) (vetores key, parent e in_tree)

    Args:
        distance_matrix: Matriz simétrica n x n de distâncias.
        root: Vértice raiz r da árvore.

    Returns:
        (parent, custo_mst): parent[v] é o pai de v em T (None para a raiz)
        e custo_mst é a soma dos pesos das arestas de T.

    Raises:
        ValueError: Se a matriz for inválida, a raiz estiver fora do domínio
                    ou o grafo for desconexo (distâncias infinitas).
    """
    n = _validate_distance_matrix(distance_matrix)
    if not isinstance(root, int) or not (0 <= root < n):
        raise ValueError(f"Raiz {root} fora do domínio [0, {n - 1}].")

    key = [math.inf] * n               # menor peso de aresta ligando v à árvore
    parent: List[Optional[int]] = [None] * n
    in_tree = [False] * n
    key[root] = 0.0

    total_cost = 0.0
    for _ in range(n):
        # EXTRACT-MIN: vértice fora da árvore com menor chave — O(V)
        u = -1
        best = math.inf
        for v in range(n):
            if not in_tree[v] and key[v] < best:
                best = key[v]
                u = v
        if u == -1:
            raise ValueError("Grafo desconexo: não existe árvore geradora (distâncias infinitas).")

        in_tree[u] = True
        total_cost += key[u]

        # Relaxamento das arestas (u, v) — O(V)
        row = distance_matrix[u]
        for v in range(n):
            if not in_tree[v] and row[v] < key[v]:
                key[v] = row[v]
                parent[v] = u

    return parent, float(total_cost)


def preorder_walk(parent: List[Optional[int]], root: int = 0) -> List[int]:
    """
    Percurso em pré-ordem da árvore representada pelo vetor de pais.
    Filhos são visitados em ordem crescente de índice (resultado determinístico).

    Complexidade:
        Tempo: O(V)
        Espaço: O(V)
    """
    n = len(parent)
    children: List[List[int]] = [[] for _ in range(n)]
    for v in range(n):
        p = parent[v]
        if p is not None:
            children[p].append(v)

    order: List[int] = []
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        # Empilha em ordem reversa para desempilhar o menor filho primeiro
        stack.extend(reversed(children[u]))
    return order


def approx_tsp_tour(distance_matrix: List[List[float]], root: int = 0) -> Tuple[List[int], float]:
    """
    APPROX-TSP-TOUR (Cormen, Seção 35.2.1): 2-aproximação para o TSP métrico.

    Complexidade:
        Tempo: Θ(V²)
        Espaço: Θ(V)

    Args:
        distance_matrix: Matriz simétrica n x n que respeita a desigualdade triangular
                         (ex.: generate_euclidean_tsp_instance).
        root: Cidade inicial r (raiz da árvore geradora mínima).

    Returns:
        (tour, custo): mesmo formato das soluções exatas em src.exact,
        com custo <= 2 * ótimo quando a instância é métrica.

    Raises:
        ValueError: Se a matriz for inválida ou a raiz estiver fora do domínio.
        TypeError: Se a matriz contiver valores não numéricos.
    """
    n = _validate_distance_matrix(distance_matrix)
    if not isinstance(root, int) or not (0 <= root < n):
        raise ValueError(f"Raiz {root} fora do domínio [0, {n - 1}].")

    if n == 1:
        return [root], 0.0

    parent, _ = mst_prim(distance_matrix, root)      # linhas 1-2
    tour = preorder_walk(parent, root)               # linha 3
    return tour, calculate_tour_cost(distance_matrix, tour)  # linha 4
