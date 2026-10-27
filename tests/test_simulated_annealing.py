import math

import pytest

from src.metaheuristics.simulated_annealing import (
    DockingProblem,
    Pose,
    generate_docking_problem,
    random_search,
    simulated_annealing,
)


def test_pose_energy_is_finite():
    problem = generate_docking_problem(complexity=3, seed=42)

    energy = problem.energy(Pose(x=0.0, y=0.0, theta=0.0))

    assert math.isfinite(energy)


def test_problem_generation_is_reproducible():
    problem_a = generate_docking_problem(complexity=4, seed=123)
    problem_b = generate_docking_problem(complexity=4, seed=123)

    assert problem_a.targets == problem_b.targets
    assert problem_a.obstacles == problem_b.obstacles


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


def test_invalid_complexity_is_rejected():
    with pytest.raises(ValueError):
        generate_docking_problem(complexity=0)


def test_invalid_iteration_count_is_rejected():
    problem = generate_docking_problem(complexity=3, seed=42)

    with pytest.raises(ValueError):
        simulated_annealing(problem, iterations=0)

    with pytest.raises(ValueError):
        random_search(problem, iterations=0)