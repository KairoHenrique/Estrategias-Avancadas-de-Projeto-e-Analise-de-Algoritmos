"""
Script de benchmarks para algoritmos exatos (Vertex Cover e TSP).
Executa experimentos com entradas progressivas, mede tempos de execução (CPU/Wall-clock)
e gera gráficos demonstrando a explosão combinatória.
"""

import csv
import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Adiciona a pasta src ao sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import matplotlib.pyplot as plt
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


def run_vertex_cover_benchmarks():
    """Executa benchmarks de Cobertura de Vértices para entradas progressivas."""
    print("\n" + "=" * 60)
    print(">>> INICIANDO BENCHMARK: VERTEX COVER (EXATO)")
    print("=" * 60)

    ns = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    results = []

    for n in ns:
        g = generate_random_graph(num_vertices=n, edge_probability=0.35, seed=42 + n)

        # Mede Branch and Bound
        t0 = time.perf_counter()
        _, size_bb = vertex_cover_branch_and_bound(g)
        t_bb = time.perf_counter() - t0

        # Mede Força Bruta (limite de n para não travar a máquina)
        if n <= 18:
            t0 = time.perf_counter()
            _, size_bf = vertex_cover_brute_force(g)
            t_bf = time.perf_counter() - t0
        else:
            t_bf = None
            size_bf = size_bb

        print(f"|V| = {n:2d} | |E| = {g.num_edges:2d} | Cobertura Ótima: {size_bb:2d} | "
              f"B&B: {t_bb * 1000:8.3f} ms | "
              f"Força Bruta: {f'{t_bf * 1000:8.3f} ms' if t_bf is not None else 'PULADO (>18)'}")

        results.append({
            "n": n,
            "edges": g.num_edges,
            "optimal_size": size_bb,
            "time_bb_sec": t_bb,
            "time_bf_sec": t_bf,
        })

    return results


def run_tsp_benchmarks():
    """Executa benchmarks de TSP para entradas progressivas."""
    print("\n" + "=" * 60)
    print(">>> INICIANDO BENCHMARK: TSP (FORÇA BRUTA VS HELD-KARP)")
    print("=" * 60)

    ns = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    results = []

    for n in ns:
        tsp_inst = generate_euclidean_tsp_instance(num_cities=n, seed=100 + n)
        matrix = tsp_inst.distance_matrix

        # Mede Held-Karp
        t0 = time.perf_counter()
        _, cost_hk = tsp_held_karp(matrix)
        t_hk = time.perf_counter() - t0

        # Mede Força Bruta apenas para n <= 10 (10! / 2 = 181.440 rotas)
        # n = 11 já seriam 1,8 milhões de rotas, n = 12 seriam 19,9 milhões
        if n <= 10:
            t0 = time.perf_counter()
            _, cost_bf = tsp_brute_force(matrix)
            t_bf = time.perf_counter() - t0
        else:
            t_bf = None
            cost_bf = cost_hk

        print(f"Cidades (n) = {n:2d} | Custo Ótimo: {cost_hk:8.2f} | "
              f"Held-Karp: {t_hk * 1000:8.3f} ms | "
              f"Força Bruta: {f'{t_bf * 1000:8.3f} ms' if t_bf is not None else 'PULADO (>10)'}")

        results.append({
            "n": n,
            "optimal_cost": cost_hk,
            "time_hk_sec": t_hk,
            "time_bf_sec": t_bf,
        })

    return results


def save_results_and_plots(vc_results, tsp_results):
    """Salva os resultados em CSV e plota gráficos comparativos."""
    output_dir = BASE_DIR / "benchmarks" / "results"
    plots_dir = BASE_DIR / "benchmarks" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    # 1. Salva CSV Vertex Cover
    vc_csv = output_dir / "vertex_cover_benchmarks.csv"
    with open(vc_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "edges", "optimal_size", "time_bb_sec", "time_bf_sec"])
        writer.writeheader()
        writer.writerows(vc_results)
    print(f"\n[OK] CSV Vertex Cover salvo em: {vc_csv}")

    # 2. Salva CSV TSP
    tsp_csv = output_dir / "tsp_benchmarks.csv"
    with open(tsp_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "optimal_cost", "time_hk_sec", "time_bf_sec"])
        writer.writeheader()
        writer.writerows(tsp_results)
    print(f"[OK] CSV TSP salvo em: {tsp_csv}")

    # 3. Gráfico Vertex Cover
    plt.figure(figsize=(9, 5))
    vc_ns = [r["n"] for r in vc_results]
    vc_bb = [r["time_bb_sec"] * 1000 for r in vc_results]
    vc_bf_ns = [r["n"] for r in vc_results if r["time_bf_sec"] is not None]
    vc_bf = [r["time_bf_sec"] * 1000 for r in vc_results if r["time_bf_sec"] is not None]

    plt.plot(vc_bf_ns, vc_bf, "r-o", label=r"Força Bruta Exaustiva $O(2^n \cdot |E|)$", linewidth=2)
    plt.plot(vc_ns, vc_bb, "g-s", label=r"Branch-and-Bound Podado $O(2^k \cdot |E|)$", linewidth=2)
    plt.yscale("log")
    plt.title("Vertex Cover Exato: Força Bruta vs Branch-and-Bound", fontsize=13, fontweight="bold")
    plt.xlabel("Número de Vértices (|V|)", fontsize=11)
    plt.ylabel("Tempo de Execução (ms) - Escala Logarítmica", fontsize=11)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plot_vc_path = plots_dir / "benchmark_vertex_cover.png"
    plt.savefig(plot_vc_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico Vertex Cover gerado em: {plot_vc_path}")

    # 4. Gráfico TSP
    plt.figure(figsize=(9, 5))
    tsp_ns = [r["n"] for r in tsp_results]
    tsp_hk = [r["time_hk_sec"] * 1000 for r in tsp_results]
    tsp_bf_ns = [r["n"] for r in tsp_results if r["time_bf_sec"] is not None]
    tsp_bf = [r["time_bf_sec"] * 1000 for r in tsp_results if r["time_bf_sec"] is not None]

    plt.plot(tsp_bf_ns, tsp_bf, "r-o", label=r"Força Bruta Permutacional $\Theta((n-1)! \cdot n)$", linewidth=2)
    plt.plot(tsp_ns, tsp_hk, "b-^", label=r"Held-Karp Prog. Dinâmica $\Theta(n^2 2^n)$", linewidth=2)
    plt.yscale("log")
    plt.title("TSP Exato: Força Bruta $((n-1)!)$ vs Held-Karp $(n^2 2^n)$", fontsize=13, fontweight="bold")
    plt.xlabel("Número de Cidades (n)", fontsize=11)
    plt.ylabel("Tempo de Execução (ms) - Escala Logarítmica", fontsize=11)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plot_tsp_path = plots_dir / "benchmark_tsp.png"
    plt.savefig(plot_tsp_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico TSP gerado em: {plot_tsp_path}")


if __name__ == "__main__":
    vc_data = run_vertex_cover_benchmarks()
    tsp_data = run_tsp_benchmarks()
    save_results_and_plots(vc_data, tsp_data)
