"""
Verificadores de Certificado em Tempo Polinomial (Classe NP).
Capítulo 34: NP-Completude (Cormen et al.).

Conceito Teórico:
A classe NP não significa 'Não Polinomial', mas sim 'Polinomial Não-Determinístico'.
Equivalentemente, NP é a classe de linguagens onde qualquer instância positiva (x ∈ L)
possui um certificado (testemunha) c de tamanho polinomial que pode ser verificado
por um algoritmo determinístico em tempo polinomial (|x|^O(1)).

Enquanto ENCONTRAR a cobertura mínima ou o tour ótimo requer tempo exponencial
no pior caso (salvo se P = NP), VERIFICAR se um candidato fornecido satisfaz os
requisitos do problema de decisão executa em tempo estritamente polinomial:
- Cobertura de Vértices: O(|V| + |E|)
- Caixeiro-Viajante (TSP): O(n)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Set, Tuple

from ..generators.instances import Graph


@dataclass
class VerificationResult:
    """Resultado detalhado da validação de um certificado polinomial."""
    is_valid: bool
    reason: str
    metric_value: Optional[float] = None
    threshold: Optional[float] = None

    def __bool__(self) -> bool:
        return self.is_valid


def verify_vertex_cover_certificate(
    graph: Graph,
    certificate: Iterable[int],
    k: int
) -> VerificationResult:
    """
    Verificador em tempo polinomial para o problema de decisão da Cobertura de Vértices:
    Instância: Grafo G = (V, E) e limite k ∈ ℕ.
    Pergunta: Existe um subconjunto C ⊆ V com |C| <= k que cobre todas as arestas de E?
    Certificado: Conjunto de vértices C.

    Complexidade:
        Tempo: O(|V| + |E|) — Estritamente polinomial (linear na entrada).
        Espaço: O(|V|) para indexação em tabela hash / conjunto.

    Args:
        graph: Instância de Graph com V vértices e E arestas.
        certificate: Coleção de vértices candidata à cobertura.
        k: Limite máximo aceitável para o tamanho da cobertura (|C| <= k).

    Returns:
        VerificationResult com status booleano e justificativa técnica.

    Raises:
        TypeError: Se graph não for uma instância de Graph.
        ValueError: Se k for negativo.
    """
    if not isinstance(graph, Graph):
        raise TypeError(f"O parâmetro 'graph' deve ser uma instância de Graph, recebido {type(graph).__name__}")
    if k < 0:
        raise ValueError(f"O parâmetro 'k' deve ser um inteiro >= 0, recebido {k}")

    # Converte o certificado para conjunto (hash set para buscas O(1))
    cert_set = set(certificate)

    # Verificação 1: Tamanho do certificado não pode exceder k
    if len(cert_set) > k:
        return VerificationResult(
            is_valid=False,
            reason=f"Certificado inválido: cardinalidade |C| = {len(cert_set)} excede o limite k = {k}.",
            metric_value=float(len(cert_set)),
            threshold=float(k),
        )

    # Verificação 2: Todos os vértices do certificado devem existir no grafo (0 <= v < |V|)
    for v in cert_set:
        if not isinstance(v, int) or v < 0 or v >= graph.num_vertices:
            return VerificationResult(
                is_valid=False,
                reason=f"Certificado inválido: vértice {v} não pertence ao conjunto de vértices do grafo [0, {graph.num_vertices - 1}].",
                metric_value=float(len(cert_set)),
                threshold=float(k),
            )

    # Verificação 3: Todas as arestas (u, v) ∈ E devem ser incidentes a pelo menos um vértice de C
    for u, v in graph.edges:
        if u not in cert_set and v not in cert_set:
            return VerificationResult(
                is_valid=False,
                reason=f"Certificado inválido: aresta ({u}, {v}) não é coberta pelo certificado fornecido.",
                metric_value=float(len(cert_set)),
                threshold=float(k),
            )

    return VerificationResult(
        is_valid=True,
        reason=f"Certificado aceito: cobre todas as {graph.num_edges} arestas com {len(cert_set)} vértices (<= {k}).",
        metric_value=float(len(cert_set)),
        threshold=float(k),
    )


def verify_tsp_certificate(
    distance_matrix: List[List[float]],
    certificate_tour: List[int],
    max_cost: float,
    tolerance: float = 1e-7
) -> VerificationResult:
    """
    Verificador em tempo polinomial para o problema de decisão do Caixeiro-Viajante (TSP):
    Instância: Matriz de distâncias D (n x n) e limite de custo L ∈ ℝ+.
    Pergunta: Existe um tour hamiltoniano com custo total <= L?
    Certificado: Sequência ordenada de vértices P = [v0, v1, ..., vn-1].

    Complexidade:
        Tempo: O(n) — Estritamente polinomial (linear no número de cidades).
        Espaço: O(n) para validação da permutação.

    Args:
        distance_matrix: Matriz quadrada de distâncias n x n.
        certificate_tour: Sequência de cidades proposta como rota.
        max_cost: Limite máximo permitido para o custo da rota (L).
        tolerance: Margem de erro numérico para pontos flutuantes.

    Returns:
        VerificationResult com status booleano e justificativa técnica.

    Raises:
        ValueError: Se a matriz não for quadrada ou for vazia.
        TypeError: Se types de entrada forem inválidos.
    """
    if not isinstance(distance_matrix, list) or not distance_matrix:
        raise ValueError("A matriz de distâncias deve ser uma lista não vazia.")
    n = len(distance_matrix)
    for row in distance_matrix:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"A matriz de distâncias deve ser quadrada n x n (esperado {n} colunas).")

    if not isinstance(certificate_tour, (list, tuple)):
        raise TypeError("O certificado deve ser uma lista ou tupla de inteiros representando a rota.")

    # Caso especial trivial: n = 1
    if n == 1:
        if list(certificate_tour) == [0] and max_cost >= -tolerance:
            return VerificationResult(is_valid=True, reason="Tour trivial de 1 cidade aceito.", metric_value=0.0, threshold=max_cost)
        return VerificationResult(is_valid=False, reason="Tour inválido para n = 1.", metric_value=0.0, threshold=max_cost)

    # Verificação 1: Comprimento deve ser exatamente n
    if len(certificate_tour) != n:
        return VerificationResult(
            is_valid=False,
            reason=f"Certificado inválido: o tour contém {len(certificate_tour)} cidades, mas o grafo possui {n}.",
            metric_value=None,
            threshold=max_cost,
        )

    # Verificação 2: Deve ser uma permutação válida de {0, 1, ..., n-1}
    visited = set()
    for city in certificate_tour:
        if not isinstance(city, int) or city < 0 or city >= n:
            return VerificationResult(
                is_valid=False,
                reason=f"Certificado inválido: identificador de cidade {city} fora do domínio [0, {n-1}].",
                metric_value=None,
                threshold=max_cost,
            )
        if city in visited:
            return VerificationResult(
                is_valid=False,
                reason=f"Certificado inválido: cidade {city} aparece repetida no tour (não é um ciclo simples).",
                metric_value=None,
                threshold=max_cost,
            )
        visited.add(city)

    # Verificação 3: Custo total da rota (incluindo o retorno à primeira cidade)
    total_cost = 0.0
    for i in range(n):
        u = certificate_tour[i]
        v = certificate_tour[(i + 1) % n]
        dist = distance_matrix[u][v]
        if dist == float("inf") or math.isinf(dist):
            return VerificationResult(
                is_valid=False,
                reason=f"Certificado inválido: aresta ({u}, {v}) intransponível (peso infinito).",
                metric_value=float("inf"),
                threshold=max_cost,
            )
        total_cost += dist

    # Verificação 4: Custo <= max_cost
    if total_cost > max_cost + tolerance:
        return VerificationResult(
            is_valid=False,
            reason=f"Certificado rejeitado: custo do tour ({total_cost:.4f}) excede o limite estipulado ({max_cost:.4f}).",
            metric_value=float(total_cost),
            threshold=max_cost,
        )

    return VerificationResult(
        is_valid=True,
        reason=f"Certificado aceito: tour hamiltoniano válido com custo {total_cost:.4f} <= {max_cost:.4f}.",
        metric_value=float(total_cost),
        threshold=max_cost,
    )
