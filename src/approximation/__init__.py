"""
Módulo de algoritmos de aproximação (Capítulo 35 — Cormen et al.).
Implementa APPROX-VERTEX-COVER (fator 2), APPROX-TSP-TOUR via MST (fator 2, TSP métrico)
e GREEDY-SET-COVER (fator H(d)).
"""

from .vertex_cover import (
    approx_vertex_cover,
    approx_vertex_cover_with_matching,
)
from .tsp import (
    mst_prim,
    preorder_walk,
    approx_tsp_tour,
)
from .set_cover import (
    SetCoverInstance,
    harmonic_number,
    is_valid_set_cover,
    greedy_set_cover,
    set_cover_brute_force,
    generate_set_cover_instance,
)

__all__ = [
    "approx_vertex_cover",
    "approx_vertex_cover_with_matching",
    "mst_prim",
    "preorder_walk",
    "approx_tsp_tour",
    "SetCoverInstance",
    "harmonic_number",
    "is_valid_set_cover",
    "greedy_set_cover",
    "set_cover_brute_force",
    "generate_set_cover_instance",
]
