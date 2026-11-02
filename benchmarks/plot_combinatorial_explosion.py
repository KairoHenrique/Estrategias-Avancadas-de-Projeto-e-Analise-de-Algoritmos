"""
Gera o gráfico comparativo de alto impacto da Explosão Combinatória e Intratabilidade
para ser utilizado diretamente nos slides da apresentação (substituindo a execução no terminal).
Versão refinada com espaçamento perfeito, legenda unificada e sem sobreposições.
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
t_bf_measured = [0.02, 0.05, 0.32, 1.21, 9.13, 88.88, 833.85]
t_bf_timeout = [833.85, 10500.0, 120000.0]
t_verif = [0.015, 0.018, 0.020, 0.022, 0.024, 0.025, 0.026, 0.027, 0.028]

l_bf, = ax1.plot(ns_real[:7], t_bf_measured, "o-", color="#E53E3E", linewidth=3.2, markersize=8.5, label="Força Bruta: Medição Real")
l_bft, = ax1.plot(ns_real[6:], t_bf_timeout, "o--", color="#E53E3E", linewidth=2.4, alpha=0.6, markersize=8.5, label="Força Bruta: Intratável / Timeout (> 10s)")
l_hk, = ax1.plot(ns_real, t_hk, "s-", color="#2B6CB0", linewidth=3.2, markersize=8.5, label="Held-Karp (Bitmask DP): O(n² 2ⁿ)")
l_verif, = ax1.plot(ns_real, t_verif, "d-", color="#276749", linewidth=2.8, markersize=7.5, label="Verificador de Certificado: O(n) (~26 µs)")

ax1.set_yscale("log")
ax1.set_ylim(0.005, 300000)
ax1.set_xlim(3.5, 12.5)
ax1.set_xticks(ns_real)

# Linhas de referência de usabilidade
ax1.axhline(1000, color="#DD6B20", linestyle=":", linewidth=1.6, alpha=0.85)
ax1.text(3.7, 1300, "Limite Interativo (1 segundo)", color="#DD6B20", fontsize=9.5, fontweight="bold")

ax1.axhline(10000, color="#C53030", linestyle=":", linewidth=1.6, alpha=0.85)
ax1.text(3.7, 13000, "Limite de Tolerância / Congelamento (10 segundos)", color="#C53030", fontsize=9.5, fontweight="bold")

# Balão 1: Força Bruta timeout
ax1.annotate("Força Bruta CONGELA o terminal!\n(extrapola para > 10 segundos)",
             xy=(11, 10500.0), xytext=(6.5, 45000.0),
             arrowprops=dict(facecolor="#E53E3E", edgecolor="#C53030", shrink=0.08, width=2, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF5F5", edgecolor="#E53E3E", linewidth=1.6),
             fontsize=10.5, fontweight="bold", color="#9B2C2C")

# Balão 2: Held-Karp
ax1.annotate("Held-Karp: 243x mais rápido\n(3,4 ms vs 834 ms em n = 10)",
             xy=(10, 3.42), xytext=(9.1, 0.18),
             arrowprops=dict(facecolor="#2B6CB0", edgecolor="#2C5282", shrink=0.08, width=2, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF8FF", edgecolor="#3182CE", linewidth=1.6),
             fontsize=10, fontweight="bold", color="#2B6CB0")

ax1.set_title("1. Medições Empíricas Reais (Hardware do Projeto)\nTempo de Execução Real por Número de Cidades (TSP)", fontsize=13.5, fontweight="bold", pad=12, color="#1A365D")
ax1.set_xlabel("Número de Cidades (n)", fontsize=11.5, fontweight="bold")
ax1.set_ylabel("Tempo de Execução (milissegundos) — Escala Logarítmica", fontsize=11.5, fontweight="bold")
ax1.grid(True, which="both", linestyle="--", alpha=0.45)

# ==============================================================================
# PAINEL 2: A PAREDE EXPONENCIAL TEÓRICA VS LIMITES DO UNIVERSO (1 GHz)
# ==============================================================================
ns_theo = np.arange(4, 32)
ops_per_sec = 1e9  # 1 GHz = 1 bilhão de operações por segundo

time_bf_sec = [(math.factorial(n - 1) / 2.0) / ops_per_sec for n in ns_theo]
time_hk_sec = [((n**2) * (2**n)) / ops_per_sec for n in ns_theo]
time_verif_sec = [n / ops_per_sec for n in ns_theo]

time_bf_sec = np.array(time_bf_sec)
time_hk_sec = np.array(time_hk_sec)
time_verif_sec = np.array(time_verif_sec)

# Marcos de tempo físico em segundos
SEC_1_SEC = 1.0
SEC_1_YEAR = 31536000.0
SEC_UNIVERSE = 13.8e9 * SEC_1_YEAR  # ~4.35 x 10^17 segundos

ax2.plot(ns_theo, time_bf_sec, "-", color="#E53E3E", linewidth=3.4, label="Força Bruta TSP: (n-1)! / 2")
ax2.plot(ns_theo, time_hk_sec, "-", color="#2B6CB0", linewidth=3.4, label="Held-Karp: n² 2ⁿ")
ax2.plot(ns_theo, time_verif_sec, "-", color="#276749", linewidth=2.8, label="Verificador Polinomial: O(n)")

ax2.set_yscale("log")
ax2.set_ylim(1e-10, 1e25)
ax2.set_xlim(3.5, 31.5)

# Linhas de marco com caixas brancas de fundo para legibilidade perfeita
ax2.axhline(SEC_1_SEC, color="#718096", linestyle="--", linewidth=1.2, alpha=0.7)
ax2.text(4.0, SEC_1_SEC * 2.5, "1 Segundo", color="#4A5568", fontsize=9.5, fontweight="bold",
         bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85))

ax2.axhline(SEC_1_YEAR, color="#805AD5", linestyle="--", linewidth=1.4, alpha=0.75)
ax2.text(4.0, SEC_1_YEAR * 2.5, "1 Ano (n ≈ 19 cidades)", color="#6B46C1", fontsize=9.5, fontweight="bold",
         bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85))

ax2.axhline(SEC_UNIVERSE, color="#C53030", linestyle="-", linewidth=2.2, alpha=0.9)
ax2.text(4.0, SEC_UNIVERSE * 2.5, "Idade do Universo Observável: 13,8 Bilhões de Anos", color="#C53030", fontsize=10, fontweight="bold",
         bbox=dict(boxstyle="square,pad=0.25", facecolor="#FFF5F5", edgecolor="#FEB2B2", alpha=0.9))

# Faixa destacando a barreira cosmológica
ax2.axhspan(SEC_UNIVERSE, 1e25, color="#FED7D7", alpha=0.35)
ax2.text(12.5, 3e21, "BARREIRA DO UNIVERSO (n ≥ 26)\nTempo supera 13,8 bilhões de anos", 
         color="#9B2C2C", fontsize=11, fontweight="bold", ha="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF5F5", edgecolor="#E53E3E", linewidth=1.8, alpha=0.95))

ax2.set_title("2. A Parede da Intratabilidade vs Limites Físicos\nTempo Teórico Estimado em CPU de 1 GHz (10⁹ ops/s)", fontsize=13.5, fontweight="bold", pad=12, color="#1A365D")
ax2.set_xlabel("Número de Cidades (n)", fontsize=11.5, fontweight="bold")
ax2.set_ylabel("Tempo Estimado (segundos) — Escala Logarítmica", fontsize=11.5, fontweight="bold")
ax2.grid(True, which="both", linestyle="--", alpha=0.45)

# Legenda Unificada na base da figura
handles = [l_bf, l_bft, l_hk, l_verif]
labels = [h.get_label() for h in handles]
fig.legend(handles, labels, loc="lower center", ncol=4, frameon=True, facecolor="white", edgecolor="#CBD5E0", fontsize=10.5, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
fig.subplots_adjust(bottom=0.12)
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.close()
print(f"[SUCESSO] Gráfico refinado salvo em: {OUTPUT_FILE}")
