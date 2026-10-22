"""
Implementação exata do Problema do Caixeiro-Viajante (Traveling Salesperson Problem - TSP).
Capítulo 34 (NP-Completude) e Capítulo 35 (Algoritmos de Aproximação).

Definição:
Dado um grafo completo ponderado representado por uma matriz de distâncias D de ordem n x n,
o objetivo é encontrar um circuito hamiltoniano (tour) que visite cada vértice exatamente uma vez
e retorne à cidade inicial, minimizando a soma das distâncias percorridas.

Algoritmos implementados:
1. Força Bruta por permutações:
   Fixa a cidade inicial no vértice 0 (elimina simetria cíclica) e avalia todas as (n - 1)!
   rotas possíveis.
   Complexidade de Tempo: Θ((n - 1)! * n)
   Complexidade de Espaço: O(n)

2. Held-Karp (Programação Dinâmica com Máscara de Bits):
   Resolve por subproblemas sobre subconjuntos de cidades S ⊆ V e última cidade visitada j ∈ S.
   Complexidade de Tempo: Θ(n^2 * 2^n)
   Complexidade de Espaço: Θ(n * 2^n)
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, List, Optional, Tuple


def _validate_distance_matrix(distance_matrix: List[List[float]]) -> int:
    """Valida a integridade da matriz de distâncias."""
    if not isinstance(distance_matrix, list) or not distance_matrix:
        raise ValueError("A matriz de distâncias não pode ser vazia.")

    n = len(distance_matrix)
    for i, row in enumerate(distance_matrix):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"Linha {i} tem comprimento inválido ({len(row) if isinstance(row, list) else 'inválida'}). Esperado: {n} (matriz quadrada).")
        for j, val in enumerate(row):
            if not isinstance(val, (int, float)):
                raise TypeError(f"Elemento na posição ({i}, {j}) não é numérico: {val}")
            if math.isnan(val):
                raise ValueError(f"Elemento na posição ({i}, {j}) é NaN.")
    return n


def calculate_tour_cost(distance_matrix: List[List[float]], tour: List[int]) -> float:
    """
    Calcula o custo total de um ciclo TSP.
    Soma D[tour[i]][tour[i+1]] para 0 <= i < n-1 mais o retorno D[tour[n-1]][tour[0]].
    Executa em tempo O(n).
    """
    n = _validate_distance_matrix(distance_matrix)
    if len(tour) != n:
        raise ValueError(f"Tamanho do tour ({len(tour)}) não corresponde ao número de cidades ({n}).")
    if set(tour) != set(range(n)):
        raise ValueError("O tour deve ser uma permutação válida de todas as cidades {0, ..., n-1}.")

    if n <= 1:
        return 0.0

    total_cost = 0.0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        total_cost += distance_matrix[u][v]
    return float(total_cost)


def tsp_brute_force(distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
    """
    Resolve o TSP de forma exata avaliando todas as (n - 1)! permutações.
    Fixa o vértice inicial em 0 para quebrar a simetria de rotação.

    Complexidade:
        Tempo: Θ((n - 1)! * n)
        Espaço: O(n)

    Args:
        distance_matrix: Matriz quadrada n x n com as distâncias entre pares de cidades.

    Returns:
        (melhor_tour, custo_minimo): Tupla com a rota ótima encontrada e seu custo.

    Raises:
        ValueError: Se a matriz não for quadrada ou for vazia.
        TypeError: Se contiver tipos não numéricos.
    """
    n = _validate_distance_matrix(distance_matrix)

    if n == 1:
        return [0], 0.0
    if n == 2:
        cost = distance_matrix[0][1] + distance_matrix[1][0]
        return [0, 1], float(cost)

    best_tour: Optional[List[int]] = None
    min_cost = float("inf")

    # Fixa o vértice 0 e permuta os vértices {1, 2, ..., n-1}
    other_cities = list(range(1, n))
    for perm in itertools.permutations(other_cities):
        tour = [0] + list(perm)
        # Calcula o custo da rota
        current_cost = 0.0
        valid = True
        for i in range(n):
            u = tour[i]
            v = tour[(i + 1) % n]
            edge_dist = distance_matrix[u][v]
            if edge_dist == float("inf"):
                valid = False
                break
            current_cost += edge_dist

        if valid and current_cost < min_cost:
            min_cost = current_cost
            best_tour = tour

    if best_tour is None:
        raise ValueError("Nenhum tour hamiltoniano viável foi encontrado na matriz fornecida.")

    return best_tour, float(min_cost)


def tsp_held_karp(distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
    r"""
    Resolve o TSP de forma exata usando o algoritmo de Held-Karp (1962).
    Utiliza Programação Dinâmica com representação de subconjuntos por máscara de bits.

    Subproblema:
        C(S, j): Custo mínimo de um caminho que inicia na cidade 0, visita todos os
                 vértices do subconjunto S exatamente uma vez e termina no vértice j ∈ S.

    Recorrência:
        C({0}, 0) = 0
        C(S, j) = min { C(S \ {j}, i) + D[i][j] }, para todo i ∈ S, i != j.

    Tour ótimo final:
        min { C(V, j) + D[j][0] }, para todo j ∈ V \ {0}.

    Complexidade:
        Tempo: Θ(n^2 * 2^n)
        Espaço: Θ(n * 2^n)

    Args:
        distance_matrix: Matriz quadrada n x n.

    Returns:
        (melhor_tour, custo_minimo): Tour ótimo e o menor custo.
    """
    n = _validate_distance_matrix(distance_matrix)

    if n == 1:
        return [0], 0.0
    if n == 2:
        cost = distance_matrix[0][1] + distance_matrix[1][0]
        return [0, 1], float(cost)

    # memo[(mask, last_vertex)] = (min_cost, predecessor)
    # mask: bitmask de n bits onde bit i = 1 indica que o vértice i pertence ao subconjunto
    memo: Dict[Tuple[int, int], Tuple[float, Optional[int]]] = {}

    # Caso base: conjunto apenas com a cidade 0 (mask = 1 << 0 = 1)
    memo[(1, 0)] = (0.0, None)

    # Itera sobre os tamanhos de subconjuntos k = 2, 3, ..., n
    all_other_cities = list(range(1, n))
    for size in range(2, n + 1):
        for subset in itertools.combinations(all_other_cities, size - 1):
            # Constrói a máscara incluindo a cidade 0 e as cidades da combinação
            mask = 1
            for city in subset:
                mask |= (1 << city)

            for j in subset:
                prev_mask = mask ^ (1 << j)
                best_cost = float("inf")
                best_prev = None

                # Candidato i pode ser 0 (se size == 2) ou qualquer elemento de subset exceto j
                candidates = [0] if size == 2 else [c for c in subset if c != j]
                for i in candidates:
                    if (prev_mask, i) in memo:
                        cost = memo[(prev_mask, i)][0] + distance_matrix[i][j]
                        if cost < best_cost:
                            best_cost = cost
                            best_prev = i

                memo[(mask, j)] = (best_cost, best_prev)

    # Fecha o ciclo retornando à cidade 0 a partir de qualquer cidade final j
    full_mask = (1 << n) - 1
    min_total_cost = float("inf")
    best_last_city: Optional[int] = None

    for j in range(1, n):
        if (full_mask, j) in memo:
            cost = memo[(full_mask, j)][0] + distance_matrix[j][0]
            if cost < min_total_cost:
                min_total_cost = cost
                best_last_city = j

    if best_last_city is None or min_total_cost == float("inf"):
        raise ValueError("Nenhum tour viável encontrado pela programação dinâmica.")

    # Reconstrói a rota ótima a partir dos predecessores gravados
    tour = []
    curr_mask = full_mask
    curr_city = best_last_city

    while curr_city is not None:
        tour.append(curr_city)
        prev_city = memo[(curr_mask, curr_city)][1]
        curr_mask = curr_mask ^ (1 << curr_city)
        curr_city = prev_city

    # Inverte para que inicie em 0 e termine na última cidade antes de fechar em 0
    tour.reverse()

    return tour, float(min_total_cost)
