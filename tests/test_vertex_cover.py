"""
Testes unitários para as soluções exatas de Cobertura de Vértices (Issues #10 e #45).
Testa força bruta e branch-and-bound contra grafos com solução ótima teoricamente conhecida.
"""

import pytest

from src.exact import (
    vertex_cover_brute_force,
    vertex_cover_branch_and_bound,
    is_valid_vertex_cover,
)
from src.generators import (
    Graph,
    generate_complete_graph,
    generate_cycle_graph,
    generate_star_graph,
    generate_petersen_graph,
    generate_random_graph,
)


class TestVertexCoverExact:
    def test_empty_graph(self):
        """Grafo sem arestas possui cobertura mínima vazia (tamanho 0)."""
        g = Graph(num_vertices=5, edges=[])
        cover_bf, size_bf = vertex_cover_brute_force(g)
        cover_bb, size_bb = vertex_cover_branch_and_bound(g)
        assert size_bf == 0
        assert size_bb == 0
        assert cover_bf == set()
        assert cover_bb == set()

    def test_single_edge(self):
        """Grafo com uma aresta (0, 1): tamanho da cobertura ótima é 1."""
        g = Graph(num_vertices=2, edges=[(0, 1)])
        cover_bf, size_bf = vertex_cover_brute_force(g)
        cover_bb, size_bb = vertex_cover_branch_and_bound(g)
        assert size_bf == 1
        assert size_bb == 1
        assert is_valid_vertex_cover(g, cover_bf)
        assert is_valid_vertex_cover(g, cover_bb)

    def test_triangle_k3(self):
        """K_3 requer 2 vértices para cobrir todas as 3 arestas."""
        k3 = generate_complete_graph(3)
        cover_bf, size_bf = vertex_cover_brute_force(k3)
        cover_bb, size_bb = vertex_cover_branch_and_bound(k3)
        assert size_bf == 2
        assert size_bb == 2
        assert is_valid_vertex_cover(k3, cover_bf)
        assert is_valid_vertex_cover(k3, cover_bb)

    def test_complete_graph_kn(self):
        """K_n requer exatamente n - 1 vértices para cobertura mínima."""
        for n in [4, 5, 6]:
            kn = generate_complete_graph(n)
            cover_bf, size_bf = vertex_cover_brute_force(kn)
            cover_bb, size_bb = vertex_cover_branch_and_bound(kn)
            assert size_bf == n - 1
            assert size_bb == n - 1
            assert is_valid_vertex_cover(kn, cover_bf)
            assert is_valid_vertex_cover(kn, cover_bb)

    def test_star_graph(self):
        """Estrela K_{1, n-1} tem cobertura ótima de tamanho 1 (apenas o centro {0})."""
        star = generate_star_graph(8)
        cover_bf, size_bf = vertex_cover_brute_force(star)
        cover_bb, size_bb = vertex_cover_branch_and_bound(star)
        assert size_bf == 1
        assert size_bb == 1
        assert cover_bf == {0}
        assert cover_bb == {0}

    def test_cycles(self):
        """
        Ciclo C_n tem cobertura ótima de tamanho ceil(n / 2).
        C_4: 2 vértices.
        C_5: 3 vértices.
        C_6: 3 vértices.
        """
        c4 = generate_cycle_graph(4)
        c5 = generate_cycle_graph(5)
        c6 = generate_cycle_graph(6)

        assert vertex_cover_brute_force(c4)[1] == 2
        assert vertex_cover_branch_and_bound(c4)[1] == 2

        assert vertex_cover_brute_force(c5)[1] == 3
        assert vertex_cover_branch_and_bound(c5)[1] == 3

        assert vertex_cover_brute_force(c6)[1] == 3
        assert vertex_cover_branch_and_bound(c6)[1] == 3

    def test_petersen_graph(self):
        """O grafo de Petersen (10 vértices) possui cobertura mínima conhecida de 6 vértices."""
        petersen = generate_petersen_graph()
        cover_bf, size_bf = vertex_cover_brute_force(petersen)
        cover_bb, size_bb = vertex_cover_branch_and_bound(petersen)
        assert size_bf == 6
        assert size_bb == 6
        assert is_valid_vertex_cover(petersen, cover_bf)
        assert is_valid_vertex_cover(petersen, cover_bb)

    def test_random_graphs_bf_bb_equivalence(self):
        """Testa equivalência de resultados entre Força Bruta e Branch-and-Bound em grafos aleatórios."""
        for seed in [10, 20, 30]:
            rg = generate_random_graph(num_vertices=10, edge_probability=0.35, seed=seed)
            cover_bf, size_bf = vertex_cover_brute_force(rg)
            cover_bb, size_bb = vertex_cover_branch_and_bound(rg)
            assert size_bf == size_bb
            assert is_valid_vertex_cover(rg, cover_bf)
            assert is_valid_vertex_cover(rg, cover_bb)

    def test_invalid_inputs(self):
        """Verifica tratamento de erro para tipos inválidos."""
        with pytest.raises(TypeError):
            vertex_cover_brute_force("não é um grafo")
        with pytest.raises(TypeError):
            vertex_cover_branch_and_bound(None)
        with pytest.raises(TypeError):
            is_valid_vertex_cover(None, {0})
