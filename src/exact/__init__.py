"""
Módulo de algoritmos exatos para problemas NP-difíceis.
Implementa força bruta enumerativa, branch-and-bound e programação dinâmica (Held-Karp).
"""

from .vertex_cover import (
    vertex_cover_brute_force,
    vertex_cover_branch_and_bound,
    is_valid_vertex_cover,
)
from .tsp import (
    tsp_brute_force,
    tsp_held_karp,
    calculate_tour_cost,
)

__all__ = [
    "vertex_cover_brute_force",
    "vertex_cover_branch_and_bound",
    "is_valid_vertex_cover",
    "tsp_brute_force",
    "tsp_held_karp",
    "calculate_tour_cost",
]
