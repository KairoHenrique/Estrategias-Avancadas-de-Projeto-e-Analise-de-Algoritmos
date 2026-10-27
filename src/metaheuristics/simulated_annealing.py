"""Simulated Annealing aplicado a um modelo didático de docking molecular."""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple


Point = Tuple[float, float]


@dataclass(frozen=True)
class Pose:
    """Posição e orientação simplificadas de um ligante."""
    x: float
    y: float
    theta: float


@dataclass
class DockingProblem:
    """
    Modelo didático de docking molecular.

    targets representam regiões de atração.
    obstacles representam regiões de repulsão.

    Este modelo é exclusivamente educacional: não calcula afinidade
    molecular real nem substitui ferramentas científicas de docking.
    """
    targets: List[Point]
    obstacles: List[Point]
    ligand_atoms: List[Point]
    attraction_sigma: float = 1.2
    repulsion_distance: float = 0.9
    repulsion_strength: float = 8.0
    boundary: float = 5.0

    def energy(self, pose: Pose) -> float:
        """Calcula a energia artificial de uma pose. Menor é melhor."""
        energy = 0.0

        cos_theta = math.cos(pose.theta)
        sin_theta = math.sin(pose.theta)

        # Transforma os átomos locais para a posição global.
        transformed_atoms = []

        for atom_x, atom_y in self.ligand_atoms:
            x = pose.x + atom_x * cos_theta - atom_y * sin_theta
            y = pose.y + atom_x * sin_theta + atom_y * cos_theta
            transformed_atoms.append((x, y))

        # Atração: cada átomo recebe uma contribuição do alvo mais próximo.
        sigma_squared = self.attraction_sigma ** 2

        for atom_x, atom_y in transformed_atoms:
            if self.targets:
                nearest_distance_squared = min(
                    (atom_x - target_x) ** 2
                    + (atom_y - target_y) ** 2
                    for target_x, target_y in self.targets
                )

                energy -= math.exp(
                    -nearest_distance_squared / (2.0 * sigma_squared)
                )

        # Repulsão: penaliza átomos que se aproximam demais dos obstáculos.
        for atom_x, atom_y in transformed_atoms:
            for obstacle_x, obstacle_y in self.obstacles:
                distance = math.hypot(
                    atom_x - obstacle_x,
                    atom_y - obstacle_y,
                )

                overlap = self.repulsion_distance - distance

                if overlap > 0:
                    energy += self.repulsion_strength * overlap ** 2

        # Penaliza poses que ultrapassam os limites do espaço.
        for x, y in transformed_atoms:
            excess_x = max(0.0, abs(x) - self.boundary)
            excess_y = max(0.0, abs(y) - self.boundary)

            energy += 10.0 * (excess_x ** 2 + excess_y ** 2)

        return energy


def generate_docking_problem(
    complexity: int,
    seed: int = 42,
) -> DockingProblem:
    """
    Cria uma instância reproduzível do problema.

    complexity controla a quantidade de regiões de atração e obstáculos.
    """
    if complexity < 1:
        raise ValueError("complexity deve ser maior ou igual a 1.")

    rng = random.Random(seed)

    targets = [
        (rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0))
        for _ in range(complexity)
    ]

    obstacles = [
        (rng.uniform(-4.0, 4.0), rng.uniform(-4.0, 4.0))
        for _ in range(complexity * 2)
    ]

    ligand_atoms = [
        (-0.8, 0.0),
        (-0.3, 0.5),
        (0.4, 0.4),
        (0.8, -0.2),
    ]

    return DockingProblem(
        targets=targets,
        obstacles=obstacles,
        ligand_atoms=ligand_atoms,
    )


def simulated_annealing(
    problem: DockingProblem,
    iterations: int = 2000,
    initial_temperature: float = 2.0,
    final_temperature: float = 0.01,
    seed: int = 42,
) -> dict:
    """
    Executa o Simulated Annealing para minimizar a energia.

    Retorna a melhor pose encontrada, sua energia, o número de avaliações
    e o tempo de execução.
    """
    if iterations < 1:
        raise ValueError("iterations deve ser maior ou igual a 1.")

    if initial_temperature <= 0 or final_temperature <= 0:
        raise ValueError("As temperaturas devem ser positivas.")

    if final_temperature > initial_temperature:
        raise ValueError(
            "A temperatura final deve ser menor ou igual à inicial."
        )

    rng = random.Random(seed)

    current = Pose(
        x=rng.uniform(-4.0, 4.0),
        y=rng.uniform(-4.0, 4.0),
        theta=rng.uniform(-math.pi, math.pi),
    )

    current_energy = problem.energy(current)
    best = current
    best_energy = current_energy
    evaluations = 1

    start_time = time.perf_counter()

    for step in range(iterations):
        progress = step / max(1, iterations - 1)

        # Resfriamento geométrico: a temperatura diminui ao longo do tempo.
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress

        # Perturbação da posição e orientação.
        candidate = Pose(
            x=max(-6.0, min(6.0, current.x + rng.gauss(0, 0.6))),
            y=max(-6.0, min(6.0, current.y + rng.gauss(0, 0.6))),
            theta=(
                current.theta + rng.gauss(0, 0.25) + math.pi
            ) % (2.0 * math.pi) - math.pi,
        )

        candidate_energy = problem.energy(candidate)
        evaluations += 1

        delta = candidate_energy - current_energy

        # Aceita melhorias e, ocasionalmente, soluções piores.
        if delta < 0 or rng.random() < math.exp(
            -delta / temperature
        ):
            current = candidate
            current_energy = candidate_energy

        if current_energy < best_energy:
            best = current
            best_energy = current_energy

    elapsed = time.perf_counter() - start_time

    return {
        "best_pose": best,
        "best_energy": best_energy,
        "evaluations": evaluations,
        "time_sec": elapsed,
    }


def random_search(
    problem: DockingProblem,
    iterations: int = 2000,
    seed: int = 42,
) -> dict:
    """
    Busca aleatória usada como referência experimental.

    Faz o mesmo número de avaliações que o Simulated Annealing,
    permitindo comparar a qualidade das soluções encontradas.
    """
    if iterations < 1:
        raise ValueError("iterations deve ser maior ou igual a 1.")

    rng = random.Random(seed)

    best = None
    best_energy = float("inf")

    start_time = time.perf_counter()

    for _ in range(iterations + 1):
        pose = Pose(
            x=rng.uniform(-4.0, 4.0),
            y=rng.uniform(-4.0, 4.0),
            theta=rng.uniform(-math.pi, math.pi),
        )

        energy = problem.energy(pose)

        if energy < best_energy:
            best = pose
            best_energy = energy

    elapsed = time.perf_counter() - start_time

    return {
        "best_pose": best,
        "best_energy": best_energy,
        "evaluations": iterations + 1,
        "time_sec": elapsed,
    }