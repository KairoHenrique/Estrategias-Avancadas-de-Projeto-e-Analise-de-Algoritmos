"""
Algoritmo de aproximação para a Cobertura de Vértices (Vertex Cover).
Capítulo 35.1 (Cormen et al.) — APPROX-VERTEX-COVER.

Pseudocódigo (Cormen):
    APPROX-VERTEX-COVER(G)
    1  C = ∅
    2  E' = G.E
    3  while E' ≠ ∅
    4      seja (u, v) uma aresta arbitrária de E'
    5      C = C ∪ {u, v}
    6      remova de E' toda aresta incidente em u ou em v
    7  return C

Garantia (Teorema 35.1): APPROX-VERTEX-COVER é uma 2-aproximação polinomial.
    As arestas escolhidas na linha 4 formam um emparelhamento maximal A
    (nenhum par de arestas de A compartilha vértice). Toda cobertura, inclusive
    a ótima C*, precisa conter ao menos um extremo de cada aresta de A, logo
    |C*| >= |A|. Como cada aresta de A acrescenta exatamente 2 vértices,
    |C| = 2|A| <= 2|C*|.

Complexidade:
    Tempo: O(|V| + |E|) — cada aresta é examinada uma única vez.
    Espaço: O(|V|) para o conjunto C.
"""

from __future__ import annotations

from typing import List, Set, Tuple

from ..generators.instances import Graph


def approx_vertex_cover_with_matching(graph: Graph) -> Tuple[Set[int], List[Tuple[int, int]]]:
    """
    Executa APPROX-VERTEX-COVER e devolve também o emparelhamento maximal A
    formado pelas arestas escolhidas (útil para a prova do fator 2 e para os diagramas).

    Implementação da linha 6: em vez de remover fisicamente as arestas incidentes
    de E', percorre-se E uma única vez e descarta-se toda aresta que já possui
    algum extremo em C (exatamente as arestas que teriam sido removidas).
    A "aresta arbitrária" da linha 4 é a próxima de graph.edges (ordem lexicográfica),
    o que torna o resultado determinístico e reprodutível.

    Complexidade:
        Tempo: O(|V| + |E|)
        Espaço: O(|V|)

    Args:
        graph: Instância de Graph.

    Returns:
        (cobertura, emparelhamento): conjunto C e a lista de arestas A escolhidas.

    Raises:
        TypeError: Se graph não for uma instância de Graph.
    """
    if not isinstance(graph, Graph):
        raise TypeError(f"Parâmetro 'graph' deve ser uma instância de Graph, recebido {type(graph).__name__}")

    cover: Set[int] = set()                     # linha 1: C = ∅
    matching: List[Tuple[int, int]] = []

    for u, v in graph.edges:                    # linhas 2-4: percorre E'
        # Aresta já coberta => teria sido removida de E' na linha 6
        if u in cover or v in cover:
            continue
        cover.add(u)                            # linha 5: C = C ∪ {u, v}
        cover.add(v)
        matching.append((u, v))

    return cover, matching                      # linha 7


def approx_vertex_cover(graph: Graph) -> Tuple[Set[int], int]:
    """
    APPROX-VERTEX-COVER (Cormen, Seção 35.1): 2-aproximação para a Cobertura de Vértices.

    Complexidade:
        Tempo: O(|V| + |E|)
        Espaço: O(|V|)

    Args:
        graph: Instância de Graph.

    Returns:
        (cobertura, tamanho): mesmo formato das soluções exatas em src.exact,
        garantindo tamanho <= 2 * ótimo.

    Raises:
        TypeError: Se graph não for uma instância de Graph.
    """
    cover, _ = approx_vertex_cover_with_matching(graph)
    return cover, len(cover)
