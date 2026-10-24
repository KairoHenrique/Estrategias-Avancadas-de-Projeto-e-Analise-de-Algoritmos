"""
Testes unitários do APPROX-VERTEX-COVER (Issues #11 e #49).
Verifica validade da cobertura e o fator de aproximação 2 contra o ótimo exato.
"""

import pytest

from src.approximation import approx_vertex_cover, approx_vertex_cover_with_matching
from src.exact import vertex_cover_branch_and_bound, is_valid_vertex_cover
from src.generators import (
    Graph,
    generate_complete_graph,
    generate_cycle_graph,
    generate_star_graph,
    generate_petersen_graph,
    generate_random_graph,
    generate_bipartite_graph,
)
from src.verification import verify_vertex_cover_certificate


class TestApproxVertexCover:
    def test_empty_graph(self):
        """Grafo sem arestas: cobertura vazia."""
        cover, size = approx_vertex_cover(Graph(num_vertices=5, edges=[]))
        assert cover == set()
        assert size == 0

    def test_single_edge(self):
        """Uma aresta: o algoritmo pega os dois extremos (pior caso, razão 2)."""
        cover, size = approx_vertex_cover(Graph(num_vertices=2, edges=[(0, 1)]))
        assert cover == {0, 1}
        assert size == 2

    def test_output_is_valid_cover_on_classic_graphs(self):
        """A saída sempre é uma cobertura válida (critério da Issue #49)."""
        graphs = [
            generate_complete_graph(6),
            generate_cycle_graph(7),
            generate_star_graph(8),
            generate_petersen_graph(),
            generate_bipartite_graph(4, 5, 0.5, seed=1),
        ]
        for g in graphs:
            cover, size = approx_vertex_cover(g)
            assert size == len(cover)
            assert is_valid_vertex_cover(g, cover)
            assert verify_vertex_cover_certificate(g, cover, size).is_valid

    def test_size_is_twice_the_matching(self):
        """|C| = 2|A| e A é um emparelhamento (arestas disjuntas)."""
        g = generate_random_graph(15, 0.3, seed=7)
        cover, matching = approx_vertex_cover_with_matching(g)
        assert len(cover) == 2 * len(matching)
        endpoints = [v for e in matching for v in e]
        assert len(endpoints) == len(set(endpoints))

    def test_matching_is_maximal(self):
        """Toda aresta do grafo toca algum vértice do emparelhamento (maximalidade)."""
        g = generate_random_graph(12, 0.4, seed=3)
        cover, _ = approx_vertex_cover_with_matching(g)
        for u, v in g.edges:
            assert u in cover or v in cover

    def test_factor_two_against_optimum(self):
        """Critério da Issue #49: |C| <= 2 · |C*| em instâncias pequenas."""
        for n in [6, 8, 10, 12]:
            for seed in range(5):
                g = generate_random_graph(n, 0.35, seed=100 * n + seed)
                _, approx_size = approx_vertex_cover(g)
                _, opt_size = vertex_cover_branch_and_bound(g)
                assert opt_size <= approx_size <= 2 * opt_size

    def test_tight_example_perfect_matching(self):
        """
        Exemplo justo (tight): k arestas disjuntas. Ótimo = k, aproximação = 2k.
        Mostra que a análise do fator 2 não pode ser melhorada.
        """
        k = 5
        g = Graph(num_vertices=2 * k, edges=[(2 * i, 2 * i + 1) for i in range(k)])
        _, approx_size = approx_vertex_cover(g)
        _, opt_size = vertex_cover_branch_and_bound(g)
        assert opt_size == k
        assert approx_size == 2 * k

    def test_deterministic(self):
        """Mesma entrada produz a mesma saída (reprodutibilidade)."""
        g = generate_random_graph(20, 0.25, seed=42)
        assert approx_vertex_cover(g) == approx_vertex_cover(g)

    def test_invalid_inputs(self):
        with pytest.raises(TypeError):
            approx_vertex_cover("não é um grafo")
        with pytest.raises(TypeError):
            approx_vertex_cover(None)
