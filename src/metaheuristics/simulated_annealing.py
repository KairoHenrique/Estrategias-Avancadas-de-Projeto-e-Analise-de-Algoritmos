import math
import random
import time

from dataclasses import dataclass
from typing import List, Tuple


Point = Tuple[float, float]

# Os dois algoritmos devem usar o mesmo intervalo para x e y.
SEARCH_MIN = -4.0
SEARCH_MAX = 4.0


@dataclass(frozen=True)
class Pose:
    """Representa a posição e a orientação do ligante."""
    x: float
    y: float
    theta: float


@dataclass
class DockingProblem:
    """
    Problema educacional inspirado em docking molecular.

    Este modelo usa uma função de energia artificial simplificada.
    Ele NÃO representa docking molecular real nem prevê afinidade
    entre moléculas.
    """
    targets: List[Point]
    obstacles: List[Point]
    ligand_atoms: List[Point]

    attraction_sigma: float = 1.2
    repulsion_distance: float = 0.9
    repulsion_strength: float = 8.0
    boundary: float = 5.0

    def __post_init__(self):
        if self.attraction_sigma <= 0:
            raise ValueError("attraction_sigma deve ser maior que zero.")

        if self.repulsion_distance < 0:
            raise ValueError("repulsion_distance não pode ser negativo.")

        if self.repulsion_strength < 0:
            raise ValueError("repulsion_strength não pode ser negativo.")

        if self.boundary <= 0:
            raise ValueError("boundary deve ser maior que zero.")

        if not self.ligand_atoms:
            raise ValueError("ligand_atoms não pode estar vazio.")

    def energy(self, pose: Pose) -> float:
        """
        Calcula a energia artificial de uma pose.

        Quanto menor a energia, melhor a solução segundo este modelo.
        """
        energy = 0.0

        cos_theta = math.cos(pose.theta)
        sin_theta = math.sin(pose.theta)

        transformed_atoms = []

        # Transforma os átomos do ligante conforme a pose.
        for atom_x, atom_y in self.ligand_atoms:
            x = (
                atom_x * cos_theta
                - atom_y * sin_theta
                + pose.x
            )

            y = (
                atom_x * sin_theta
                + atom_y * cos_theta
                + pose.y
            )

            transformed_atoms.append((x, y))

        for atom_x, atom_y in transformed_atoms:

            # Atração pelo alvo mais próximo.
            if self.targets:
                distances = [
                    math.hypot(
                        atom_x - target_x,
                        atom_y - target_y
                    )
                    for target_x, target_y in self.targets
                ]

                nearest_distance = min(distances)

                attraction = -math.exp(
                    -(nearest_distance ** 2)
                    / (2 * self.attraction_sigma ** 2)
                )

                energy += attraction

            # Repulsão contra obstáculos próximos.
            for obstacle_x, obstacle_y in self.obstacles:
                distance = math.hypot(
                    atom_x - obstacle_x,
                    atom_y - obstacle_y
                )

                if distance < self.repulsion_distance:
                    difference = self.repulsion_distance - distance

                    energy += (
                        self.repulsion_strength
                        * difference ** 2
                    )

            # Penalidade para átomos fora dos limites.
            if abs(atom_x) > self.boundary:
                energy += (abs(atom_x) - self.boundary) ** 2

            if abs(atom_y) > self.boundary:
                energy += (abs(atom_y) - self.boundary) ** 2

        return energy


def generate_docking_problem(
    complexity: int,
    seed: int = 42
) -> DockingProblem:
    """
    Gera uma instância reproduzível do problema.

    A complexidade controla a quantidade de alvos e obstáculos.
    """
    if complexity < 1:
        raise ValueError("complexity deve ser maior ou igual a 1.")

    rng = random.Random(seed)

    targets = [
        (
            rng.uniform(-2.0, 2.0),
            rng.uniform(-2.0, 2.0)
        )
        for _ in range(complexity)
    ]

    obstacles = [
        (
            rng.uniform(-4.0, 4.0),
            rng.uniform(-4.0, 4.0)
        )
        for _ in range(complexity * 2)
    ]

    ligand_atoms = [
        (0.0, 0.0),
        (0.8, 0.0),
        (0.0, 0.8),
        (0.8, 0.8)
    ]

    return DockingProblem(
        targets=targets,
        obstacles=obstacles,
        ligand_atoms=ligand_atoms
    )


def simulated_annealing(
    problem: DockingProblem,
    iterations: int = 2000,
    initial_temperature: float = 2.0,
    final_temperature: float = 0.01,
    seed: int = 42
) -> dict:
    """
    Executa o algoritmo Simulated Annealing.

    O parâmetro iterations indica quantas avaliações serão feitas
    depois da avaliação da solução inicial.

    Portanto:
        avaliações totais = iterations + 1
    """
    if iterations < 1:
        raise ValueError("iterations deve ser maior ou igual a 1.")

    if (
        not math.isfinite(initial_temperature)
        or initial_temperature <= 0
    ):
        raise ValueError(
            "initial_temperature deve ser finita e maior que zero."
        )

    if (
        not math.isfinite(final_temperature)
        or final_temperature <= 0
    ):
        raise ValueError(
            "final_temperature deve ser finita e maior que zero."
        )

    if final_temperature > initial_temperature:
        raise ValueError(
            "final_temperature não pode ser maior que initial_temperature."
        )

    rng = random.Random(seed)

    # O tempo começa antes da criação e avaliação da solução inicial.
    start_time = time.perf_counter()

    current_pose = Pose(
        x=rng.uniform(SEARCH_MIN, SEARCH_MAX),
        y=rng.uniform(SEARCH_MIN, SEARCH_MAX),
        theta=rng.uniform(-math.pi, math.pi)
    )

    current_energy = problem.energy(current_pose)
    evaluations = 1

    best_pose = current_pose
    best_energy = current_energy

    for step in range(iterations):

        progress = step / max(iterations - 1, 1)

        # Resfriamento geométrico da temperatura.
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress

        # Gera uma solução vizinha dentro do mesmo espaço de busca.
        candidate_pose = Pose(
            x=max(
                SEARCH_MIN,
                min(
                    SEARCH_MAX,
                    current_pose.x + rng.gauss(0, 0.6)
                )
            ),
            y=max(
                SEARCH_MIN,
                min(
                    SEARCH_MAX,
                    current_pose.y + rng.gauss(0, 0.6)
                )
            ),
            theta=(
                current_pose.theta + rng.gauss(0, 0.25) + math.pi
            ) % (2 * math.pi) - math.pi
        )

        candidate_energy = problem.energy(candidate_pose)
        evaluations += 1

        delta = candidate_energy - current_energy

        # Aceita soluções melhores ou, probabilisticamente,
        # soluções piores para tentar escapar de mínimos locais.
        if (
            delta < 0
            or rng.random() < math.exp(-delta / temperature)
        ):
            current_pose = candidate_pose
            current_energy = candidate_energy

        # Guarda a melhor solução encontrada até o momento.
        if current_energy < best_energy:
            best_pose = current_pose
            best_energy = current_energy

    elapsed_time = time.perf_counter() - start_time

    return {
        "best_pose": best_pose,
        "best_energy": best_energy,
        "evaluations": evaluations,
        "time_sec": elapsed_time
    }


def random_search(
    problem: DockingProblem,
    iterations: int = 2000,
    seed: int = 42
) -> dict:
    """
    Executa a Busca Aleatória como algoritmo de comparação.

    O parâmetro iterations indica quantas avaliações adicionais
    serão feitas após a primeira solução.

    Portanto:
        avaliações totais = iterations + 1
    """
    if iterations < 1:
        raise ValueError("iterations deve ser maior ou igual a 1.")

    rng = random.Random(seed)

    # A medição começa antes da primeira avaliação.
    start_time = time.perf_counter()

    best_pose = None
    best_energy = float("inf")
    evaluations = 0

    for _ in range(iterations + 1):
        pose = Pose(
            x=rng.uniform(SEARCH_MIN, SEARCH_MAX),
            y=rng.uniform(SEARCH_MIN, SEARCH_MAX),
            theta=rng.uniform(-math.pi, math.pi)
        )

        energy = problem.energy(pose)
        evaluations += 1

        if energy < best_energy:
            best_pose = pose
            best_energy = energy

    elapsed_time = time.perf_counter() - start_time

    return {
        "best_pose": best_pose,
        "best_energy": best_energy,
        "evaluations": evaluations,
        "time_sec": elapsed_time
    }