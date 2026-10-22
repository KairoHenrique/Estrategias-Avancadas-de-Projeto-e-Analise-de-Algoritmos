"""
Gerador de instâncias com semente pseudoaleatória fixa para problemas NP-difíceis.
Permite reprodutibilidade estrita entre execuções e compatibilidade com experimentos
das pessoas 3 (Kairo - Exatos), 4 (Heitor - Aproximações) e 5 (Jade - Metaheurísticas).
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Graph:
    """
    Representação de um grafo não-direcionado simples.
    Vértices são indexados de 0 a num_vertices - 1.
    """
    num_vertices: int
    edges: List[Tuple[int, int]] = field(default_factory=list)
    adjacency_list: Dict[int, Set[int]] = field(default_factory=dict)

    def __post_init__(self):
        if self.num_vertices < 0:
            raise ValueError(f"O número de vértices não pode ser negativo. Recebido: {self.num_vertices}")

        if not self.adjacency_list:
            self.adjacency_list = {i: set() for i in range(self.num_vertices)}
            # Normaliza e insere as arestas fornecidas
            normalized_edges = set()
            for u, v in self.edges:
                if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
                    raise ValueError(f"Aresta ({u}, {v}) inválida para grafo com {self.num_vertices} vértices.")
                if u != v:  # Ignora laços simples
                    edge = (min(u, v), max(u, v))
                    normalized_edges.add(edge)
                    self.adjacency_list[u].add(v)
                    self.adjacency_list[v].add(u)
            self.edges = sorted(list(normalized_edges))

    def has_edge(self, u: int, v: int) -> bool:
        """Verifica se existe uma aresta entre u e v."""
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            return False
        return v in self.adjacency_list.get(u, set())

    @property
    def num_edges(self) -> int:
        """Retorna o número de arestas no grafo."""
        return len(self.edges)

    def to_dict(self) -> dict:
        """Serializa o grafo para dicionário."""
        return {
            "num_vertices": self.num_vertices,
            "edges": self.edges,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Graph:
        """Cria uma instância de Graph a partir de um dicionário."""
        return cls(
            num_vertices=data["num_vertices"],
            edges=[(u, v) for u, v in data["edges"]],
        )


@dataclass
class TSPInstance:
    """
    Representação de uma instância do Caixeiro-Viajante (TSP).
    Contém a matriz de distâncias e, opcionalmente, as coordenadas 2D.
    """
    num_cities: int
    distance_matrix: List[List[float]]
    coordinates: Optional[List[Tuple[float, float]]] = None
    is_metric: bool = True

    def __post_init__(self):
        if self.num_cities < 0:
            raise ValueError(f"Número de cidades não pode ser negativo: {self.num_cities}")
        if len(self.distance_matrix) != self.num_cities:
            raise ValueError(
                f"Tamanho da matriz ({len(self.distance_matrix)}) não corresponde ao número de cidades ({self.num_cities})."
            )
        for row in self.distance_matrix:
            if len(row) != self.num_cities:
                raise ValueError("A matriz de distâncias deve ser quadrada.")

    def to_dict(self) -> dict:
        """Serializa a instância do TSP para dicionário."""
        return {
            "num_cities": self.num_cities,
            "distance_matrix": self.distance_matrix,
            "coordinates": self.coordinates,
            "is_metric": self.is_metric,
        }

    @classmethod
    def from_dict(cls, data: dict) -> TSPInstance:
        """Cria uma instância do TSP a partir de um dicionário."""
        coords = None
        if data.get("coordinates") is not None:
            coords = [(float(x), float(y)) for x, y in data["coordinates"]]
        return cls(
            num_cities=data["num_cities"],
            distance_matrix=data["distance_matrix"],
            coordinates=coords,
            is_metric=data.get("is_metric", True),
        )


def generate_random_graph(num_vertices: int, edge_probability: float, seed: Optional[int] = None) -> Graph:
    """
    Gera um grafo aleatório no modelo Erdős-Rényi G(n, p).
    
    Args:
        num_vertices: Quantidade de vértices n >= 0.
        edge_probability: Probabilidade p de inclusão de cada aresta (0.0 <= p <= 1.0).
        seed: Semente pseudoaleatória para reprodutibilidade.
    """
    if num_vertices < 0:
        raise ValueError(f"num_vertices deve ser >= 0, recebido {num_vertices}")
    if not (0.0 <= edge_probability <= 1.0):
        raise ValueError(f"edge_probability deve estar em [0.0, 1.0], recebido {edge_probability}")

    rng = random.Random(seed)
    edges = []
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if rng.random() < edge_probability:
                edges.append((u, v))

    return Graph(num_vertices=num_vertices, edges=edges)


def generate_complete_graph(num_vertices: int) -> Graph:
    """Gera um grafo completo K_n."""
    if num_vertices < 0:
        raise ValueError(f"num_vertices deve ser >= 0, recebido {num_vertices}")
    edges = [(u, v) for u in range(num_vertices) for v in range(u + 1, num_vertices)]
    return Graph(num_vertices=num_vertices, edges=edges)


def generate_cycle_graph(num_vertices: int) -> Graph:
    """Gera um grafo ciclo C_n."""
    if num_vertices < 0:
        raise ValueError(f"num_vertices deve ser >= 0, recebido {num_vertices}")
    if num_vertices <= 2:
        # Para n <= 2, gera caminhos ou vértices isolados
        edges = [(i, i + 1) for i in range(num_vertices - 1)]
    else:
        edges = [(i, (i + 1) % num_vertices) for i in range(num_vertices)]
    return Graph(num_vertices=num_vertices, edges=edges)


def generate_star_graph(num_vertices: int) -> Graph:
    """Gera um grafo estrela K_{1, n-1} com o centro no vértice 0."""
    if num_vertices < 0:
        raise ValueError(f"num_vertices deve ser >= 0, recebido {num_vertices}")
    edges = [(0, v) for v in range(1, num_vertices)]
    return Graph(num_vertices=num_vertices, edges=edges)


def generate_bipartite_graph(n1: int, n2: int, edge_probability: float, seed: Optional[int] = None) -> Graph:
    """
    Gera um grafo bipartido com partições de tamanho n1 e n2.
    Vértices da partição 1: 0 .. n1-1; da partição 2: n1 .. n1+n2-1.
    """
    if n1 < 0 or n2 < 0:
        raise ValueError("Tamanhos das partições devem ser >= 0")
    if not (0.0 <= edge_probability <= 1.0):
        raise ValueError(f"edge_probability deve estar em [0.0, 1.0], recebido {edge_probability}")

    rng = random.Random(seed)
    total_vertices = n1 + n2
    edges = []
    for u in range(n1):
        for v in range(n1, total_vertices):
            if rng.random() < edge_probability:
                edges.append((u, v))
    return Graph(num_vertices=total_vertices, edges=edges)


def generate_petersen_graph() -> Graph:
    """Gera o clássico grafo de Petersen (10 vértices, 15 arestas)."""
    edges = [
        # Ciclo externo: 0, 1, 2, 3, 4
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        # Estrela interna: 5, 6, 7, 8, 9
        (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
        # Conexões entre ciclo externo e estrela interna
        (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    ]
    return Graph(num_vertices=10, edges=edges)


def generate_euclidean_tsp_instance(
    num_cities: int,
    width: float = 100.0,
    height: float = 100.0,
    seed: Optional[int] = None
) -> TSPInstance:
    """
    Gera uma instância euclidiana 2D para o TSP com cidades distribuídas no plano.
    Garante matematicamente a desigualdade triangular (TSP Métrico):
        d(u, v) <= d(u, w) + d(w, v)
    
    Args:
        num_cities: Número de cidades n >= 0.
        width: Largura máxima da caixa delimitadora.
        height: Altura máxima da caixa delimitadora.
        seed: Semente pseudoaleatória para reprodutibilidade.
    """
    if num_cities < 0:
        raise ValueError(f"num_cities deve ser >= 0, recebido {num_cities}")
    if width <= 0 or height <= 0:
        raise ValueError("width e height devem ser estritamente positivos")

    rng = random.Random(seed)
    coordinates = [
        (rng.uniform(0.0, width), rng.uniform(0.0, height))
        for _ in range(num_cities)
    ]

    distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        x1, y1 = coordinates[i]
        for j in range(i + 1, num_cities):
            x2, y2 = coordinates[j]
            dist = math.hypot(x1 - x2, y1 - y2)
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    return TSPInstance(
        num_cities=num_cities,
        distance_matrix=distance_matrix,
        coordinates=coordinates,
        is_metric=True,
    )


def save_graph_to_json(graph: Graph, filepath: str | Path) -> None:
    """Salva a estrutura do grafo em formato JSON legível."""
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(graph.to_dict(), f, indent=2)


def load_graph_from_json(filepath: str | Path) -> Graph:
    """Carrega um grafo a partir de arquivo JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Graph.from_dict(data)


def save_tsp_to_json(tsp: TSPInstance, filepath: str | Path) -> None:
    """Salva uma instância TSP em formato JSON legível."""
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(tsp.to_dict(), f, indent=2)


def load_tsp_from_json(filepath: str | Path) -> TSPInstance:
    """Carrega uma instância TSP a partir de arquivo JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return TSPInstance.from_dict(data)
