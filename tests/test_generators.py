"""
Testes unitários para o gerador de instâncias com semente fixa (Issue #44).
Garante reprodutibilidade, validade estrutural e respeito à desigualdade triangular.
"""

import json
import math
import pytest
from pathlib import Path

from src.generators import (
    Graph,
    TSPInstance,
    generate_random_graph,
    generate_complete_graph,
    generate_cycle_graph,
    generate_star_graph,
    generate_bipartite_graph,
    generate_petersen_graph,
    generate_euclidean_tsp_instance,
    save_graph_to_json,
    load_graph_from_json,
    save_tsp_to_json,
    load_tsp_from_json,
)


class TestGraphGenerators:
    def test_seed_reproducibility(self):
        """Verifica se a mesma semente produz grafos exatamente idênticos."""
        g1 = generate_random_graph(num_vertices=20, edge_probability=0.3, seed=12345)
        g2 = generate_random_graph(num_vertices=20, edge_probability=0.3, seed=12345)
        assert g1.num_vertices == g2.num_vertices
        assert g1.edges == g2.edges
        assert g1.adjacency_list == g2.adjacency_list

    def test_different_seeds_produce_different_graphs(self):
        """Verifica se sementes distintas geram grafos diferentes."""
        g1 = generate_random_graph(num_vertices=20, edge_probability=0.3, seed=12345)
        g2 = generate_random_graph(num_vertices=20, edge_probability=0.3, seed=54321)
        assert g1.edges != g2.edges

    def test_complete_graph(self):
        """Verifica se K_n possui n*(n-1)/2 arestas."""
        n = 6
        kn = generate_complete_graph(n)
        assert kn.num_vertices == n
        assert kn.num_edges == n * (n - 1) // 2

    def test_cycle_graph(self):
        """Verifica propriedades do grafo ciclo C_n."""
        n = 5
        cn = generate_cycle_graph(n)
        assert cn.num_vertices == n
        assert cn.num_edges == n
        for v in range(n):
            assert len(cn.adjacency_list[v]) == 2

    def test_star_graph(self):
        """Verifica grafo estrela: centro com grau n-1 e folhas com grau 1."""
        n = 7
        star = generate_star_graph(n)
        assert star.num_vertices == n
        assert star.num_edges == n - 1
        assert len(star.adjacency_list[0]) == n - 1
        for v in range(1, n):
            assert len(star.adjacency_list[v]) == 1

    def test_petersen_graph(self):
        """Verifica o grafo de Petersen (10 vértices, 15 arestas, 3-regular)."""
        petersen = generate_petersen_graph()
        assert petersen.num_vertices == 10
        assert petersen.num_edges == 15
        for v in range(10):
            assert len(petersen.adjacency_list[v]) == 3

    def test_bipartite_graph(self):
        """Verifica se todas as arestas ligam partições distintas."""
        n1, n2 = 4, 5
        bg = generate_bipartite_graph(n1, n2, edge_probability=0.7, seed=42)
        assert bg.num_vertices == n1 + n2
        for u, v in bg.edges:
            assert (u < n1 and v >= n1) or (v < n1 and u >= n1)

    def test_invalid_graph_parameters(self):
        """Validação de parâmetros incorretos."""
        with pytest.raises(ValueError):
            generate_random_graph(-1, 0.5)
        with pytest.raises(ValueError):
            generate_random_graph(10, -0.1)
        with pytest.raises(ValueError):
            generate_random_graph(10, 1.1)


class TestTSPGenerators:
    def test_tsp_seed_reproducibility(self):
        """Verifica se a mesma semente produz a mesma instância euclidiana de TSP."""
        tsp1 = generate_euclidean_tsp_instance(num_cities=15, seed=999)
        tsp2 = generate_euclidean_tsp_instance(num_cities=15, seed=999)
        assert tsp1.num_cities == tsp2.num_cities
        assert tsp1.coordinates == tsp2.coordinates
        assert tsp1.distance_matrix == tsp2.distance_matrix

    def test_triangle_inequality_holds(self):
        """Garante que a métrica euclidiana satisfaz d(i, j) <= d(i, k) + d(k, j)."""
        tsp = generate_euclidean_tsp_instance(num_cities=20, seed=42)
        D = tsp.distance_matrix
        n = tsp.num_cities
        tol = 1e-9
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    assert D[i][j] <= D[i][k] + D[k][j] + tol, (
                        f"Violou desigualdade triangular: D[{i}][{j}]={D[i][j]} > D[{i}][{k}]={D[i][k]} + D[{k}][{j}]={D[k][j]}"
                    )

    def test_distance_matrix_symmetry_and_diagonal(self):
        """Verifica se D[i][i] == 0 e D[i][j] == D[j][i]."""
        tsp = generate_euclidean_tsp_instance(num_cities=10, seed=77)
        D = tsp.distance_matrix
        for i in range(10):
            assert D[i][i] == 0.0
            for j in range(10):
                assert math.isclose(D[i][j], D[j][i], abs_tol=1e-9)

    def test_invalid_tsp_parameters(self):
        with pytest.raises(ValueError):
            generate_euclidean_tsp_instance(-5)
        with pytest.raises(ValueError):
            generate_euclidean_tsp_instance(10, width=-10.0)


class TestSerialization:
    def test_graph_json_roundtrip(self, tmp_path):
        """Testa salvar e carregar grafo em JSON."""
        g = generate_petersen_graph()
        file_path = tmp_path / "petersen.json"
        save_graph_to_json(g, file_path)

        loaded_g = load_graph_from_json(file_path)
        assert loaded_g.num_vertices == g.num_vertices
        assert loaded_g.edges == g.edges

    def test_tsp_json_roundtrip(self, tmp_path):
        """Testa salvar e carregar instância TSP em JSON."""
        tsp = generate_euclidean_tsp_instance(num_cities=8, seed=123)
        file_path = tmp_path / "tsp_test.json"
        save_tsp_to_json(tsp, file_path)

        loaded_tsp = load_tsp_from_json(file_path)
        assert loaded_tsp.num_cities == tsp.num_cities
        assert loaded_tsp.coordinates == tsp.coordinates
        assert loaded_tsp.distance_matrix == tsp.distance_matrix
