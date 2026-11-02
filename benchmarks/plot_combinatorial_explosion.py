"""
Gera o gráfico comparativo de alto impacto da Explosão Combinatória e Intratabilidade
para ser utilizado diretamente nos slides da apresentação (substituindo a execução no terminal).
"""

import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
PLOTS_DIR = BASE_DIR / "benchmarks" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = PLOTS_DIR / "explosao_combinatoria_demonstracao.png"

# Configuração visual profissional
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Segoe UI", "Arial"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.2), dpi=300)

# ==============================================================================
# PAINEL 1: RESULTADOS EMPÍRICOS MEDIDOS EM HARDWARE REAL (MILISSEGUNDOS)
# ==============================================================================
ns_real = [4, 5, 6, 7, 8, 9, 10, 11, 12]
t_hk = [0.05, 0.06, 0.25, 0.33, 0.49, 1.19, 3.42, 7.90, 21.07]
# 11 e 12 extrapolados pelo limite de tempo do terminal (> 10s e ~2 min)
t_bf = [0.02, 0.05, 0.32, 1.21, 9.13, 88.88, 833.85, 10500.0, 120000.0]
t_verif = [0.015, 0.018, 0.020, 0.022, 0.024, 0.025, 0.026, 0.027, 0.028]

# Curvas
ax1.plot(ns_real[:7], t_bf[:7], "o-", color="#E53E3E", linewidth=2.8, markersize=8, label="Força Bruta: Medição Concluída")
ax1.plot(ns_real[6:], t_bf[6:], "o--", color="#E53E3E", linewidth=2.2, alpha=0.6, markersize=8, label="Força Bruta: Intratável / Timeout (> 10s)")
ax1.plot(ns_real, t_hk, "s-", color="#3182CE", linewidth=2.8, markersize=8, label="Held-Karp (Bitmask DP): O(n² 2ⁿ)")
ax1.plot(ns_real, t_verif, "d-", color="#38A169", linewidth=2.2, markersize=7, label="Verificador de Certificado: O(n)")

ax1.set_yscale("log")
ax1.set_title("Medições Empíricas Reais (Hardware do Projeto)\nTempo de Execução por Instância de TSP", fontsize=14, fontweight="bold", pad=12, color="#1A365D")
ax1.set_xlabel("Número de Cidades (n)", fontsize=12, fontweight="bold")
ax1.set_ylabel("Tempo de Execução (milissegundos) — Escala Logarítmica", fontsize=12, fontweight="bold")
ax1.set_xticks(ns_real)
ax1.grid(True, which="both", linestyle="--", alpha=0.5)

# Linhas de referência de usabilidade
ax1.axhline(1000, color="#DD6B20", linestyle=":", linewidth=1.8, alpha=0.85)
ax1.text(4.2, 1300, "Limite Interativo Humano (1 segundo)", color="#DD6B20", fontsize=10, fontweight="bold")

ax1.axhline(10000, color="#E53E3E", linestyle=":", linewidth=1.8, alpha=0.85)
ax1.text(4.2, 13000, "Limite de Tolerância / Congelamento (10 segundos)", color="#E53E3E", fontsize=10, fontweight="bold")

# Balões informativos
ax1.annotate("Held-Karp: 243x mais rápido!\n(3,4 ms vs 834 ms em n = 10)",
             xy=(10, 3.42), xytext=(6.5, 0.2),
             arrowprops=dict(facecolor="#3182CE", shrink=0.08, width=2, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF8FF", edgecolor="#3182CE", linewidth=1.5),
             fontsize=10.5, fontweight="bold", color="#2B6CB0")

ax1.annotate("Força Bruta INTRATÁVEL\n(trava a CPU em n ≥ 11)",
             xy=(11, 10500.0), xytext=(7.8, 30000.0),
             arrowprops=dict(facecolor="#E53E3E", shrink=0.08, width=2, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF5F5", edgecolor="#E53E3E", linewidth=1.5),
             fontsize=10.5, fontweight="bold", color="#9B2C2C")

ax1.annotate("Verificação Polinomial: ~26 µs\n(sempre instantânea em NP)",
             xy=(12, 0.028), xytext=(8.0, 0.003),
             arrowprops=dict(facecolor="#38A169", shrink=0.08, width=1.5, headwidth=7),
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#F0FFF4", edgecolor="#38A169", linewidth=1.5),
             fontsize=9.5, fontweight="bold", color="#276749")

ax1.set_ylim(0.001, 500000)
ax1.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.95, fontsize=10)

# ==============================================================================
# PAINEL 2: A PAREDE EXPONENCIAL TEÓRICA VS LIMITES DO UNIVERSO (1 GHz)
# ==============================================================================
ns_theo = np.arange(4, 32)
ops_per_sec = 1e9  # 1 GHz = 1 bilhão de operações por segundo

time_bf_sec = []
time_hk_sec = []
time_verif_sec = []

for n in ns_theo:
    # (n-1)! / 2 / 10^9
    t_b = (math.factorial(n - 1) / 2.0) / ops_per_sec
    time_bf_sec.append(t_b)
    # n^2 * 2^n / 10^9
    t_h = ((n**2) * (2**n)) / ops_per_sec
    time_hk_sec.append(t_h)
    # n / 10^9
    time_verif_sec.append(n / ops_per_sec)

time_bf_sec = np.array(time_bf_sec)
time_hk_sec = np.array(time_hk_sec)
time_verif_sec = np.array(time_verif_sec)

# Marcos de tempo físico em segundos
SEC_1_SEC = 1.0
SEC_1_DAY = 86400.0
SEC_1_YEAR = 31536000.0
SEC_UNIVERSE = 13.8e9 * SEC_1_YEAR  # ~4.35 x 10^17 segundos

ax2.plot(ns_theo, time_bf_sec, "-", color="#E53E3E", linewidth=3.0, label="Força Bruta TSP: (n-1)! / 2")
ax2.plot(ns_theo, time_hk_sec, "-", color="#3182CE", linewidth=3.0, label="Held-Karp: n² 2ⁿ")
ax2.plot(ns_theo, time_verif_sec, "-", color="#38A169", linewidth=2.5, label="Verificador Polinomial: O(n)")

ax2.set_yscale("log")
ax2.set_title("A Parede da Intratabilidade vs Limites Físicos\nTempo Teórico Estimado em CPU de 1 GHz (10⁹ ops/s)", fontsize=14, fontweight="bold", pad=12, color="#1A365D")
ax2.set_xlabel("Número de Cidades (n)", fontsize=12, fontweight="bold")
ax2.set_ylabel("Tempo Estimado (segundos) — Escala Logarítmica", fontsize=12, fontweight="bold")
ax2.grid(True, which="both", linestyle="--", alpha=0.5)

# Linhas de marco
ax2.axhline(SEC_1_SEC, color="#4A5568", linestyle="--", linewidth=1.2, alpha=0.7)
ax2.text(4.5, SEC_1_SEC * 2, "1 Segundo", color="#4A5568", fontsize=9.5, fontweight="bold")

ax2.axhline(SEC_1_DAY, color="#DD6B20", linestyle="--", linewidth=1.2, alpha=0.7)
ax2.text(4.5, SEC_1_DAY * 2, "1 Dia", color="#DD6B20", fontsize=9.5, fontweight="bold")

ax2.axhline(SEC_1_YEAR, color="#805AD5", linestyle="--", linewidth=1.4, alpha=0.8)
ax2.text(4.5, SEC_1_YEAR * 2.2, "1 Ano (n ≈ 19)", color="#805AD5", fontsize=9.5, fontweight="bold")

ax2.axhline(SEC_UNIVERSE, color="#C53030", linestyle="-", linewidth=2.2, alpha=0.95)
ax2.text(4.5, SEC_UNIVERSE * 2.5, "Idade do Universo Observável: 13,8 Bilhões de Anos (n ≈ 26)", color="#C53030", fontsize=10.5, fontweight="bold")

# Faixa destacando a barreira cosmológica
ax2.axhspan(SEC_UNIVERSE, 1e26, color="#FFF5F5", alpha=0.5)
ax2.text(18.5, 3e22, "BARREIRA INSUPERÁVEL DO UNIVERSO\n(Supera 13,8 bilhões de anos em n ≥ 26 cidades)", 
         color="#9B2C2C", fontsize=10.5, fontweight="bold", ha="center",
         bbox=dict(boxstyle="square,pad=0.5", facecolor="#FED7D7", edgecolor="#E53E3E", linewidth=1.5, alpha=0.9))

ax2.set_ylim(1e-10, 1e26)
ax2.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.95, fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300)
plt.close()
print(f"[SUCESSO] Gráfico da demonstração salvo em: {OUTPUT_FILE}")
