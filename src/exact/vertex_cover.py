"""
Implementação exata do problema de Cobertura de Vértices (Vertex Cover).
Capítulo 34 (NP-Completude) e Capítulo 35 (Algoritmos de Aproximação).

Definição:
Dado um grafo não-direcionado G = (V, E), uma cobertura de vértices é um subconjunto
C ⊆ V tal que para toda aresta (u, v) ∈ E, temos u ∈ C ou v ∈ C (ou ambos).
O problema de otimização busca uma cobertura C de tamanho mínimo |C|.

Complexidade:
- Força Bruta por enumeração de subconjuntos: O(2^|V| * |E|)
- Branch-and-Bound / Backtracking podado: O(2^k * |E|), onde k = |C*| <= |V|
Espaço adicional: O(|V|)
"""

from __future__ import annotations

import itertools
from typing import List, Optional, Set, Tuple

from ..generators.instances import Graph


def is_valid_vertex_cover(graph: Graph, candidate: Set[int]) -> bool:
    """
    Verifica se um dado conjunto candidato de vértices cobre todas as arestas do grafo.
    Executa em tempo O(|E|).
    """
    if not isinstance(graph, Graph):
        raise TypeError(f"Esperado objeto Graph, recebido {type(graph)}")
    if not isinstance(candidate, (set, frozenset)):
        candidate = set(candidate)

    for u, v in graph.edges:
        if u not in candidate and v not in candidate:
            return False
    return True


def vertex_cover_brute_force(graph: Graph) -> Tuple[Set[int], int]:
    """
    Resolve o problema da Cobertura de Vértices Mínima por força bruta exaustiva.
    Testa subconjuntos de tamanho k = 0, 1, 2, ..., |V|.
    O primeiro subconjunto válido encontrado possui cardinalidade mínima garantida.

    Complexidade:
        Tempo: O(2^|V| * |E|) no pior caso.
        Espaço: O(|V|) de memória auxiliar.

    Args:
        graph: Instância de Graph.

    Returns:
        (cobertura_minima, tamanho_minimo): Tupla com o conjunto de vértices e seu tamanho.

    Raises:
        TypeError: Se graph não for uma instância válida de Graph.
        ValueError: Se o grafo tiver estrutura inconsistente.
    """
    if not isinstance(graph, Graph):
        raise TypeError(f"Parâmetro 'graph' deve ser uma instância de Graph, recebido {type(graph).__name__}")

    # Grafo sem arestas: cobertura ótima é o conjunto vazio
    if graph.num_edges == 0:
        return set(), 0

    vertices = list(range(graph.num_vertices))

    # Testa tamanhos de k = 1 até |V|
    for k in range(1, graph.num_vertices + 1):
        for candidate_tuple in itertools.combinations(vertices, k):
            candidate = set(candidate_tuple)
            if is_valid_vertex_cover(graph, candidate):
                return candidate, k

    # Fallback teórico: todos os vértices cobrem todas as arestas
    return set(vertices), graph.num_vertices


def vertex_cover_branch_and_bound(graph: Graph) -> Tuple[Set[int], int]:
    """
    Resolve o problema da Cobertura de Vértices Mínima usando Branch-and-Bound (Backtracking).
    Em cada passo, escolhe uma aresta não-coberta (u, v). Em qualquer cobertura válida,
    ou u pertence à cobertura, ou v pertence à cobertura.
    Ramos cuja cardinalidade atual já é >= à melhor solução conhecida são podados.

    Complexidade:
        Tempo: O(2^k * |E|), onde k é o tamanho da cobertura mínima ótima.
        Espaço: O(|V|) para a pilha de recursão.

    Args:
        graph: Instância de Graph.

    Returns:
        (cobertura_minima, tamanho_minimo): Tupla com o conjunto de vértices e seu tamanho.
    """
    if not isinstance(graph, Graph):
        raise TypeError(f"Parâmetro 'graph' deve ser uma instância de Graph, recebido {type(graph).__name__}")

    if graph.num_edges == 0:
        return set(), 0

    best_cover: Set[int] = set(range(graph.num_vertices))
    best_size: int = graph.num_vertices

    # Heurística inicial para encontrar um limitante superior rápido:
    # Seleciona vértices de maior grau até cobrir todas as arestas
    uncovered = set(graph.edges)
    degrees = {i: len(graph.adjacency_list[i]) for i in range(graph.num_vertices)}
    greedy_cover: Set[int] = set()
    while uncovered:
        # Vértice que mais cobre arestas restantes
        best_v = max(degrees.keys(), key=lambda v: degrees[v])
        greedy_cover.add(best_v)
        covered_edges = {e for e in uncovered if best_v in e}
        uncovered -= covered_edges
        degrees[best_v] = -1
        for u, v in covered_edges:
            other = v if u == best_v else u
            if degrees[other] > 0:
                degrees[other] -= 1

    if is_valid_vertex_cover(graph, greedy_cover):
        best_cover = greedy_cover
        best_size = len(greedy_cover)

    # Busca em profundidade com poda
    def backtrack(current_cover: Set[int], remaining_edges: List[Tuple[int, int]]):
        nonlocal best_cover, best_size

        # Poda por limitante: se já empatou ou ultrapassou a melhor solução, descarta
        if len(current_cover) >= best_size:
            return

        # Se não restam arestas, encontramos uma cobertura válida melhor
        if not remaining_edges:
            best_cover = set(current_cover)
            best_size = len(current_cover)
            return

        # Escolhe a primeira aresta não coberta
        u, v = remaining_edges[0]

        # Ramo 1: incluir u
        next_edges_u = [e for e in remaining_edges if u not in e]
        current_cover.add(u)
        backtrack(current_cover, next_edges_u)
        current_cover.remove(u)

        # Ramo 2: incluir v (apenas se ainda for promissor)
        if len(current_cover) + 1 < best_size:
            next_edges_v = [e for e in remaining_edges if v not in e]
            current_cover.add(v)
            backtrack(current_cover, next_edges_v)
            current_cover.remove(v)

    backtrack(set(), list(graph.edges))
    return best_cover, best_size
