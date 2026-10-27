import math

import pytest

from src.metaheuristics.simulated_annealing import (
    DockingProblem,
    Pose,
    generate_docking_problem,
    random_search,
    simulated_annealing,
)


# ============================================================
# TESTES DA FUNÇÃO DE ENERGIA E DO PROBLEMA
# ============================================================

def test_pose_energy_is_finite():
    problem = generate_docking_problem(complexity=3, seed=42)

    energy = problem.energy(Pose(x=0.0, y=0.0, theta=0.0))

    assert math.isfinite(energy)


def test_problem_generation_is_reproducible():
    problem_a = generate_docking_problem(complexity=4, seed=123)
    problem_b = generate_docking_problem(complexity=4, seed=123)

    assert problem_a.targets == problem_b.targets
    assert problem_a.obstacles == problem_b.obstacles
    assert problem_a.ligand_atoms == problem_b.ligand_atoms


def test_invalid_complexity_is_rejected():
    with pytest.raises(ValueError):
        generate_docking_problem(complexity=0)


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("attraction_sigma", 0),
        ("attraction_sigma", -1),
        ("repulsion_distance", -1),
        ("repulsion_strength", -1),
        ("boundary", 0),
        ("boundary", -1),
    ],
)
def test_invalid_problem_parameters_are_rejected(parameter, value):
    parameters = {
        "targets": [(0.0, 0.0)],
        "obstacles": [],
        "ligand_atoms": [(0.0, 0.0)],
    }
    parameters[parameter] = value

    with pytest.raises(ValueError):
        DockingProblem(**parameters)


def test_empty_ligand_is_rejected():
    with pytest.raises(ValueError):
        DockingProblem(
            targets=[(0.0, 0.0)],
            obstacles=[],
            ligand_atoms=[],
        )


# ============================================================
# TESTES DO SIMULATED ANNEALING
# ============================================================

def test_simulated_annealing_returns_valid_result():
    problem = generate_docking_problem(complexity=3, seed=42)

    result = simulated_annealing(
        problem=problem,
        iterations=100,
        seed=42,
    )

    assert isinstance(result["best_pose"], Pose)
    assert math.isfinite(result["best_energy"])
    assert result["evaluations"] == 101
    assert result["time_sec"] >= 0


def test_simulated_annealing_is_reproducible():
    problem = generate_docking_problem(complexity=3, seed=42)

    result_a = simulated_annealing(
        problem=problem,
        iterations=100,
        initial_temperature=2.0,
        final_temperature=0.01,
        seed=123,
    )

    result_b = simulated_annealing(
        problem=problem,
        iterations=100,
        initial_temperature=2.0,
        final_temperature=0.01,
        seed=123,
    )

    assert result_a["best_pose"] == result_b["best_pose"]
    assert result_a["best_energy"] == result_b["best_energy"]
    assert result_a["evaluations"] == result_b["evaluations"]


def test_simulated_annealing_accepts_configurable_temperatures():
    problem = generate_docking_problem(complexity=3, seed=42)

    result = simulated_annealing(
        problem=problem,
        iterations=20,
        initial_temperature=5.0,
        final_temperature=0.1,
        seed=42,
    )

    assert isinstance(result["best_pose"], Pose)
    assert math.isfinite(result["best_energy"])
    assert result["evaluations"] == 21


@pytest.mark.parametrize(
    "temperature",
    [0, -1, float("inf"), float("-inf"), float("nan")],
)
def test_invalid_initial_temperature_is_rejected(temperature):
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        simulated_annealing(
            problem=problem,
            iterations=10,
            initial_temperature=temperature,
            final_temperature=0.01,
        )


@pytest.mark.parametrize(
    "temperature",
    [0, -1, float("inf"), float("-inf"), float("nan")],
)
def test_invalid_final_temperature_is_rejected(temperature):
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        simulated_annealing(
            problem=problem,
            iterations=10,
            initial_temperature=2.0,
            final_temperature=temperature,
        )


def test_final_temperature_greater_than_initial_is_rejected():
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        simulated_annealing(
            problem=problem,
            iterations=10,
            initial_temperature=1.0,
            final_temperature=2.0,
        )


def test_invalid_simulated_annealing_iteration_count_is_rejected():
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        simulated_annealing(problem, iterations=0)

    with pytest.raises(ValueError):
        simulated_annealing(problem, iterations=-1)


# ============================================================
# TESTES DO RANDOM SEARCH
# ============================================================

def test_random_search_returns_valid_result():
    problem = generate_docking_problem(complexity=3, seed=42)

    result = random_search(
        problem=problem,
        iterations=100,
        seed=42,
    )

    assert isinstance(result["best_pose"], Pose)
    assert math.isfinite(result["best_energy"])
    assert result["evaluations"] == 101
    assert result["time_sec"] >= 0


def test_random_search_is_reproducible():
    problem = generate_docking_problem(complexity=3, seed=42)

    result_a = random_search(
        problem=problem,
        iterations=100,
        seed=123,
    )

    result_b = random_search(
        problem=problem,
        iterations=100,
        seed=123,
    )

    assert result_a["best_pose"] == result_b["best_pose"]
    assert result_a["best_energy"] == result_b["best_energy"]
    assert result_a["evaluations"] == result_b["evaluations"]


def test_invalid_random_search_iteration_count_is_rejected():
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        random_search(problem, iterations=0)

    with pytest.raises(ValueError):
        random_search(problem, iterations=-1)