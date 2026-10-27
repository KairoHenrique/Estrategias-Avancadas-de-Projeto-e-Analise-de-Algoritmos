"""
Experimento de ajuste de parâmetros do Simulated Annealing.

Compara três configurações de temperatura usando:
- As mesmas instâncias de docking;
- As mesmas sementes aleatórias;
- O mesmo orçamento de avaliações;
- Repetições independentes e reproduzíveis.

Resultados:
- simulated_annealing_tuning_results.csv
- simulated_annealing_tuning_summary.csv
"""

import csv
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path

from src.metaheuristics.simulated_annealing import (
    generate_docking_problem,
    simulated_annealing,
)


# ============================================================
# CONFIGURAÇÕES DO EXPERIMENTO
# ============================================================

COMPLEXITIES = [2, 6, 10]

EVALUATION_BUDGET = 10_000

REPETITIONS = 30

BASE_SEED = 42

# Mantemos a temperatura final constante para isolar
# o efeito da temperatura inicial.
CONFIGURATIONS = {
    "A_moderada": {
        "initial_temperature": 1.0,
        "final_temperature": 0.01,
    },
    "B_intermediaria": {
        "initial_temperature": 2.0,
        "final_temperature": 0.01,
    },
    "C_exploratoria": {
        "initial_temperature": 5.0,
        "final_temperature": 0.01,
    },
}

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "results"
OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

RAW_RESULTS_FILE = (
    OUTPUT_DIRECTORY / "simulated_annealing_tuning_results.csv"
)

SUMMARY_FILE = (
    OUTPUT_DIRECTORY / "simulated_annealing_tuning_summary.csv"
)


# ============================================================
# EXECUÇÃO DOS EXPERIMENTOS
# ============================================================

def run_experiment():
    """Executa e registra os experimentos de ajuste de parâmetros."""

    results = []

    total_runs = (
        len(COMPLEXITIES)
        * len(CONFIGURATIONS)
        * REPETITIONS
    )

    current_run = 0

    print("=" * 65)
    print("AJUSTE DE PARÂMETROS - SIMULATED ANNEALING")
    print("=" * 65)

    print(f"Configurações: {len(CONFIGURATIONS)}")
    print(f"Complexidades: {COMPLEXITIES}")
    print(f"Avaliações por execução: {EVALUATION_BUDGET}")
    print(f"Repetições: {REPETITIONS}")
    print(f"Total de execuções: {total_runs}")
    print()

    for complexity in COMPLEXITIES:
        print(f"\nComplexidade: {complexity}")

        for repetition in range(REPETITIONS):
            # A mesma instância e a mesma semente serão utilizadas
            # por todas as configurações nesta repetição.
            seed = BASE_SEED + repetition

            problem = generate_docking_problem(
                complexity=complexity,
                seed=seed,
            )

            for config_name, parameters in CONFIGURATIONS.items():
                current_run += 1

                start_time = time.perf_counter()

                result = simulated_annealing(
                    problem=problem,
                    iterations=EVALUATION_BUDGET - 1,
                    initial_temperature=parameters[
                        "initial_temperature"
                    ],
                    final_temperature=parameters[
                        "final_temperature"
                    ],
                    seed=seed,
                )

                elapsed_time = time.perf_counter() - start_time

                row = {
                    "configuration": config_name,
                    "initial_temperature": parameters[
                        "initial_temperature"
                    ],
                    "final_temperature": parameters[
                        "final_temperature"
                    ],
                    "complexity": complexity,
                    "repetition": repetition + 1,
                    "seed": seed,
                    "evaluation_budget": EVALUATION_BUDGET,
                    "evaluations": result["evaluations"],
                    "best_energy": result["best_energy"],
                    "runtime_seconds": elapsed_time,
                }

                results.append(row)

                print(
                    f"[{current_run}/{total_runs}] "
                    f"Complexidade={complexity} | "
                    f"Configuração={config_name} | "
                    f"Energia={result['best_energy']:.6f} | "
                    f"Tempo={elapsed_time:.4f}s"
                )

    save_raw_results(results)
    save_summary(results)

    print("\n" + "=" * 65)
    print("EXPERIMENTOS CONCLUÍDOS")
    print("=" * 65)

    print(f"\nResultados completos: {RAW_RESULTS_FILE}")
    print(f"Resumo estatístico: {SUMMARY_FILE}")

    print_summary(results)


# ============================================================
# SALVAMENTO DOS RESULTADOS
# ============================================================

def save_raw_results(results):
    """Salva os dados individuais de todas as execuções."""

    if not results:
        raise ValueError("Nenhum resultado foi produzido.")

    with RAW_RESULTS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )

        writer.writeheader()
        writer.writerows(results)


def save_summary(results):
    """Calcula e salva estatísticas por configuração e complexidade."""

    grouped_results = defaultdict(list)

    for result in results:
        key = (
            result["configuration"],
            result["complexity"],
        )

        grouped_results[key].append(result)

    summary = []

    for (configuration, complexity), group in sorted(
        grouped_results.items()
    ):
        energies = [
            item["best_energy"]
            for item in group
        ]

        runtimes = [
            item["runtime_seconds"]
            for item in group
        ]

        summary.append({
            "configuration": configuration,
            "complexity": complexity,
            "repetitions": len(group),
            "mean_best_energy": statistics.mean(energies),
            "median_best_energy": statistics.median(energies),
            "std_best_energy": (
                statistics.stdev(energies)
                if len(energies) > 1
                else 0.0
            ),
            "min_best_energy": min(energies),
            "max_best_energy": max(energies),
            "mean_runtime_seconds": statistics.mean(runtimes),
            "initial_temperature": CONFIGURATIONS[
                configuration
            ]["initial_temperature"],
            "final_temperature": CONFIGURATIONS[
                configuration
            ]["final_temperature"],
        })

    with SUMMARY_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(summary[0].keys()),
        )

        writer.writeheader()
        writer.writerows(summary)


# ============================================================
# APRESENTAÇÃO DO RESUMO
# ============================================================

def print_summary(results):
    """Exibe uma comparação simples das configurações."""

    grouped_results = defaultdict(list)

    for result in results:
        key = (
            result["configuration"],
            result["complexity"],
        )

        grouped_results[key].append(result["best_energy"])

    print("\nRESUMO DAS CONFIGURAÇÕES")
    print("-" * 85)

    print(
        f"{'Configuração':<22}"
        f"{'Complexidade':<15}"
        f"{'Energia média':<20}"
        f"{'Desvio padrão':<20}"
    )

    print("-" * 85)

    for (configuration, complexity), energies in sorted(
        grouped_results.items()
    ):
        mean_energy = statistics.mean(energies)

        std_energy = (
            statistics.stdev(energies)
            if len(energies) > 1
            else 0.0
        )

        print(
            f"{configuration:<22}"
            f"{complexity:<15}"
            f"{mean_energy:<20.6f}"
            f"{std_energy:<20.6f}"
        )

    print("-" * 85)
    print(
        "\nLembrete: como a função objetivo é de minimização, "
        "energias menores indicam soluções melhores no modelo."
    )


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    random.seed(BASE_SEED)
    run_experiment()