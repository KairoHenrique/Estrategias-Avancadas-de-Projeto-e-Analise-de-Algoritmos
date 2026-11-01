"""
Testes unitários do GREEDY-SET-COVER (Issues #11 e #51).
Verifica cobertura de todos os elementos e o fator H(d) contra o ótimo por força bruta.
"""

import pytest

from src.approximation import (
    SetCoverInstance,
    harmonic_number,
    is_valid_set_cover,
    greedy_set_cover,
    set_cover_brute_force,
    generate_set_cover_instance,
)


class TestSetCoverInstance:
    def test_infeasible_instance_raises(self):
        with pytest.raises(ValueError):
            SetCoverInstance(universe={1, 2, 3}, subsets=[{1}, {2}])

    def test_element_outside_universe_raises(self):
        with pytest.raises(ValueError):
            SetCoverInstance(universe={1, 2}, subsets=[{1, 2, 99}])

    def test_generator_is_feasible_and_reproducible(self):
        a = generate_set_cover_instance(30, 10, 0.2, seed=7)
        b = generate_set_cover_instance(30, 10, 0.2, seed=7)
        assert a.subsets == b.subsets
        assert set().union(*a.subsets) == a.universe

    def test_harmonic_number(self):
        assert harmonic_number(0) == 0
        assert harmonic_number(1) == 1
        assert harmonic_number(3) == pytest.approx(1 + 1 / 2 + 1 / 3)


class TestGreedySetCover:
    def test_empty_universe(self):
        inst = SetCoverInstance(universe=set(), subsets=[{}, {}])
        assert greedy_set_cover(inst) == ([], 0)

    def test_covers_all_elements(self):
        """Critério da Issue #51: todos os elementos de X são cobertos."""
        for seed in range(10):
            inst = generate_set_cover_instance(40, 15, 0.15, seed=seed)
            chosen, size = greedy_set_cover(inst)
            assert size == len(chosen) == len(set(chosen))
            assert is_valid_set_cover(inst, chosen)

    def test_picks_largest_first(self):
        """Linha 4: o primeiro conjunto escolhido é o de maior |S ∩ X|."""
        inst = SetCoverInstance(universe=range(6), subsets=[{0}, {0, 1, 2, 3}, {4, 5}])
        chosen, _ = greedy_set_cover(inst)
        assert chosen[0] == 1

    def test_suboptimal_example(self):
        """
        Exemplo em que o guloso NÃO é ótimo:
            X = {1..6}, S0 = {1,2,3,4}, S1 = {1,2,5}, S2 = {3,4,6}
        Guloso escolhe S0 e depois precisa de S1 e S2 (3 conjuntos); ótimo = {S1, S2} (2).
        Razão 1,5 <= H(4) ≈ 2,08.
        """
        inst = SetCoverInstance(universe={1, 2, 3, 4, 5, 6}, subsets=[{1, 2, 3, 4}, {1, 2, 5}, {3, 4, 6}])
        _, greedy_size = greedy_set_cover(inst)
        opt, opt_size = set_cover_brute_force(inst)
        assert greedy_size == 3
        assert opt_size == 2
        assert sorted(opt) == [1, 2]
        assert greedy_size <= harmonic_number(inst.max_subset_size) * opt_size

    def test_factor_hd_against_optimum(self):
        """|C| <= H(max|S|) · |C*| em instâncias pequenas."""
        for m in [6, 10, 14]:
            for seed in range(5):
                inst = generate_set_cover_instance(25, m, 0.2, seed=100 * m + seed)
                _, greedy_size = greedy_set_cover(inst)
                opt, opt_size = set_cover_brute_force(inst)
                assert is_valid_set_cover(inst, opt)
                assert opt_size <= greedy_size
                assert greedy_size <= harmonic_number(inst.max_subset_size) * opt_size + 1e-9

    def test_invalid_inputs(self):
        with pytest.raises(TypeError):
            greedy_set_cover(None)
        with pytest.raises(TypeError):
            set_cover_brute_force([{1, 2}])
        with pytest.raises(ValueError):
            generate_set_cover_instance(5, 0)
