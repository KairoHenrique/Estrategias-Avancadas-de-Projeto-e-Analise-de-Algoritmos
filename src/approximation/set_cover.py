"""
Algoritmo de aproximação para a Cobertura de Conjuntos (Set Cover).
Capítulo 35.3 (Cormen et al.) — GREEDY-SET-COVER.

Definição:
    Instância (X, F): um universo finito X e uma família F de subconjuntos de X
    tal que X = ∪_{S ∈ F} S. Busca-se uma subfamília C ⊆ F de cardinalidade mínima
    cuja união seja X.

Pseudocódigo (Cormen):
    GREEDY-SET-COVER(X, F)
    1  U = X
    2  C = ∅
    3  while U ≠ ∅
    4      selecione um S ∈ F que maximize |S ∩ U|
    5      U = U − S
    6      C = C ∪ {S}
    7  return C

Garantia (Teorema 35.4 / Corolário 35.5):
    |C| <= H(max{|S| : S ∈ F}) · |C*|, onde H(d) = Σ_{i=1..d} 1/i <= ln d + 1.
    Consequentemente |C| <= (ln |X| + 1) · |C*|.

Complexidade (implementação direta):
    Tempo: O(|X| · |F| · min(|X|, |F|)) — o laço executa no máximo min(|X|, |F|)
           vezes e cada iteração examina todos os |F| conjuntos em O(|X|).
    Espaço: O(|X| + Σ|S|).

Este módulo também contém um solver exato por força bruta (necessário para
medir a razão de aproximação empírica) e um gerador de instâncias com semente fixa.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from typing import FrozenSet, Iterable, List, Optional, Sequence, Tuple


@dataclass
class SetCoverInstance:
    """
    Instância (X, F) do problema de Cobertura de Conjuntos.
    Os subconjuntos são indexados de 0 a len(subsets) - 1.
    """
    universe: FrozenSet[int]
    subsets: List[FrozenSet[int]] = field(default_factory=list)

    def __post_init__(self):
        self.universe = frozenset(self.universe)
        self.subsets = [frozenset(s) for s in self.subsets]

        union: set = set()
        for i, s in enumerate(self.subsets):
            extra = s - self.universe
            if extra:
                raise ValueError(f"Subconjunto {i} contém elementos fora do universo: {sorted(extra)}")
            union |= s

        missing = self.universe - union
        if missing:
            raise ValueError(
                f"Instância inviável: a união de F não cobre X. Elementos descobertos: {sorted(missing)}"
            )

    @property
    def num_subsets(self) -> int:
        return len(self.subsets)

    @property
    def max_subset_size(self) -> int:
        """d = max{|S| : S ∈ F}, usado no fator teórico H(d)."""
        return max((len(s) for s in self.subsets), default=0)


def harmonic_number(d: int) -> float:
    """H(d) = 1 + 1/2 + ... + 1/d (H(0) = 0). Fator teórico do GREEDY-SET-COVER."""
    if d < 0:
        raise ValueError(f"d deve ser >= 0, recebido {d}")
    return sum(1.0 / i for i in range(1, d + 1))


def _check_instance(instance: SetCoverInstance) -> None:
    if not isinstance(instance, SetCoverInstance):
        raise TypeError(
            f"Parâmetro 'instance' deve ser uma instância de SetCoverInstance, recebido {type(instance).__name__}"
        )


def is_valid_set_cover(instance: SetCoverInstance, chosen: Iterable[int]) -> bool:
    """
    Verifica se os índices escolhidos formam uma cobertura de X.
    Executa em tempo O(Σ|S| para S escolhido).
    """
    _check_instance(instance)
    covered: set = set()
    for i in chosen:
        if not isinstance(i, int) or not (0 <= i < instance.num_subsets):
            return False
        covered |= instance.subsets[i]
    return covered >= instance.universe


def greedy_set_cover(instance: SetCoverInstance) -> Tuple[List[int], int]:
    """
    GREEDY-SET-COVER (Cormen, Seção 35.3): H(d)-aproximação para a Cobertura de Conjuntos.
    Empates na linha 4 são resolvidos pelo menor índice (resultado determinístico).

    Complexidade:
        Tempo: O(|X| · |F| · min(|X|, |F|))
        Espaço: O(|X|)

    Args:
        instance: Instância (X, F).

    Returns:
        (indices_escolhidos, tamanho): índices dos subconjuntos de F na ordem
        em que foram selecionados e a cardinalidade |C|.

    Raises:
        TypeError: Se instance não for SetCoverInstance.
    """
    _check_instance(instance)

    uncovered = set(instance.universe)          # linha 1: U = X
    chosen: List[int] = []                      # linha 2: C = ∅

    while uncovered:                            # linha 3
        # linha 4: S que maximiza |S ∩ U| (max devolve o primeiro em caso de empate)
        best = max(range(instance.num_subsets), key=lambda i: len(instance.subsets[i] & uncovered))
        uncovered -= instance.subsets[best]     # linha 5: U = U − S
        chosen.append(best)                     # linha 6: C = C ∪ {S}

    return chosen, len(chosen)                  # linha 7


def set_cover_brute_force(instance: SetCoverInstance) -> Tuple[List[int], int]:
    """
    Solução EXATA da Cobertura de Conjuntos por enumeração de subfamílias de tamanho
    k = 1, 2, ..., |F|. A primeira subfamília válida tem cardinalidade mínima.
    Os conjuntos são codificados como máscaras de bits para que a união seja O(1)
    por operação de palavra (para |X| pequeno).

    Usada apenas como referência de ótimo para medir a razão empírica (Issue #52).

    Complexidade:
        Tempo: O(2^|F| · |F|) operações de máscara no pior caso.
        Espaço: O(|F|).

    Returns:
        (indices_otimos, tamanho_otimo)
    """
    _check_instance(instance)
    if not instance.universe:
        return [], 0

    index = {x: b for b, x in enumerate(sorted(instance.universe))}
    full = (1 << len(index)) - 1
    masks = []
    for s in instance.subsets:
        m = 0
        for x in s:
            m |= 1 << index[x]
        masks.append(m)

    for k in range(1, instance.num_subsets + 1):
        for combo in itertools.combinations(range(instance.num_subsets), k):
            acc = 0
            for i in combo:
                acc |= masks[i]
            if acc == full:
                return list(combo), k

    # Inalcançável: __post_init__ garante que F cobre X
    raise ValueError("Instância inviável.")  # pragma: no cover


def generate_set_cover_instance(
    universe_size: int,
    num_subsets: int,
    density: float = 0.2,
    seed: Optional[int] = None,
) -> SetCoverInstance:
    """
    Gera uma instância aleatória (X, F) viável com semente fixa.
    X = {0, ..., universe_size - 1}. Cada elemento entra em cada subconjunto com
    probabilidade `density`; elementos que ficarem descobertos são inseridos em um
    subconjunto sorteado, garantindo X = ∪F.

    Args:
        universe_size: |X| >= 0.
        num_subsets: |F| >= 1 (quando |X| > 0).
        density: Probabilidade de inclusão de cada elemento em cada subconjunto.
        seed: Semente pseudoaleatória para reprodutibilidade.
    """
    if universe_size < 0:
        raise ValueError(f"universe_size deve ser >= 0, recebido {universe_size}")
    if num_subsets < 1 and universe_size > 0:
        raise ValueError(f"num_subsets deve ser >= 1, recebido {num_subsets}")
    if not (0.0 <= density <= 1.0):
        raise ValueError(f"density deve estar em [0.0, 1.0], recebido {density}")

    rng = random.Random(seed)
    subsets: List[set] = [
        {x for x in range(universe_size) if rng.random() < density}
        for _ in range(num_subsets)
    ]

    covered = set().union(*subsets) if subsets else set()
    for x in range(universe_size):
        if x not in covered:
            subsets[rng.randrange(num_subsets)].add(x)

    return SetCoverInstance(universe=frozenset(range(universe_size)), subsets=subsets)
