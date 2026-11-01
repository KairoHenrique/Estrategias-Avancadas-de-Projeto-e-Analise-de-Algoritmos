"""
Testes unitários do APPROX-TSP-TOUR via MST-PRIM (Issues #11 e #50).
Verifica a árvore geradora mínima, a validade do tour e o fator 2 em instâncias euclidianas.
"""

import pytest

from src.approximation import mst_prim, preorder_walk, approx_tsp_tour
from src.exact import tsp_held_karp, calculate_tour_cost
from src.generators import generate_euclidean_tsp_instance
from src.verification import verify_tsp_certificate

EPS = 1e-9


class TestMSTPrim:
    def test_square(self):
        """Quadrado de lado 1: MST tem 3 arestas de peso 1 (custo 3)."""
        s = 2 ** 0.5
        d = [
            [0, 1, s, 1],
            [1, 0, 1, s],
            [s, 1, 0, 1],
            [1, s, 1, 0],
        ]
        parent, cost = mst_prim(d, root=0)
        assert cost == pytest.approx(3.0)
        assert parent[0] is None
        assert sum(p is None for p in parent) == 1

    def test_mst_is_lower_bound_of_optimum(self):
        """c(T) <= c(H*): base da prova do fator 2."""
        for seed in range(5):
            m = generate_euclidean_tsp_instance(8, seed=seed).distance_matrix
            _, mst_cost = mst_prim(m)
            _, opt = tsp_held_karp(m)
            assert mst_cost <= opt + EPS

    def test_disconnected_graph_raises(self):
        inf = float("inf")
        d = [[0, inf], [inf, 0]]
        with pytest.raises(ValueError):
            mst_prim(d)

    def test_invalid_root(self):
        m = generate_euclidean_tsp_instance(4, seed=1).distance_matrix
        with pytest.raises(ValueError):
            mst_prim(m, root=10)


class TestPreorderWalk:
    def test_simple_tree(self):
        """Árvore 0 -> {1, 2}, 1 -> {3}: pré-ordem = [0, 1, 3, 2]."""
        parent = [None, 0, 0, 1]
        assert preorder_walk(parent, 0) == [0, 1, 3, 2]


class TestApproxTSPTour:
    def test_trivial_sizes(self):
        assert approx_tsp_tour([[0.0]]) == ([0], 0.0)
        tour, cost = approx_tsp_tour([[0, 5], [5, 0]])
        assert sorted(tour) == [0, 1]
        assert cost == pytest.approx(10.0)

    def test_tour_is_valid_hamiltonian_cycle(self):
        """Critério da Issue #50: o tour é uma permutação válida das cidades."""
        for n in [3, 5, 10, 25]:
            m = generate_euclidean_tsp_instance(n, seed=n).distance_matrix
            tour, cost = approx_tsp_tour(m)
            assert sorted(tour) == list(range(n))
            assert tour[0] == 0
            assert cost == pytest.approx(calculate_tour_cost(m, tour))
            assert verify_tsp_certificate(m, tour, cost).is_valid

    def test_factor_two_against_optimum(self):
        """Critério da Issue #50: c(H) <= 2 · c(H*) em instâncias euclidianas."""
        for n in [4, 6, 8, 9]:
            for seed in range(5):
                m = generate_euclidean_tsp_instance(n, seed=1000 * n + seed).distance_matrix
                _, approx_cost = approx_tsp_tour(m)
                _, opt_cost = tsp_held_karp(m)
                assert opt_cost - EPS <= approx_cost <= 2 * opt_cost + EPS

    def test_tour_at_most_twice_mst(self):
        """c(H) <= 2 · c(T) (desigualdade triangular nos atalhos)."""
        m = generate_euclidean_tsp_instance(30, seed=5).distance_matrix
        _, mst_cost = mst_prim(m)
        _, approx_cost = approx_tsp_tour(m)
        assert approx_cost <= 2 * mst_cost + EPS

    def test_custom_root(self):
        m = generate_euclidean_tsp_instance(7, seed=2).distance_matrix
        tour, _ = approx_tsp_tour(m, root=3)
        assert tour[0] == 3
        assert sorted(tour) == list(range(7))

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            approx_tsp_tour([])
        with pytest.raises(ValueError):
            approx_tsp_tour([[0, 1], [1]])
        with pytest.raises(ValueError):
            approx_tsp_tour([[0, 1], [1, 0]], root=-1)
