"""
Razão de aproximação empírica: aproximado vs. ótimo (Issues #12, #52 e #53).

Para cada problema, executa o algoritmo exato e o de aproximação NAS MESMAS instâncias
(semente fixa), em pelo menos 3 tamanhos de entrada, e registra:
    razão empírica ρ = custo_aproximado / custo_ótimo  (>= 1)
comparando-a com o fator teórico do Cormen (Cap. 35):
    - APPROX-VERTEX-COVER: 2
    - APPROX-TSP-TOUR (métrico): 2
    - GREEDY-SET-COVER: H(max|S|)

Saídas:
    benchmarks/results/approximation_ratio.csv          (dados brutos por instância)
    benchmarks/results/approximation_ratio_summary.csv  (média/mín/máx por tamanho)
    benchmarks/plots/approximation_ratio.png            (gráfico gerado A PARTIR do CSV)

Uso:
    python benchmarks/benchmark_approximation.py              # roda experimentos + gráfico
    python benchmarks/benchmark_approximation.py --plot-only  # só regera o gráfico do CSV
"""

import argparse
import csv
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.approximation import (
    approx_vertex_cover,
    approx_tsp_tour,
    greedy_set_cover,
    set_cover_brute_force,
    generate_set_cover_instance,
    harmonic_number,
    is_valid_set_cover,
)
from src.exact import vertex_cover_branch_and_bound, tsp_held_karp, is_valid_vertex_cover
from src.generators import generate_random_graph, generate_euclidean_tsp_instance

RESULTS_DIR = BASE_DIR / "benchmarks" / "results"
PLOTS_DIR = BASE_DIR / "benchmarks" / "plots"
RAW_CSV = RESULTS_DIR / "approximation_ratio.csv"
SUMMARY_CSV = RESULTS_DIR / "approximation_ratio_summary.csv"
PLOT_PATH = PLOTS_DIR / "approximation_ratio.png"

# Parâmetros dos experimentos (semente base fixa => reprodutível)
SEEDS_PER_SIZE = 10
VC_SIZES = [8, 12, 16, 20]          # |V|, grafo G(n, p)
VC_EDGE_PROB = 0.3
TSP_SIZES = [6, 8, 10, 12]          # n cidades euclidianas
SC_SIZES = [8, 12, 16, 18]          # |F| subconjuntos
SC_UNIVERSE = 30                    # |X|
SC_DENSITY = 0.15

FIELDS = [
    "problema", "n", "seed", "custo_aprox", "custo_otimo", "razao",
    "fator_teorico", "t_aprox_s", "t_exato_s",
]


def _timed(fn, *args):
    t0 = time.perf_counter()
    out = fn(*args)
    return out, time.perf_counter() - t0


def run_vertex_cover():
    rows = []
    print("\n>>> APPROX-VERTEX-COVER vs Branch-and-Bound")
    for n in VC_SIZES:
        for s in range(SEEDS_PER_SIZE):
            seed = 1000 * n + s
            g = generate_random_graph(n, VC_EDGE_PROB, seed=seed)
            if g.num_edges == 0:
                continue
            (cover, approx), ta = _timed(approx_vertex_cover, g)
            (_, opt), te = _timed(vertex_cover_branch_and_bound, g)
            assert is_valid_vertex_cover(g, cover)
            rows.append(dict(problema="vertex_cover", n=n, seed=seed, custo_aprox=approx,
                             custo_otimo=opt, razao=approx / opt, fator_teorico=2.0,
                             t_aprox_s=ta, t_exato_s=te))
        _print_size(rows, "vertex_cover", n)
    return rows


def run_tsp():
    rows = []
    print("\n>>> APPROX-TSP-TOUR vs Held-Karp (instâncias euclidianas)")
    for n in TSP_SIZES:
        for s in range(SEEDS_PER_SIZE):
            seed = 1000 * n + s
            m = generate_euclidean_tsp_instance(n, seed=seed).distance_matrix
            (_, approx), ta = _timed(approx_tsp_tour, m)
            (_, opt), te = _timed(tsp_held_karp, m)
            rows.append(dict(problema="tsp", n=n, seed=seed, custo_aprox=approx,
                             custo_otimo=opt, razao=approx / opt, fator_teorico=2.0,
                             t_aprox_s=ta, t_exato_s=te))
        _print_size(rows, "tsp", n)
    return rows


def run_set_cover():
    rows = []
    print(f"\n>>> GREEDY-SET-COVER vs Força Bruta (|X| = {SC_UNIVERSE})")
    for n in SC_SIZES:
        for s in range(SEEDS_PER_SIZE):
            seed = 1000 * n + s
            inst = generate_set_cover_instance(SC_UNIVERSE, n, SC_DENSITY, seed=seed)
            (chosen, approx), ta = _timed(greedy_set_cover, inst)
            (_, opt), te = _timed(set_cover_brute_force, inst)
            assert is_valid_set_cover(inst, chosen)
            rows.append(dict(problema="set_cover", n=n, seed=seed, custo_aprox=approx,
                             custo_otimo=opt, razao=approx / opt,
                             fator_teorico=harmonic_number(inst.max_subset_size),
                             t_aprox_s=ta, t_exato_s=te))
        _print_size(rows, "set_cover", n)
    return rows


def _print_size(rows, problem, n):
    r = [x for x in rows if x["problema"] == problem and x["n"] == n]
    ratios = [x["razao"] for x in r]
    print(f"  n = {n:2d} | instâncias = {len(r):2d} | razão média = {statistics.mean(ratios):.4f} | "
          f"máx = {max(ratios):.4f} | fator teórico médio = {statistics.mean(x['fator_teorico'] for x in r):.3f} | "
          f"t_aprox médio = {statistics.mean(x['t_aprox_s'] for x in r) * 1000:.3f} ms | "
          f"t_exato médio = {statistics.mean(x['t_exato_s'] for x in r) * 1000:.3f} ms")


def save_csv(rows):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"\n[OK] CSV bruto salvo em: {RAW_CSV}")

    groups = defaultdict(list)
    for r in rows:
        groups[(r["problema"], r["n"])].append(r)
    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["problema", "n", "instancias", "razao_media", "razao_min", "razao_max",
                    "fator_teorico_medio", "t_aprox_medio_s", "t_exato_medio_s"])
        for (p, n), g in groups.items():
            ratios = [x["razao"] for x in g]
            w.writerow([p, n, len(g), statistics.mean(ratios), min(ratios), max(ratios),
                        statistics.mean(x["fator_teorico"] for x in g),
                        statistics.mean(x["t_aprox_s"] for x in g),
                        statistics.mean(x["t_exato_s"] for x in g)])
    print(f"[OK] CSV resumo salvo em: {SUMMARY_CSV}")


def plot_from_csv(csv_path=RAW_CSV, out_path=PLOT_PATH):
    """Issue #53: gera o gráfico da razão empírica vs. fator teórico lendo o CSV."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = defaultdict(lambda: defaultdict(list))
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            data[r["problema"]][int(r["n"])].append((float(r["razao"]), float(r["fator_teorico"])))

    panels = [
        ("vertex_cover", "APPROX-VERTEX-COVER", "Número de vértices |V|"),
        ("tsp", "APPROX-TSP-TOUR (euclidiano)", "Número de cidades n"),
        ("set_cover", "GREEDY-SET-COVER", "Número de subconjuntos |F|"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (key, title, xlabel) in zip(axes, panels):
        if key not in data:
            ax.set_visible(False)
            continue
        ns = sorted(data[key])
        means = [statistics.mean(r for r, _ in data[key][n]) for n in ns]
        mins = [min(r for r, _ in data[key][n]) for n in ns]
        maxs = [max(r for r, _ in data[key][n]) for n in ns]
        factors = [statistics.mean(fa for _, fa in data[key][n]) for n in ns]

        ax.errorbar(ns, means, yerr=[[m - lo for m, lo in zip(means, mins)],
                                     [hi - m for m, hi in zip(means, maxs)]],
                    fmt="o-", color="#2b6cb0", ecolor="#90cdf4", capsize=5, linewidth=2,
                    label="Razão empírica (média, mín–máx)")
        ax.plot(ns, factors, "--", color="#c53030", linewidth=2,
                label="Fator teórico (ρ = 2 para VC/TSP; H(max|S|) para Set Cover)")
        ax.text(ns[-1], factors[-1], "  " + ("H(d)" if key == "set_cover" else "2"),
                color="#c53030", va="bottom", ha="right", fontsize=10, fontweight="bold")
        ax.axhline(1.0, color="gray", linestyle=":", linewidth=1, label="Ótimo (ρ = 1)")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Custo aproximado / custo ótimo")
        ax.set_xticks(ns)
        ax.set_ylim(0.9, max(max(factors), max(maxs)) * 1.1)
        ax.grid(True, linestyle="--", alpha=0.6)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=10, frameon=False)
    fig.suptitle("Razão de aproximação empírica vs. fator teórico (Cormen, Cap. 35)",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0.07, 1, 1])
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"[OK] Gráfico salvo em: {out_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plot-only", action="store_true", help="apenas regera o gráfico a partir do CSV")
    args = parser.parse_args()

    if not args.plot_only:
        rows = run_vertex_cover() + run_tsp() + run_set_cover()
        save_csv(rows)
    plot_from_csv()


if __name__ == "__main__":
    main()
