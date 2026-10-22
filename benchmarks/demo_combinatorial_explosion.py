"""
Script de Demonstração Interativa da Explosão Combinatória e Intratabilidade.
Issue #62: Slides dos algoritmos exatos e demonstração ao vivo.

Demonstra:
1. A matemática da intratabilidade (tabelas teóricas de tempo com 1 bilhão de operações/s).
2. Execução empírica ao vivo comparando Força Bruta vs Algoritmos Otimizados (Held-Karp e B&B).
3. A fronteira prática onde algoritmos exatos tornam-se inviáveis no mundo real
   (ex: molecular docking na triagem virtual de fármacos).
"""

import math
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.exact import (
    vertex_cover_brute_force,
    vertex_cover_branch_and_bound,
    tsp_brute_force,
    tsp_held_karp,
)
from src.generators import (
    generate_random_graph,
    generate_euclidean_tsp_instance,
)
from src.verification import (
    verify_vertex_cover_certificate,
    verify_tsp_certificate,
)


def format_time_estimate(seconds: float) -> str:
    """Converte segundos em uma representação humana legível."""
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f} microssegundos"
    if seconds < 1.0:
        return f"{seconds * 1e3:.1f} milissegundos"
    if seconds < 60:
        return f"{seconds:.2f} segundos"
    if seconds < 3600:
        return f"{seconds / 60:.1f} minutos"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} horas"
    if seconds < 31536000:
        return f"{seconds / 86400:.1f} dias"
    if seconds < 31536000 * 1000:
        return f"{seconds / 31536000:.1f} anos"
    if seconds < 31536000 * 1e9:
        return f"{seconds / (31536000 * 1e6):.2f} milhões de anos"
    return f"{seconds / (31536000 * 1e9):.2e} bilhões de anos (> idade do Universo: 13.8 bi anos)"


def print_theoretical_table():
    print("=" * 80)
    print("  TABELA TEORICA DA EXPLOSAO COMBINATORIA (Computador a 1 GHz = 10^9 ops/seg)")
    print("=" * 80)
    header = f"{'n':>4} | {'Forca Bruta TSP (n-1)!/2':>28} | {'Held-Karp n^2 2^n':>20} | {'Vertex Cover 2^n':>18}"
    print(header)
    print("-" * 80)

    test_ns = [5, 10, 15, 20, 25, 50, 100]
    ops_per_sec = 1e9

    for n in test_ns:
        # TSP Força bruta: (n-1)! / 2
        fact_routes = math.factorial(n - 1) // 2
        fact_time = fact_routes / ops_per_sec

        # TSP Held-Karp: n^2 * 2^n
        hk_ops = (n ** 2) * (2 ** n)
        hk_time = hk_ops / ops_per_sec

        # Vertex cover: 2^n
        vc_ops = 2 ** n
        vc_time = vc_ops / ops_per_sec

        print(f"{n:4d} | {format_time_estimate(fact_time):>28} | {format_time_estimate(hk_time):>20} | {format_time_estimate(vc_time):>18}")
    print("=" * 80)
    print("Obs: Idade estimada do Universo observavel ~ 13.8 bilhoes de anos (4.35 x 10^17 s).")
    print("Para n = 25 cidades, a forca bruta ja levaria milhoes de vezes a idade do Universo!\n")


def live_tsp_demo():
    print("=" * 80)
    print("  DEMONSTRAÇÃO EMPÍRICA AO VIVO: TSP (FORÇA BRUTA vs HELD-KARP)")
    print("=" * 80)
    print("Executando instâncias progressivas no seu hardware atual...\n")

    for n in range(4, 13):
        tsp_inst = generate_euclidean_tsp_instance(num_cities=n, seed=42 + n)
        matrix = tsp_inst.distance_matrix

        # Held-Karp
        t0 = time.perf_counter()
        opt_tour_hk, cost_hk = tsp_held_karp(matrix)
        t_hk = time.perf_counter() - t0

        # Força Bruta (até n=10 para tempo de resposta interativo aceitável)
        if n <= 10:
            t0 = time.perf_counter()
            opt_tour_bf, cost_bf = tsp_brute_force(matrix)
            t_bf = time.perf_counter() - t0
            bf_str = f"{t_bf * 1000:9.2f} ms"
            speedup = f"{t_bf / t_hk:.1f}x mais rápido"
        else:
            bf_str = "INTRAVÁVEL (> 10s)"
            # Estimativa de tempo teórico extrapolado
            estimated_bf = (t_bf if n == 11 else 0.5) * (n - 1)
            speedup = f"Extrapolado >> {n-1}x mais lento"

        print(f"Cidades: {n:2d} | Custo Ótimo: {cost_hk:7.2f} | "
              f"Held-Karp: {t_hk * 1000:7.2f} ms | "
              f"Força Bruta: {bf_str:18} | {speedup}")

    print("\n[Conclusão TSP]: O algoritmo de Held-Karp (Programação Dinâmica) viabiliza n=15..20,")
    print("mas para n > 30 até ele se torna inviável pela memória O(n 2^n).")
    print("Para n=100 cidades, apenas aproximações e metaheurísticas encontram soluções viáveis.\n")


def live_verification_demo():
    print("=" * 80)
    print("  DEMONSTRAÇÃO AO VIVO: VERIFICAÇÃO POLINOMIAL (A ESSÊNCIA DE NP)")
    print("=" * 80)
    print("Cenário: Encontrar o tour ótimo para 12 cidades exigiu resolver um problema NP-difícil.")
    print("No entanto, validar se uma rota proposta atende ao requisito é estritamente POLINOMIAL O(n)!\n")

    n = 12
    tsp_inst = generate_euclidean_tsp_instance(num_cities=n, seed=99)
    matrix = tsp_inst.distance_matrix

    print(f"1. Calculando tour ótimo para n = {n} cidades via Held-Karp...")
    opt_tour, opt_cost = tsp_held_karp(matrix)
    print(f"   -> Tour ótimo encontrado: {opt_tour}")
    print(f"   -> Custo ótimo: {opt_cost:.4f}")

    print("\n2. Executando verificador com Certificado Ótimo (L = custo ótimo):")
    t0 = time.perf_counter()
    res1 = verify_tsp_certificate(matrix, opt_tour, max_cost=opt_cost)
    t_v1 = time.perf_counter() - t0
    print(f"   Status: {'APROVADO' if res1.is_valid else 'REJEITADO'} em {t_v1 * 1e6:.1f} µs | Justificativa: {res1.reason}")

    print("\n3. Executando verificador com Certificado Subótimo / Inválido (L = custo ótimo - 1.0):")
    res2 = verify_tsp_certificate(matrix, opt_tour, max_cost=opt_cost - 1.0)
    print(f"   Status: {'APROVADO' if res2.is_valid else 'REJEITADO'} | Justificativa: {res2.reason}")

    print("\n4. Executando verificador com Certificado Malformado (cidade duplicada):")
    bad_tour = opt_tour[:-1] + [opt_tour[0]]
    res3 = verify_tsp_certificate(matrix, bad_tour, max_cost=opt_cost * 2)
    print(f"   Status: {'APROVADO' if res3.is_valid else 'REJEITADO'} | Justificativa: {res3.reason}")

    print("\n" + "=" * 80)
    print("  LIGAÇÃO COM O MUNDO REAL: MOLECULAR DOCKING & VIRTUAL SCREENING")
    print("=" * 80)
    print("Na triagem virtual de fármacos, busca-se a melhor conformação de um ligante químico")
    print("no sítio ativo de uma proteína alvo (receptor biológico).")
    print("Cada ligação rotacionável do ligante introduz um grau de liberdade contínuo.")
    print("Com apenas 10 ligações rotacionáveis discretizadas em 12 ângulos possíveis cada:")
    print("   Espaço de busca = 12^10 ≈ 61.917.364.224 (61,9 bilhões de conformações)!")
    print("Um algoritmo exato é COMPLETAMENTE IMPOSSÍVEL em tempo clínico hábil.")
    print("Por isso, softwares de ponta (como AutoDock Vina) utilizam Simulated Annealing,")
    print("Algoritmos Genéticos e Heurísticas de Otimização Estocástica — como desenvolvido pela Pessoa 5.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print_theoretical_table()
    live_tsp_demo()
    live_verification_demo()
