import csv
import math
import random
import statistics
import sys
import time

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt


# Permite importar os módulos de src mesmo quando o script
# é executado diretamente a partir da pasta benchmarks.
ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.metaheuristics.simulated_annealing import (
    generate_docking_problem,
    simulated_annealing,
    random_search
)


# ============================================================
# CONFIGURAÇÃO DO EXPERIMENTO
# ============================================================

COMPLEXITIES = [2, 4, 6, 8, 10]

EVALUATION_BUDGETS = [
    100,
    1000,
    10000,
    100000,
    1000000
]

REPETITIONS = 30
BASE_SEED = 42

# Número de amostras utilizadas no bootstrap.
BOOTSTRAP_SAMPLES = 10000

CONFIDENCE_LEVEL = 0.95

# Diferenças menores que esta tolerância serão consideradas empates.
TIE_TOLERANCE = 1e-12


RESULTS_DIR = ROOT_DIR / "benchmarks" / "results"
PLOTS_DIR = ROOT_DIR / "benchmarks" / "plots"

CSV_PATH = (
    RESULTS_DIR / "simulated_annealing_benchmarks.csv"
)

SUMMARY_CSV_PATH = (
    RESULTS_DIR / "simulated_annealing_summary.csv"
)

STATISTICS_CSV_PATH = (
    RESULTS_DIR / "simulated_annealing_statistics.csv"
)


# ============================================================
# ESTATÍSTICAS DESCRITIVAS
# ============================================================

def calculate_statistics(values):
    """Calcula a média e o desvio-padrão amostral."""
    mean_value = statistics.mean(values)

    if len(values) >= 2:
        std_value = statistics.stdev(values)
    else:
        std_value = 0.0

    return mean_value, std_value


def percentile(sorted_values, probability):
    """
    Calcula um percentil usando interpolação linear.

    probability deve estar entre 0 e 1.
    """
    if not sorted_values:
        raise ValueError("A lista de valores não pode estar vazia.")

    if not 0 <= probability <= 1:
        raise ValueError("O percentil deve estar entre 0 e 1.")

    position = (len(sorted_values) - 1) * probability

    lower_index = math.floor(position)
    upper_index = math.ceil(position)

    if lower_index == upper_index:
        return sorted_values[lower_index]

    fraction = position - lower_index

    return (
        sorted_values[lower_index] * (1 - fraction)
        + sorted_values[upper_index] * fraction
    )


# ============================================================
# INTERVALO DE CONFIANÇA POR BOOTSTRAP PAREADO
# ============================================================

def paired_bootstrap_confidence_interval(
    differences,
    seed,
    samples=BOOTSTRAP_SAMPLES,
    confidence_level=CONFIDENCE_LEVEL
):
    """
    Calcula um intervalo de confiança bootstrap para a média
    das diferenças pareadas.

    Cada diferença corresponde a:

        energia do Simulated Annealing
        menos
        energia do Random Search

    Diferenças negativas favorecem o Simulated Annealing.

    O bootstrap reamostra as diferenças pareadas, preservando
    a associação entre os resultados dos dois algoritmos.
    """
    if not differences:
        raise ValueError("É necessário fornecer diferenças.")

    if samples < 1:
        raise ValueError("samples deve ser maior que zero.")

    if not 0 < confidence_level < 1:
        raise ValueError(
            "confidence_level deve estar entre 0 e 1."
        )

    rng = random.Random(seed)
    sample_size = len(differences)

    bootstrap_means = []

    for _ in range(samples):
        resampled = [
            differences[rng.randrange(sample_size)]
            for _ in range(sample_size)
        ]

        bootstrap_means.append(statistics.mean(resampled))

    bootstrap_means.sort()

    alpha = 1 - confidence_level

    lower = percentile(
        bootstrap_means,
        alpha / 2
    )

    upper = percentile(
        bootstrap_means,
        1 - alpha / 2
    )

    return lower, upper


# ============================================================
# TESTE BINOMIAL EXATO DOS SINAIS
# ============================================================

def exact_sign_test(wins, losses):
    """
    Calcula o valor-p bilateral do teste binomial exato dos sinais.

    Empates são excluídos.

    Hipótese nula:
        entre as diferenças não empatadas, cada algoritmo tem
        probabilidade de 0,5 de apresentar a menor energia.

    Este teste considera a frequência das vitórias, não a
    magnitude das diferenças.
    """
    n = wins + losses

    if n == 0:
        return 1.0

    smaller_count = min(wins, losses)

    lower_tail = sum(
        math.comb(n, k)
        for k in range(smaller_count + 1)
    ) / (2 ** n)

    return min(1.0, 2 * lower_tail)


# ============================================================
# EXECUÇÃO DO BENCHMARK
# ============================================================

def run_benchmark():
    """
    Compara Simulated Annealing e Random Search.

    Para cada complexidade e repetição, a mesma instância é
    utilizada em todos os orçamentos de avaliações.

    Os algoritmos também usam sementes próprias, reproduzíveis
    e distintas entre si.

    A análise estatística é feita separadamente para cada
    combinação de complexidade e orçamento.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_results = []

    for complexity in COMPLEXITIES:
        print(
            f"\nExecutando experimentos "
            f"com complexidade {complexity}..."
        )

        for repetition in range(REPETITIONS):

            # A instância depende somente da complexidade
            # e da repetição, nunca do orçamento.
            problem_seed = (
                BASE_SEED
                + complexity * 100_000
                + repetition
            )

            problem = generate_docking_problem(
                complexity=complexity,
                seed=problem_seed
            )

            # Sementes próprias para cada algoritmo.
            # Elas não dependem do orçamento, permitindo
            # reprodutibilidade entre as configurações.
            sa_seed = (
                BASE_SEED
                + complexity * 100_000
                + repetition * 2
                + 1
            )

            random_seed = (
                BASE_SEED
                + complexity * 100_000
                + repetition * 2
                + 2
            )

            for budget in EVALUATION_BUDGETS:
                iterations = budget - 1

                # --------------------------------------------
                # SIMULATED ANNEALING
                # --------------------------------------------

                start_sa = time.perf_counter()

                sa_result = simulated_annealing(
                    problem=problem,
                    iterations=iterations,
                    seed=sa_seed
                )

                sa_elapsed_ms = (
                    time.perf_counter() - start_sa
                ) * 1000

                # --------------------------------------------
                # RANDOM SEARCH
                # --------------------------------------------

                start_random = time.perf_counter()

                random_result = random_search(
                    problem=problem,
                    iterations=iterations,
                    seed=random_seed
                )

                random_elapsed_ms = (
                    time.perf_counter() - start_random
                ) * 1000

                # --------------------------------------------
                # VALIDAÇÃO DO ORÇAMENTO
                # --------------------------------------------

                if sa_result["evaluations"] != budget:
                    raise RuntimeError(
                        "Simulated Annealing utilizou "
                        f"{sa_result['evaluations']} avaliações; "
                        f"esperado: {budget}."
                    )

                if random_result["evaluations"] != budget:
                    raise RuntimeError(
                        "Random Search utilizou "
                        f"{random_result['evaluations']} avaliações; "
                        f"esperado: {budget}."
                    )

                # Diferença pareada:
                # negativa favorece SA;
                # positiva favorece Random Search.
                energy_difference = (
                    sa_result["best_energy"]
                    - random_result["best_energy"]
                )

                raw_results.append({
                    "complexity": complexity,
                    "budget": budget,
                    "repetition": repetition + 1,

                    "problem_seed": problem_seed,
                    "sa_seed": sa_seed,
                    "random_seed": random_seed,

                    "sa_best_energy": sa_result["best_energy"],
                    "sa_evaluations": sa_result["evaluations"],
                    "sa_elapsed_ms": sa_elapsed_ms,

                    "random_best_energy": random_result["best_energy"],
                    "random_evaluations": random_result["evaluations"],
                    "random_elapsed_ms": random_elapsed_ms,

                    "energy_difference_sa_minus_random":
                        energy_difference
                })

                print(
                    f"  Orçamento: {budget:>7} | "
                    f"Repetição: {repetition + 1:>2}/{REPETITIONS} | "
                    f"SA: {sa_result['best_energy']:.6f} | "
                    f"Random: {random_result['best_energy']:.6f}"
                )

    # Salva as execuções individuais.
    save_raw_results(raw_results)

    # Calcula as estatísticas descritivas.
    summary_results = build_summary(raw_results)
    save_summary_results(summary_results)

    # Calcula as diferenças pareadas e os testes estatísticos.
    statistical_results = build_statistical_analysis(raw_results)
    save_statistical_results(statistical_results)

    # Gera os gráficos.
    for complexity in COMPLEXITIES:
        plot_energy(summary_results, complexity)
        plot_runtime(summary_results, complexity)

    print("\nExperimento concluído!")
    print(f"Resultados individuais: {CSV_PATH}")
    print(f"Resumo descritivo: {SUMMARY_CSV_PATH}")
    print(f"Análise estatística: {STATISTICS_CSV_PATH}")
    print(f"Gráficos: {PLOTS_DIR}")

    return raw_results, summary_results, statistical_results


# ============================================================
# SALVAMENTO DOS RESULTADOS
# ============================================================

def save_csv(path, results):
    """Salva uma lista de dicionários em um arquivo CSV."""
    if not results:
        return

    with path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(results[0].keys())
        )

        writer.writeheader()
        writer.writerows(results)


def save_raw_results(results):
    """Salva os resultados individuais de todas as execuções."""
    save_csv(CSV_PATH, results)


def save_summary_results(summary_results):
    """Salva as médias e os desvios-padrão."""
    save_csv(SUMMARY_CSV_PATH, summary_results)


def save_statistical_results(statistical_results):
    """Salva as diferenças pareadas e a análise estatística."""
    save_csv(STATISTICS_CSV_PATH, statistical_results)


# ============================================================
# RESUMO DESCRITIVO
# ============================================================

def build_summary(raw_results):
    """
    Agrupa os resultados por complexidade e orçamento.

    Calcula médias e desvios-padrão de energia e tempo.
    """
    summary = []

    for complexity in COMPLEXITIES:
        for budget in EVALUATION_BUDGETS:

            group = [
                result
                for result in raw_results
                if (
                    result["complexity"] == complexity
                    and result["budget"] == budget
                )
            ]

            if not group:
                continue

            sa_energies = [
                result["sa_best_energy"]
                for result in group
            ]

            random_energies = [
                result["random_best_energy"]
                for result in group
            ]

            sa_times = [
                result["sa_elapsed_ms"]
                for result in group
            ]

            random_times = [
                result["random_elapsed_ms"]
                for result in group
            ]

            sa_energy_mean, sa_energy_std = calculate_statistics(
                sa_energies
            )

            random_energy_mean, random_energy_std = (
                calculate_statistics(random_energies)
            )

            sa_time_mean, sa_time_std = calculate_statistics(
                sa_times
            )

            random_time_mean, random_time_std = (
                calculate_statistics(random_times)
            )

            summary.append({
                "complexity": complexity,
                "budget": budget,
                "repetitions": len(group),

                "sa_energy_mean": sa_energy_mean,
                "sa_energy_std": sa_energy_std,

                "random_energy_mean": random_energy_mean,
                "random_energy_std": random_energy_std,

                "sa_time_mean_ms": sa_time_mean,
                "sa_time_std_ms": sa_time_std,

                "random_time_mean_ms": random_time_mean,
                "random_time_std_ms": random_time_std
            })

    return summary


# ============================================================
# ANÁLISE ESTATÍSTICA PAREADA
# ============================================================

def build_statistical_analysis(raw_results):
    """
    Analisa a diferença de energia entre os algoritmos.

    Para cada complexidade e orçamento, calcula:
      - média e desvio-padrão das diferenças pareadas;
      - intervalo de confiança bootstrap de 95%;
      - vitórias, empates e derrotas;
      - valor-p do teste binomial exato dos sinais.

    Convenção:
      diferença = energia SA - energia Random Search.

      diferença negativa favorece SA;
      diferença positiva favorece Random Search.
    """
    statistical_results = []

    for complexity in COMPLEXITIES:
        for budget in EVALUATION_BUDGETS:

            group = [
                result
                for result in raw_results
                if (
                    result["complexity"] == complexity
                    and result["budget"] == budget
                )
            ]

            if not group:
                continue

            differences = [
                result["energy_difference_sa_minus_random"]
                for result in group
            ]

            mean_difference, std_difference = (
                calculate_statistics(differences)
            )

            # Para o bootstrap, a semente é fixa por configuração.
            # Isso torna o intervalo reproduzível.
            bootstrap_seed = (
                BASE_SEED
                + complexity * 100_000
                + budget
            )

            ci_lower, ci_upper = (
                paired_bootstrap_confidence_interval(
                    differences=differences,
                    seed=bootstrap_seed
                )
            )

            sa_wins = sum(
                difference < -TIE_TOLERANCE
                for difference in differences
            )

            random_wins = sum(
                difference > TIE_TOLERANCE
                for difference in differences
            )

            ties = (
                len(differences)
                - sa_wins
                - random_wins
            )

            p_value = exact_sign_test(
                wins=sa_wins,
                losses=random_wins
            )

            if mean_difference < 0:
                better_mean = "Simulated Annealing"
            elif mean_difference > 0:
                better_mean = "Random Search"
            else:
                better_mean = "Empate"

            # O intervalo de confiança se refere à média
            # da diferença pareada, não a cada execução individual.
            if ci_upper < 0:
                ci_interpretation = (
                    "Intervalo favorece Simulated Annealing"
                )
            elif ci_lower > 0:
                ci_interpretation = (
                    "Intervalo favorece Random Search"
                )
            else:
                ci_interpretation = (
                    "Intervalo inclui zero"
                )

            statistical_results.append({
                "complexity": complexity,
                "budget": budget,
                "repetitions": len(differences),

                "mean_energy_difference_sa_minus_random":
                    mean_difference,

                "std_energy_difference":
                    std_difference,

                "ci95_lower": ci_lower,
                "ci95_upper": ci_upper,

                "sa_wins": sa_wins,
                "random_wins": random_wins,
                "ties": ties,

                "sign_test_p_value": p_value,

                "better_mean_energy": better_mean,
                "bootstrap_ci_interpretation":
                    ci_interpretation
            })

    return statistical_results


# ============================================================
# GRÁFICO DE ENERGIA
# ============================================================

def plot_energy(summary_results, complexity):
    """Gera o gráfico de energia média por orçamento."""
    data = [
        result
        for result in summary_results
        if result["complexity"] == complexity
    ]

    if not data:
        return

    budgets = [result["budget"] for result in data]

    sa_means = [
        result["sa_energy_mean"]
        for result in data
    ]

    sa_stds = [
        result["sa_energy_std"]
        for result in data
    ]

    random_means = [
        result["random_energy_mean"]
        for result in data
    ]

    random_stds = [
        result["random_energy_std"]
        for result in data
    ]

    plt.figure(figsize=(10, 6))

    plt.errorbar(
        budgets,
        sa_means,
        yerr=sa_stds,
        marker="o",
        capsize=4,
        label="Simulated Annealing"
    )

    plt.errorbar(
        budgets,
        random_means,
        yerr=random_stds,
        marker="s",
        capsize=4,
        label="Random Search"
    )

    plt.xscale("log")

    plt.xlabel("Orçamento de avaliações")
    plt.ylabel("Energia média (menor é melhor)")

    plt.title(
        f"Energia por orçamento — complexidade {complexity}"
    )

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    output_path = (
        PLOTS_DIR
        / f"simulated_annealing_energy_c{complexity}.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()


# ============================================================
# GRÁFICO DE TEMPO
# ============================================================

def plot_runtime(summary_results, complexity):
    """Gera o gráfico de tempo médio por orçamento."""
    data = [
        result
        for result in summary_results
        if result["complexity"] == complexity
    ]

    if not data:
        return

    budgets = [result["budget"] for result in data]

    sa_means = [
        result["sa_time_mean_ms"]
        for result in data
    ]

    sa_stds = [
        result["sa_time_std_ms"]
        for result in data
    ]

    random_means = [
        result["random_time_mean_ms"]
        for result in data
    ]

    random_stds = [
        result["random_time_std_ms"]
        for result in data
    ]

    plt.figure(figsize=(10, 6))

    plt.errorbar(
        budgets,
        sa_means,
        yerr=sa_stds,
        marker="o",
        capsize=4,
        label="Simulated Annealing"
    )

    plt.errorbar(
        budgets,
        random_means,
        yerr=random_stds,
        marker="s",
        capsize=4,
        label="Random Search"
    )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Orçamento de avaliações")
    plt.ylabel("Tempo médio (ms)")

    plt.title(
        f"Tempo de execução — complexidade {complexity}"
    )

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    output_path = (
        PLOTS_DIR
        / f"simulated_annealing_runtime_c{complexity}.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    run_benchmark()