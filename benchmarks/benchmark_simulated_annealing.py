import csv
import sys
from pathlib import Path
from statistics import mean, stdev
from time import perf_counter

import matplotlib.pyplot as plt


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.metaheuristics.simulated_annealing import (
    generate_docking_problem,
    simulated_annealing,
    random_search,
)


# ============================================================
# CONFIGURAÇÕES DO EXPERIMENTO
# ============================================================

COMPLEXITIES = [2, 4, 6, 8, 10]

EVALUATION_BUDGETS = [
    100,
    1_000,
    10_000,
    100_000,
    1_000_000,
]

REPETITIONS = 5
BASE_SEED = 42

RESULTS_DIR = ROOT_DIR / "benchmarks" / "results"
PLOTS_DIR = ROOT_DIR / "benchmarks" / "plots"

CSV_PATH = RESULTS_DIR / "simulated_annealing_benchmarks.csv"

ENERGY_PLOT_PATH = (
    PLOTS_DIR / "simulated_annealing_energy.png"
)

RUNTIME_PLOT_PATH = (
    PLOTS_DIR / "simulated_annealing_runtime.png"
)


# ============================================================
# EXECUÇÃO DOS EXPERIMENTOS
# ============================================================

def run_benchmarks():
    """
    Compara Simulated Annealing e Random Search.

    Os algoritmos recebem a mesma instância em cada repetição
    e o mesmo orçamento de avaliações da função de energia.
    """

    results = []

    total_experiments = (
        len(COMPLEXITIES)
        * len(EVALUATION_BUDGETS)
        * REPETITIONS
        * 2
    )

    current_experiment = 0

    for complexity in COMPLEXITIES:

        for budget in EVALUATION_BUDGETS:

            sa_energies = []
            sa_times = []

            random_energies = []
            random_times = []

            for repetition in range(REPETITIONS):

                seed = (
                    BASE_SEED
                    + complexity * 100_000
                    + budget
                    + repetition
                )

                # Gera a instância usada pelos dois algoritmos.
                problem = generate_docking_problem(
                    complexity,
                    seed=seed,
                )

                # ------------------------------------------------
                # SIMULATED ANNEALING
                # ------------------------------------------------

                current_experiment += 1

                print(
                    f"[{current_experiment}/{total_experiments}] "
                    f"Simulated Annealing | "
                    f"complexidade={complexity} | "
                    f"avaliações={budget:,} | "
                    f"repetição={repetition + 1}/{REPETITIONS}",
                    flush=True,
                )

                start = perf_counter()

                sa_result = simulated_annealing(
                    problem,
                    iterations=budget - 1,
                    seed=seed,
                )

                sa_elapsed_ms = (
                    perf_counter() - start
                ) * 1000

                # A função retorna um dicionário.
                sa_energy = float(
                    sa_result["best_energy"]
                )

                sa_evaluations = int(
                    sa_result["evaluations"]
                )

                # Confere se o orçamento foi respeitado.
                if sa_evaluations != budget:
                    raise RuntimeError(
                        "Quantidade inesperada de avaliações "
                        "no Simulated Annealing: "
                        f"esperado={budget}, "
                        f"obtido={sa_evaluations}."
                    )

                sa_energies.append(sa_energy)
                sa_times.append(sa_elapsed_ms)

                # ------------------------------------------------
                # RANDOM SEARCH
                # ------------------------------------------------

                current_experiment += 1

                print(
                    f"[{current_experiment}/{total_experiments}] "
                    f"Random Search | "
                    f"complexidade={complexity} | "
                    f"avaliações={budget:,} | "
                    f"repetição={repetition + 1}/{REPETITIONS}",
                    flush=True,
                )

                start = perf_counter()

                random_result = random_search(
                    problem,
                    iterations=budget - 1,
                    seed=seed,
                )

                random_elapsed_ms = (
                    perf_counter() - start
                ) * 1000

                # A função também retorna um dicionário.
                random_energy = float(
                    random_result["best_energy"]
                )

                random_evaluations = int(
                    random_result["evaluations"]
                )

                if random_evaluations != budget:
                    raise RuntimeError(
                        "Quantidade inesperada de avaliações "
                        "no Random Search: "
                        f"esperado={budget}, "
                        f"obtido={random_evaluations}."
                    )

                random_energies.append(random_energy)
                random_times.append(random_elapsed_ms)

            # ====================================================
            # ESTATÍSTICAS
            # ====================================================

            sa_mean_energy = mean(sa_energies)
            random_mean_energy = mean(random_energies)

            sa_mean_time = mean(sa_times)
            random_mean_time = mean(random_times)

            results.append({
                "complexity": complexity,
                "evaluation_budget": budget,
                "method": "Simulated Annealing",
                "repetitions": REPETITIONS,
                "mean_energy": sa_mean_energy,
                "std_energy": stdev(sa_energies),
                "mean_runtime_ms": sa_mean_time,
                "std_runtime_ms": stdev(sa_times),
            })

            results.append({
                "complexity": complexity,
                "evaluation_budget": budget,
                "method": "Random Search",
                "repetitions": REPETITIONS,
                "mean_energy": random_mean_energy,
                "std_energy": stdev(random_energies),
                "mean_runtime_ms": random_mean_time,
                "std_runtime_ms": stdev(random_times),
            })

            # ====================================================
            # RESUMO NO TERMINAL
            # ====================================================

            print()
            print("=" * 65)
            print(f"Complexidade: {complexity}")
            print(f"Orçamento: {budget:,} avaliações")
            print(f"Repetições: {REPETITIONS}")
            print()

            print(
                f"Simulated Annealing | "
                f"Energia média: {sa_mean_energy:.6f} | "
                f"Desvio: {stdev(sa_energies):.6f} | "
                f"Tempo médio: {sa_mean_time:.2f} ms"
            )

            print(
                f"Random Search       | "
                f"Energia média: {random_mean_energy:.6f} | "
                f"Desvio: {stdev(random_energies):.6f} | "
                f"Tempo médio: {random_mean_time:.2f} ms"
            )

            print("=" * 65)
            print()

    return results


# ============================================================
# SALVAR RESULTADOS EM CSV
# ============================================================

def save_results(results):

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "complexity",
        "evaluation_budget",
        "method",
        "repetitions",
        "mean_energy",
        "std_energy",
        "mean_runtime_ms",
        "std_runtime_ms",
    ]

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"CSV salvo em: {CSV_PATH}")


# ============================================================
# GRÁFICO DE ENERGIA
# ============================================================

def plot_energy(results):

    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for complexity in COMPLEXITIES:

        plt.figure(figsize=(9, 6))

        for method in (
            "Simulated Annealing",
            "Random Search",
        ):

            selected = [
                row
                for row in results
                if row["complexity"] == complexity
                and row["method"] == method
            ]

            selected.sort(
                key=lambda row: row["evaluation_budget"]
            )

            budgets = [
                row["evaluation_budget"]
                for row in selected
            ]

            energies = [
                row["mean_energy"]
                for row in selected
            ]

            deviations = [
                row["std_energy"]
                for row in selected
            ]

            plt.errorbar(
                budgets,
                energies,
                yerr=deviations,
                marker="o",
                capsize=4,
                label=method,
            )

        plt.xscale("log")

        plt.xlabel("Número de avaliações")
        plt.ylabel("Energia média (menor é melhor)")

        plt.title(
            f"Energia por orçamento — complexidade {complexity}"
        )

        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        output_path = (
            PLOTS_DIR
            / f"simulated_annealing_energy_c{complexity}.png"
        )

        plt.savefig(
            output_path,
            dpi=300,
        )

        plt.close()

        print(f"Gráfico de energia salvo: {output_path}")


# ============================================================
# GRÁFICO DE TEMPO
# ============================================================

def plot_runtime(results):

    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for complexity in COMPLEXITIES:

        plt.figure(figsize=(9, 6))

        for method in (
            "Simulated Annealing",
            "Random Search",
        ):

            selected = [
                row
                for row in results
                if row["complexity"] == complexity
                and row["method"] == method
            ]

            selected.sort(
                key=lambda row: row["evaluation_budget"]
            )

            budgets = [
                row["evaluation_budget"]
                for row in selected
            ]

            runtimes = [
                row["mean_runtime_ms"]
                for row in selected
            ]

            deviations = [
                row["std_runtime_ms"]
                for row in selected
            ]

            plt.errorbar(
                budgets,
                runtimes,
                yerr=deviations,
                marker="o",
                capsize=4,
                label=method,
            )

        plt.xscale("log")
        plt.yscale("log")

        plt.xlabel("Número de avaliações")
        plt.ylabel("Tempo médio de execução (ms)")

        plt.title(
            f"Tempo por orçamento — complexidade {complexity}"
        )

        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        output_path = (
            PLOTS_DIR
            / f"simulated_annealing_runtime_c{complexity}.png"
        )

        plt.savefig(
            output_path,
            dpi=300,
        )

        plt.close()

        print(f"Gráfico de tempo salvo: {output_path}")


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():

    print("=" * 65)
    print("BENCHMARK: SIMULATED ANNEALING VS. RANDOM SEARCH")
    print("=" * 65)

    print(f"Complexidades: {COMPLEXITIES}")
    print(f"Orçamentos: {EVALUATION_BUDGETS}")
    print(f"Repetições por configuração: {REPETITIONS}")
    print()

    results = run_benchmarks()

    save_results(results)
    plot_energy(results)
    plot_runtime(results)

    print()
    print("=" * 65)
    print("EXPERIMENTO CONCLUÍDO!")
    print("=" * 65)


if __name__ == "__main__":
    main()
