# Tema 6: Problemas NP-Completos e Aproximações

[![CI Testes Unitários](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/actions/workflows/tests.yml/badge.svg)](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Trabalho prático e teórico da disciplina (enunciado oficial em [`docs/pratica.pdf`](docs/pratica.pdf)).  
**Entregáveis:** Relatório técnico-científico (formato monografia/livro via AVA), Pitch Técnico/Seminário (40 minutos) e Implementação de Referência neste repositório GitHub.

- **Disciplina:** Estratégias Avançadas de Projeto e Análise de Algoritmos
- **Professor:** Michel Pires da Silva, DECOM-DV — CEFET-MG / UFCI-MG
- **Livro-base:** Cormen et al., *Algoritmos: Teoria e Prática* (3ª/4ª Ed.) — Cap. 34 (NP-Completude) e Cap. 35 (Algoritmos de Aproximação)

---

## Integrantes e Divisão de Papéis

| Papel | Integrante | GitHub | Responsabilidade Principal |
|---|---|---|---|
| Pessoa 1 — Relatório (teoria) | Igor | [@1g0rX](https://github.com/1g0rX) | Cap. 1 (Introdução), Cap. 2 (Fundamentação, P vs NP, Reduções) e Cap. 6 (Conclusão) |
| Pessoa 2 — Relatório (engenharia e custos) | Maria Eduarda | [@mariaeduarda-ab](https://github.com/mariaeduarda-ab) | Cap. 3 (Pseudocódigos e Diagramas), Cap. 4 (Análise Assintótica) e Apêndice (Cheat Sheet) |
| Pessoa 3 — Algoritmos exatos e infraestrutura | Kairo Henrique | [@KairoHenrique](https://github.com/KairoHenrique) | Infraestrutura, Soluções Exatas (Força Bruta e Held-Karp), Verificadores Polinomiais e Benchmarks |
| Pessoa 4 — Algoritmos de aproximação | Heitor | [@HeitorHenriqueZ](https://github.com/HeitorHenriqueZ) | APPROX-VERTEX-COVER (fator 2), APPROX-TSP-TOUR (fator 2) e GREEDY-SET-COVER (H(n)) |
| Pessoa 5 — Metaheurísticas e experimentos | Jade | [@Jade-Souza](https://github.com/Jade-Souza) | Simulated Annealing / Algoritmo Genético, Estudo de Caso (Docking Molecular) e Cap. 5 |

---

## Prazos e Cronograma

| Marco | Data | Status |
|---|---|---|
| Fundamentação + esqueleto do código e testes prontos | 18/10/2026 | Concluído |
| Implementação + experimentos concluídos | 25/10/2026 | Em andamento |
| Revisão final do relatório e slides | 30/10/2026 | Planejado |
| **Submissão no AVA** | **01/11/2026** | **Prazo Final** |
| Apresentação Oral / Seminário (40 min) | 11/11/2026 | Agendado |

---

## Escopo Técnico do Projeto

1. **Classes de Complexidade:** P, NP, NP-Difícil, NP-Completo; Verificadores determinísticos em tempo polinomial e certificados polinomiais (testemunhas).
2. **Discussão sobre P ≠ NP:** Problema do milênio do Clay Mathematics Institute; consequências do colapso P = NP na criptografia assimétrica moderna (RSA, Curvas Elípticas) e na otimização global; argumentos da comunidade científica a favor de P ≠ NP.
3. **Reduções Polinomiais:** $\text{CIRCUIT-SAT} \to \text{SAT} \to \text{3-SAT} \to \text{CLIQUE} \to \text{VERTEX-COVER}$ (Teorema de Cook-Levin como base).
4. **Explosão Combinatória e Intratabilidade:** Demonstração analítica e empírica do crescimento fatorial $((n-1)!/2)$ e exponencial $(2^n)$.
5. **Algoritmos Exatos:**
   - **Vertex Cover:** Força Bruta Enumerativa ($O(2^n \cdot |E|)$) e Branch-and-Bound com Poda ($O(2^k \cdot |E|)$).
   - **TSP:** Força Bruta Permutacional ($\Theta((n-1)! \cdot n)$) e Programação Dinâmica com Máscara de Bits — Algoritmo de Held-Karp ($\Theta(n^2 2^n)$).
6. **Verificadores Polinomiais:**
   - Vertex Cover: verificação de cobertura e cardinalidade em $O(|V| + |E|)$.
   - TSP: verificação de ciclo hamiltoniano e custo $\le L$ em $O(n)$.
7. **Algoritmos de Aproximação (Cap. 35):** APPROX-VERTEX-COVER (razão 2), APPROX-TSP-TOUR via Árvore Geradora Mínima (razão 2 em métrica euclidiana com desigualdade triangular) e GREEDY-SET-COVER (razão harmônica $H(n)$).
8. **Estudo de Caso do Mundo Real:** *Molecular Docking* e Triagem Virtual de Fármacos (*Virtual Screening*), onde o espaço conformacional de ligantes flexíveis com dezenas de torções angulares cresce exponencialmente ($k^m$), tornando abordagens exatas inviáveis e exigindo aproximações e metaheurísticas.

---

## Estrutura do Repositório

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml             # Workflow de CI no GitHub Actions (Ubuntu & Windows, Python 3.10-3.12)
├── src/
│   ├── exact/
│   │   ├── vertex_cover.py       # Cobertura de Vértices: Força Bruta e Branch-and-Bound
│   │   └── tsp.py                # TSP: Força Bruta e Held-Karp (Programação Dinâmica)
│   ├── verification/
│   │   └── verifier.py           # Verificadores de Certificado Polinomial (O(|V|+|E|) e O(n))
│   └── generators/
│       └── instances.py          # Geradores de grafos e TSP euclidiano com semente fixa
├── tests/
│   ├── test_generators.py        # Testes de reprodutibilidade e desigualdade triangular
│   ├── test_vertex_cover.py      # Testes do Vertex Cover contra grafos clássicos (Petersen, Kn, Cn)
│   ├── test_tsp.py               # Testes do TSP e equivalência estrita Força Bruta vs Held-Karp
│   └── test_verifier.py          # Testes com certificados válidos, inválidos e subótimos
├── benchmarks/
│   ├── benchmark_exact.py        # Medição progressiva de tempo de execução, exportação CSV e PNG
│   ├── demo_combinatorial_explosion.py  # Script interativo de demonstração para o seminário
│   ├── results/                  # CSVs de tempos medidos
│   └── plots/                    # Gráficos em escala logarítmica gerados
├── slides/
│   ├── slides_algoritmos_exatos.md      # Slides em formato Marp para a apresentação da Pessoa 3
│   └── roteiro_apresentacao_kairo.md   # Guia de fala cronometrado (8 minutos)
├── docs/
│   └── pratica.pdf               # Enunciado oficial fornecido pelo professor
├── pyproject.toml                # Configurações do pacote Python e pytest
├── requirements.txt              # Dependências do projeto fixadas
└── README.md
```

---

## Tabela de Complexidades Assintóticas

| Módulo / Algoritmo | Paradigma | Tempo (Pior Caso) | Tempo (Melhor/Médio) | Espaço Auxiliar | Observação |
|---|---|---|---|---|---|
| **Vertex Cover (Força Bruta)** | Enumeração de Subconjuntos | $O(2^n \cdot \|E\|)$ | $\Omega(\|E\|)$ | $O(n)$ | Inviável para $n > 25$ |
| **Vertex Cover (Branch-and-Bound)** | Backtracking com Poda | $O(2^k \cdot \|E\|)$ | $O(\|E\|)$ | $O(n)$ | $k \le n$ é a cobertura ótima |
| **TSP (Força Bruta)** | Permutação de Rotas | $\Theta((n-1)! \cdot n)$ | $\Theta((n-1)! \cdot n)$ | $O(n)$ | Inviável para $n > 10$ |
| **TSP (Held-Karp)** | Programação Dinâmica | $\Theta(n^2 2^n)$ | $\Theta(n^2 2^n)$ | $\Theta(n 2^n)$ | Viável até $n \approx 20$; barreira de RAM |
| **Verificador Vertex Cover** | Certificado Polinomial | $O(\|V\| + \|E\|)$ | $O(\|V\| + \|E\|)$ | $O(\|V\|)$ | Estritamente linear em NP |
| **Verificador TSP** | Certificado Polinomial | $O(n)$ | $O(n)$ | $O(n)$ | Linear no número de cidades |

---

## Instruções de Instalação e Execução

### 1. Pré-requisitos
- Python 3.10 ou superior instalado ([python.org](https://www.python.org/)).
- Git instalado.

### 2. Clonar o Repositório
```bash
git clone https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos.git
cd Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos
```

### 3. Criar e Ativar Ambiente Virtual (Recomendado)
- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```

---

## Execução dos Testes Unitários

O projeto possui suíte completa de testes unitários com mais de 40 casos de teste cobrindo instâncias de solução conhecida (grafo de Petersen, ciclos, cliques, triângulos, grafos bipartidos), equivalência exata entre algoritmos, validação da desigualdade triangular métrica e testes dos verificadores polinomiais:

```bash
pytest
```

---

## Execução dos Benchmarks e Gráficos

Para reproduzir os experimentos de complexidade assintótica com entradas progressivas e gerar os gráficos em escala logarítmica:

```bash
python benchmarks/benchmark_exact.py
```
Os resultados são salvos em:
- `benchmarks/results/vertex_cover_benchmarks.csv`
- `benchmarks/results/tsp_benchmarks.csv`
- `benchmarks/plots/benchmark_vertex_cover.png`
- `benchmarks/plots/benchmark_tsp.png`

---

## Demonstração Interativa ao Vivo (Seminário)

Para executar a demonstração interativa durante a apresentação do seminário:

```bash
python benchmarks/demo_combinatorial_explosion.py
```

O script exibirá:
1. A tabela matemática do tempo estimado para $n=5 \dots 100$ em um processador a 1 GHz comparado com a idade do Universo.
2. Execução progressiva ao vivo demonstrando a aceleração do Held-Karp (>160x mais rápido que força bruta para $n=10$) e o congelamento da força bruta.
3. Demonstração dos verificadores polinomiais rodando em microssegundos ($O(n)$ e $O(|V| + |E|)$).
4. Explicação do estudo de caso real de *Molecular Docking* e triagem virtual de fármacos.

---

## Detalhes das Tarefas do Projeto (GitHub Project)

- **Quadro de Tarefas Geral:** [GitHub Project #6](https://github.com/users/KairoHenrique/projects/6)
- **Todas as Issues:** [Lista de Issues](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues)
- **Milestone Principal:** [Entrega AVA - 01/11/2026](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/milestone/1)
