"""
Testes unitários para as soluções exatas do Caixeiro-Viajante (Issues #10, #46 e #47).
Testa força bruta e programação dinâmica (Held-Karp) contra instâncias com solução conhecida
e verifica a equivalência exata entre os dois métodos.
"""

import math
import pytest

from src.exact import (
    tsp_brute_force,
    tsp_held_karp,
    calculate_tour_cost,
)
from src.generators import generate_euclidean_tsp_instance


class TestTSPExact:
    def test_single_city(self):
        """Para 1 cidade, o custo é 0 e a rota é [0]."""
        matrix = [[0.0]]
        tour_bf, cost_bf = tsp_brute_force(matrix)
        tour_hk, cost_hk = tsp_held_karp(matrix)
        assert tour_bf == [0]
        assert tour_hk == [0]
        assert cost_bf == 0.0
        assert cost_hk == 0.0

    def test_two_cities(self):
        """Para 2 cidades, o custo é D[0][1] + D[1][0]."""
        matrix = [
            [0.0, 7.5],
            [7.5, 0.0]
        ]
        tour_bf, cost_bf = tsp_brute_force(matrix)
        tour_hk, cost_hk = tsp_held_karp(matrix)
        assert cost_bf == 15.0
        assert cost_hk == 15.0
        assert set(tour_bf) == {0, 1}
        assert set(tour_hk) == {0, 1}

    def test_three_cities_triangle(self):
        """Triângulo retângulo com lados 3, 4, 5. Perímetro total = 12."""
        matrix = [
            [0.0, 3.0, 4.0],
            [3.0, 0.0, 5.0],
            [4.0, 5.0, 0.0]
        ]
        tour_bf, cost_bf = tsp_brute_force(matrix)
        tour_hk, cost_hk = tsp_held_karp(matrix)
        assert math.isclose(cost_bf, 12.0)
        assert math.isclose(cost_hk, 12.0)
        assert math.isclose(calculate_tour_cost(matrix, tour_bf), 12.0)
        assert math.isclose(calculate_tour_cost(matrix, tour_hk), 12.0)

    def test_four_cities_square(self):
        """
        4 cidades formando um quadrado de lado 10 com diagonais 14.142.
        A rota ótima deve seguir o perímetro: 10 + 10 + 10 + 10 = 40.
        """
        diag = math.hypot(10, 10)
        matrix = [
            [0.0, 10.0, diag, 10.0],
            [10.0, 0.0, 10.0, diag],
            [diag, 10.0, 0.0, 10.0],
            [10.0, diag, 10.0, 0.0],
        ]
        tour_bf, cost_bf = tsp_brute_force(matrix)
        tour_hk, cost_hk = tsp_held_karp(matrix)
        assert math.isclose(cost_bf, 40.0)
        assert math.isclose(cost_hk, 40.0)
        assert math.isclose(calculate_tour_cost(matrix, tour_bf), 40.0)
        assert math.isclose(calculate_tour_cost(matrix, tour_hk), 40.0)

    def test_brute_force_and_held_karp_equivalence(self):
        """
        Gera instâncias euclidianas aleatórias e compara os custos de Força Bruta e Held-Karp.
        Ambos DEVEM produzir exatamente o mesmo valor ótimo.
        """
        for n in [4, 5, 6, 7]:
            tsp_inst = generate_euclidean_tsp_instance(num_cities=n, seed=100 + n)
            matrix = tsp_inst.distance_matrix

            tour_bf, cost_bf = tsp_brute_force(matrix)
            tour_hk, cost_hk = tsp_held_karp(matrix)

            # Verifica igualdade estrita dos custos
            assert math.isclose(cost_bf, cost_hk, rel_tol=1e-7, abs_tol=1e-7)

            # Verifica validade das rotas
            assert set(tour_bf) == set(range(n))
            assert set(tour_hk) == set(range(n))
            assert math.isclose(calculate_tour_cost(matrix, tour_bf), cost_bf, rel_tol=1e-7)
            assert math.isclose(calculate_tour_cost(matrix, tour_hk), cost_hk, rel_tol=1e-7)

    def test_held_karp_larger_instance(self):
        """Testa o Held-Karp em n = 11 (onde a força bruta é de 10! = 3.6 milhões de rotas)."""
        tsp_inst = generate_euclidean_tsp_instance(num_cities=11, seed=42)
        matrix = tsp_inst.distance_matrix
        tour_hk, cost_hk = tsp_held_karp(matrix)
        assert len(tour_hk) == 11
        assert set(tour_hk) == set(range(11))
        assert cost_hk > 0.0
        assert math.isclose(calculate_tour_cost(matrix, tour_hk), cost_hk, rel_tol=1e-7)

    def test_invalid_matrices(self):
        """Verifica tratamento de exceções com matrizes inválidas."""
        with pytest.raises(ValueError):
            tsp_brute_force([])
        with pytest.raises(ValueError):
            tsp_held_karp([])
        with pytest.raises(ValueError):
            # Matriz não retangular
            tsp_brute_force([[1, 2], [3]])
        with pytest.raises(ValueError):
            # Matriz retangular mas não quadrada (2 x 3)
            tsp_held_karp([[1, 2, 3], [4, 5, 6]])
        with pytest.raises(TypeError):
            tsp_brute_force([[1, "dois"], [3, 4]])
