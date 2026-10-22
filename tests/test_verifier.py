"""
Testes unitários para os Verificadores de Certificado em Tempo Polinomial (Issues #10 e #48).
Valida a formalização da classe NP: verificação determinística e polinomial de testemunhas.
"""

import pytest

from src.verification import (
    verify_vertex_cover_certificate,
    verify_tsp_certificate,
)
from src.generators import (
    Graph,
    generate_complete_graph,
    generate_cycle_graph,
    generate_star_graph,
    generate_petersen_graph,
    generate_euclidean_tsp_instance,
)
from src.exact import (
    vertex_cover_brute_force,
    tsp_held_karp,
)


class TestVertexCoverVerifier:
    def test_valid_certificate(self):
        """Certificado ótimo do grafo de Petersen deve ser aceito para k = 6."""
        petersen = generate_petersen_graph()
        opt_cover, opt_size = vertex_cover_brute_force(petersen)
        res = verify_vertex_cover_certificate(petersen, opt_cover, k=opt_size)
        assert res.is_valid is True
        assert bool(res) is True

    def test_valid_superset_within_k(self):
        """Qualquer superconjunto que cubra todas as arestas com tamanho <= k é válido."""
        c5 = generate_cycle_graph(5)
        # Cobertura ótima tem tamanho 3 (ex: {0, 2, 3})
        # Fornecemos 4 vértices {0, 1, 2, 3} com k = 4
        res = verify_vertex_cover_certificate(c5, [0, 1, 2, 3], k=4)
        assert res.is_valid is True

    def test_rejected_when_cardinality_exceeds_k(self):
        """Rejeita certificado cujo tamanho é maior que o limite k estipulado."""
        c5 = generate_cycle_graph(5)
        # {0, 1, 2, 3} cobre todas as arestas, mas k = 3
        res = verify_vertex_cover_certificate(c5, [0, 1, 2, 3], k=3)
        assert res.is_valid is False
        assert "excede o limite k" in res.reason

    def test_rejected_when_edge_is_uncovered(self):
        """Rejeita certificado que deixa aresta sem cobertura, mesmo se |C| <= k."""
        c5 = generate_cycle_graph(5)
        # {0, 1} deixa as arestas (2, 3), (3, 4), (4, 0) descobertas
        res = verify_vertex_cover_certificate(c5, [0, 1], k=3)
        assert res.is_valid is False
        assert "não é coberta" in res.reason

    def test_rejected_out_of_bounds_vertex(self):
        """Rejeita certificado com vértice inexistente."""
        g = generate_complete_graph(4)
        res = verify_vertex_cover_certificate(g, [0, 1, 99], k=3)
        assert res.is_valid is False
        assert "não pertence ao conjunto de vértices" in res.reason

    def test_invalid_parameters(self):
        g = generate_star_graph(4)
        with pytest.raises(TypeError):
            verify_vertex_cover_certificate("grafo_invalido", [0], 1)
        with pytest.raises(ValueError):
            verify_vertex_cover_certificate(g, [0], -1)


class TestTSPVerifier:
    def test_valid_optimal_tsp_certificate(self):
        """Certificado ótimo obtido via Held-Karp deve ser validado para max_cost = OPT."""
        tsp_inst = generate_euclidean_tsp_instance(num_cities=6, seed=42)
        opt_tour, opt_cost = tsp_held_karp(tsp_inst.distance_matrix)

        res = verify_tsp_certificate(tsp_inst.distance_matrix, opt_tour, max_cost=opt_cost)
        assert res.is_valid is True
        assert bool(res) is True

    def test_accepted_when_cost_strictly_below_limit(self):
        """Aceita certificado quando o custo do tour é menor que o limite max_cost."""
        tsp_inst = generate_euclidean_tsp_instance(num_cities=5, seed=12)
        opt_tour, opt_cost = tsp_held_karp(tsp_inst.distance_matrix)

        res = verify_tsp_certificate(tsp_inst.distance_matrix, opt_tour, max_cost=opt_cost + 50.0)
        assert res.is_valid is True

    def test_rejected_when_cost_exceeds_limit(self):
        """Rejeita se o custo do tour superar o limitante max_cost."""
        tsp_inst = generate_euclidean_tsp_instance(num_cities=5, seed=12)
        opt_tour, opt_cost = tsp_held_karp(tsp_inst.distance_matrix)

        res = verify_tsp_certificate(tsp_inst.distance_matrix, opt_tour, max_cost=opt_cost - 1.0)
        assert res.is_valid is False
        assert "excede o limite estipulado" in res.reason

    def test_rejected_when_cities_are_missing(self):
        """Rejeita tour incompleto que não visita todas as cidades."""
        matrix = [
            [0.0, 1.0, 2.0],
            [1.0, 0.0, 3.0],
            [2.0, 3.0, 0.0],
        ]
        res = verify_tsp_certificate(matrix, [0, 1], max_cost=100.0)
        assert res.is_valid is False
        assert "contém 2 cidades, mas o grafo possui 3" in res.reason

    def test_rejected_duplicate_city(self):
        """Rejeita tour que repete uma mesma cidade."""
        matrix = [
            [0.0, 1.0, 2.0],
            [1.0, 0.0, 3.0],
            [2.0, 3.0, 0.0],
        ]
        res = verify_tsp_certificate(matrix, [0, 1, 1], max_cost=100.0)
        assert res.is_valid is False
        assert "aparece repetida" in res.reason

    def test_rejected_out_of_range_city(self):
        """Rejeita cidade inexistente."""
        matrix = [
            [0.0, 1.0],
            [1.0, 0.0],
        ]
        res = verify_tsp_certificate(matrix, [0, 5], max_cost=100.0)
        assert res.is_valid is False
        assert "fora do domínio" in res.reason

    def test_invalid_verifier_inputs(self):
        with pytest.raises(ValueError):
            verify_tsp_certificate([], [0], 10.0)
        with pytest.raises(TypeError):
            verify_tsp_certificate([[0]], "não_é_uma_lista", 10.0)
