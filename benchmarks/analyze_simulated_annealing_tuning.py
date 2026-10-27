import math
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURAÇÕES DE CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

INPUT_FILE = RESULTS_DIR / "simulated_annealing_tuning_results.csv"

SUMMARY_FILE = (
    RESULTS_DIR / "simulated_annealing_tuning_statistical_summary.csv"
)

COMPARISONS_FILE = (
    RESULTS_DIR / "simulated_annealing_tuning_comparisons.csv"
)


# ============================================================
# CONFIGURAÇÕES DA ANÁLISE
# ============================================================

CONFIGURATIONS = [
    "A_moderada",
    "B_intermediaria",
    "C_exploratoria",
]

BOOTSTRAP_REPETITIONS = 10_000
BASE_SEED = 42


# ============================================================
# INTERVALO DE CONFIANÇA POR BOOTSTRAP
# ============================================================

def bootstrap_mean_difference(
    differences,
    repetitions=BOOTSTRAP_REPETITIONS,
    seed=BASE_SEED,
):
    """
    Calcula a diferença média e um intervalo de confiança
    de 95% usando bootstrap pareado.

    A diferença é calculada como:

        configuração 1 - configuração 2

    Para energia e tempo de execução, uma diferença negativa
    favorece a primeira configuração.
    """

    differences = np.asarray(differences, dtype=float)
    differences = differences[np.isfinite(differences)]

    if len(differences) == 0:
        return np.nan, np.nan, np.nan

    rng = np.random.default_rng(seed)

    mean_difference = float(np.mean(differences))

    bootstrap_means = np.empty(repetitions)

    for i in range(repetitions):
        sample = rng.choice(
            differences,
            size=len(differences),
            replace=True,
        )

        bootstrap_means[i] = np.mean(sample)

    lower = float(np.percentile(bootstrap_means, 2.5))
    upper = float(np.percentile(bootstrap_means, 97.5))

    return mean_difference, lower, upper


# ============================================================
# TESTE EXATO DOS SINAIS
# ============================================================

def exact_sign_test(differences):
    """
    Executa um teste bilateral dos sinais das diferenças
    pareadas.

    H0: não existe preferência entre as duas configurações.

    Diferenças iguais a zero são desconsideradas.

    O teste considera a quantidade de diferenças positivas
    e negativas, não a magnitude das diferenças.
    """

    differences = np.asarray(differences, dtype=float)
    differences = differences[np.isfinite(differences)]

    positive = int(np.sum(differences > 0))
    negative = int(np.sum(differences < 0))

    n = positive + negative

    if n == 0:
        return np.nan, positive, negative

    smaller = min(positive, negative)

    probability = sum(
        math.comb(n, k)
        for k in range(smaller + 1)
    ) / (2 ** n)

    p_value = min(1.0, 2 * probability)

    return p_value, positive, negative


# ============================================================
# ESTATÍSTICAS DESCRITIVAS
# ============================================================

def summarize_metric(group, metric):
    """
    Calcula estatísticas descritivas para uma métrica.
    """

    values = group[metric].dropna()

    return {
        "mean": values.mean(),
        "median": values.median(),
        "std": values.std(),
        "min": values.min(),
        "max": values.max(),
    }


# ============================================================
# ANÁLISE PRINCIPAL
# ============================================================

def main():

    # Cria a pasta de resultados caso ela não exista.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # 1. VERIFICAR E CARREGAR OS DADOS
    # --------------------------------------------------------

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {INPUT_FILE}\n"
            "Execute primeiro o script de ajuste de parâmetros:\n"
            "python -m benchmarks.tune_simulated_annealing"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "complexity",
        "configuration",
        "best_energy",
        "runtime_seconds",
        "repetition",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Colunas ausentes no CSV: {sorted(missing)}\n"
            f"Colunas encontradas: {list(df.columns)}"
        )

    df["configuration"] = df["configuration"].astype(str)

    df = df[
        df["configuration"].isin(CONFIGURATIONS)
    ].copy()

    if df.empty:
        raise ValueError(
            "Nenhum resultado encontrado para as configurações "
            "A_moderada, B_intermediaria e C_exploratoria."
        )

    metrics = [
        "best_energy",
        "runtime_seconds",
    ]

    # --------------------------------------------------------
    # 2. ESTATÍSTICAS DESCRITIVAS
    # --------------------------------------------------------

    summary_rows = []

    grouped = df.groupby(
        ["complexity", "configuration"]
    )

    for (complexity, configuration), group in grouped:

        for metric in metrics:

            stats = summarize_metric(group, metric)

            summary_rows.append({
                "complexity": complexity,
                "configuration": configuration,
                "metric": metric,
                "n": group[metric].count(),
                **stats,
            })

    summary = pd.DataFrame(summary_rows)

    summary.to_csv(
        SUMMARY_FILE,
        index=False,
    )

    # --------------------------------------------------------
    # 3. COMPARAÇÕES PAREADAS
    # --------------------------------------------------------

    comparison_pairs = [
        ("A_moderada", "B_intermediaria"),
        ("A_moderada", "C_exploratoria"),
        ("B_intermediaria", "C_exploratoria"),
    ]

    comparison_rows = []

    complexities = sorted(
        df["complexity"].dropna().unique()
    )

    for complexity in complexities:

        complexity_df = df[
            df["complexity"] == complexity
        ]

        for metric in metrics:

            for config_1, config_2 in comparison_pairs:

                first = complexity_df[
                    complexity_df["configuration"] == config_1
                ][["repetition", metric]]

                second = complexity_df[
                    complexity_df["configuration"] == config_2
                ][["repetition", metric]]

                # Emparelha os resultados pela repetição.
                paired = first.merge(
                    second,
                    on="repetition",
                    suffixes=("_1", "_2"),
                    validate="one_to_one",
                )

                paired = paired.dropna()

                if paired.empty:
                    continue

                # Diferença:
                # configuração 1 - configuração 2.
                differences = (
                    paired[f"{metric}_1"]
                    - paired[f"{metric}_2"]
                ).to_numpy()

                # Intervalo de confiança por bootstrap.
                mean_diff, ci_lower, ci_upper = (
                    bootstrap_mean_difference(
                        differences,
                        seed=BASE_SEED + int(complexity),
                    )
                )

                # Teste exato dos sinais.
                p_value, positive, negative = exact_sign_test(
                    differences
                )

                comparison_rows.append({
                    "complexity": complexity,
                    "metric": metric,
                    "configuration_1": config_1,
                    "configuration_2": config_2,
                    "paired_repetitions": len(paired),
                    "mean_difference_1_minus_2": mean_diff,
                    "bootstrap_ci_95_lower": ci_lower,
                    "bootstrap_ci_95_upper": ci_upper,
                    "sign_test_p_value": p_value,
                    "repetitions_config1_higher": positive,
                    "repetitions_config1_lower": negative,
                })

    comparisons = pd.DataFrame(comparison_rows)

    comparisons.to_csv(
        COMPARISONS_FILE,
        index=False,
    )

    # --------------------------------------------------------
    # 4. EXIBIR OS RESULTADOS
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESUMO ESTATÍSTICO")
    print("=" * 70)

    print(
        summary.round(6).to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("COMPARAÇÕES PAREADAS")
    print("=" * 70)

    if not comparisons.empty:
        print(
            comparisons.round(6).to_string(index=False)
        )
    else:
        print(
            "Nenhuma comparação pôde ser realizada. "
            "Verifique os dados de entrada."
        )

    # --------------------------------------------------------
    # 5. CAMINHOS DOS ARQUIVOS GERADOS
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 70)

    print("\nArquivos gerados:")

    print(f"- {SUMMARY_FILE}")
    print(f"- {COMPARISONS_FILE}")

    print("\nOs arquivos foram salvos em:")
    print(f"- {RESULTS_DIR}")


if __name__ == "__main__":
    main()