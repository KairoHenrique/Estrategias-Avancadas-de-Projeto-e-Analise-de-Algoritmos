# Tema 6: Problemas NP-Completos e Aproximações

[![CI Testes Unitários](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/actions/workflows/tests.yml/badge.svg)](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/actions)
[![Testes Unitários](https://img.shields.io/badge/Testes-101%20passando-success.svg)](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repositório acadêmico contendo o desenvolvimento teórico, formal, analítico e experimental do **Tema 6: Problemas NP-Completos e Algoritmos de Aproximação**, fundamentado nos Capítulos 34 e 35 do livro *Algoritmos: Teoria e Prática* (Cormen et al.).

- **Instituição:** Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG)  
- **Departamento:** Departamento de Computação e Mecânica (DECOM-DV)  
- **Disciplina:** Estratégias Avançadas de Projeto e Análise de Algoritmos  
- **Professor:** Michel Pires da Silva  
- **Autores:** Kairo Henrique, Heitor Henrique, Jade Souza, Igor e Maria Eduarda  

---

## 📌 Visão Geral e Motivação Teórica

O cerne deste trabalho é investigar os limites da computabilidade eficiente e as estratégias práticas para lidar com a intratabilidade computacional inerente aos problemas NP-Completos e NP-Difíceis.

### 1. O Problema Motivador: A Parede da Explosão Combinatória
> *"Por que nenhum supercomputador do mundo consegue encontrar a rota de entrega ótima para apenas 100 cidades?"*

No Problema do Caixeiro-Viajante (TSP), o número de rotas possíveis é dado por:
$$\frac{(n-1)!}{2} \implies \text{Para } n = 100: \quad \frac{99!}{2} \approx 4{,}66 \times 10^{155} \text{ rotas.}$$

Para efeito de escala: existem aproximadamente $10^{80}$ átomos em todo o universo observável. Se cada átomo fosse um supercomputador calculando 1 bilhão de rotas por segundo desde o Big Bang ($13{,}8$ bilhões de anos), não teria verificado nem mesmo uma fração microscópica dessa quantidade de rotas.

### 2. A Assimetria Fundamental de NP e os Verificadores Polinomiais
Enquanto *encontrar* uma solução ótima para um problema NP-Difícil exige varrer um espaço de busca exponencial ou fatorial, *verificar* a validade de uma solução proposta (certificado/testemunha) pode ser feito de forma determinística e ultrarrápida em tempo polinomial. O projeto implementa e demonstra essa assimetria na prática: validar um certificado leva microssegundos, enquanto achá-lo pode levar eras.

### 3. A Conexão com o Mundo Real: Triagem de Fármacos (*Molecular Docking*)
A intratabilidade não é uma abstração matemática: na medicina e na indústria farmacêutica, simular a conformação geométrica ótima em que um fármaco (ligante) se acopla a uma proteína receptora (*Molecular Docking*) envolve múltiplos ângulos contínuos de torção. Para uma molécula com apenas 10 ligações rotacionáveis discretizadas em passos de $30^\circ$, o espaço conformacional alcança:
$$12^{10} \approx 6{,}19 \times 10^{10} \text{ conformações!}$$
Isso inviabiliza algoritmos exatos em tempo clínico hábil, exigindo algoritmos de aproximação com garantias matemáticas e metaheurísticas estocásticas (*Simulated Annealing*).

---

## ⚙️ Módulos e Algoritmos Implementados

### 1. Algoritmos Exatos
* **Vertex Cover (Cobertura de Vértices):**
  * *Força Bruta Enumerativa:* Testa subconjuntos em ordem de cardinalidade crescente — $\mathcal{O}(2^n \cdot |E|)$ tempo, $\mathcal{O}(n)$ espaço.
  * *Branch-and-Bound com Poda:* Ramificação por aresta não coberta com descarte de ramos não promissores — $\mathcal{O}(2^k \cdot |E|)$, onde $k \le n$ é o tamanho da cobertura ótima.
* **Traveling Salesperson Problem (TSP):**
  * *Força Bruta Permutacional:* Enumera todos os ciclos hamiltonianos possíveis — $\Theta((n-1)! \cdot n)$ tempo, $\mathcal{O}(n)$ espaço.
  * *Held-Karp (Programação Dinâmica com Bitmask):* Resolve recursivamente por memoização de subconjuntos de cidades visitadas — $\Theta(n^2 2^n)$ tempo, $\Theta(n 2^n)$ espaço auxiliar.

### 2. Verificadores Polinomiais de Certificados (NP)
* **Verificador de Vertex Cover:** Recebe grafo $G$, teto $k$ e conjunto $C \subseteq V$. Checa se $|C| \le k$ e se toda aresta $(u, v) \in E$ possui $u \in C \lor v \in C$ em tempo estritamente linear $\mathcal{O}(|V| + |E|)$.
* **Verificador de TSP:** Recebe matriz de distâncias $D$, limitante $L$ e ciclo $P$. Checa se $P$ é permutação válida e se $\sum D \le L$ em tempo $\mathcal{O}(n)$.

### 3. Algoritmos de Aproximação (Capítulo 35 do Cormen)
* **APPROX-VERTEX-COVER (Cap. 35.1):** 2-aproximação polinomial em tempo linear $\mathcal{O}(|V| + |E|)$ baseada na construção de um emparelhamento maximal de arestas.
* **APPROX-TSP-TOUR (Cap. 35.2):** 2-aproximação para TSP métrico com desigualdade triangular em tempo $\Theta(V^2)$, combinando Árvore Geradora Mínima (Algoritmo de Prim) e percurso em pré-ordem com atalhos diretos.
* **GREEDY-SET-COVER (Cap. 35.3):** Heurística gulosa para cobertura de conjuntos com garantia teórica harmônica $H(d) = \sum_{i=1}^d \frac{1}{i} \le \ln(d) + 1$, onde $d = \max |S|$.

### 4. Metaheurísticas e Estudo de Caso de Docking
* **Simulated Annealing (Recozimento Simulado):** Otimizador estocástico com resfriamento geométrico ($T_{k+1} = \alpha T_k$) e critério de aceitação de Metropolis para explorar superfícies energéticas acidentadas e escapar de ótimos locais.

---

## 📊 Tabela Consolidada de Complexidades

| Módulo / Algoritmo | Paradigma | Tempo (Pior Caso) | Tempo (Melhor/Médio) | Espaço Auxiliar | Garantia / Observação |
|---|---|---|---|---|---|
| **Vertex Cover (Força Bruta)** | Enumeração de Subconjuntos | $\mathcal{O}(2^n \cdot \|E\|)$ | $\Omega(\|E\|)$ | $\mathcal{O}(n)$ | Solução ótima exata; inviável para $n > 25$ |
| **Vertex Cover (Branch-and-Bound)** | Backtracking com Poda | $\mathcal{O}(2^k \cdot \|E\|)$ | $\mathcal{O}(\|E\|)$ | $\mathcal{O}(n)$ | $k \le n$ é a cobertura ótima |
| **TSP (Força Bruta)** | Permutação de Rotas | $\Theta((n-1)! \cdot n)$ | $\Theta((n-1)! \cdot n)$ | $\mathcal{O}(n)$ | Inviável para $n > 10$ |
| **TSP (Held-Karp)** | Programação Dinâmica | $\Theta(n^2 2^n)$ | $\Theta(n^2 2^n)$ | $\Theta(n 2^n)$ | Viável até $n \approx 20$; barreira de RAM para $n > 25$ |
| **Verificador Vertex Cover** | Certificado Polinomial | $\mathcal{O}(\|V\| + \|E\|)$ | $\mathcal{O}(\|V\| + \|E\|)$ | $\mathcal{O}(\|V\|)$ | Verificação determinística linear em NP |
| **Verificador TSP** | Certificado Polinomial | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Verificação determinística linear em NP |
| **APPROX-VERTEX-COVER** | Emparelhamento Maximal | $\mathcal{O}(\|V\| + \|E\|)$ | $\mathcal{O}(\|V\| + \|E\|)$ | $\mathcal{O}(\|V\|)$ | 2-aproximação comprovada ($\rho = 2$) |
| **APPROX-TSP-TOUR** | Prim (MST) + Pré-Ordem | $\Theta(V^2)$ | $\Theta(V^2)$ | $\Theta(V)$ | 2-aproximação em TSP Métrico ($\rho = 2$) |
| **GREEDY-SET-COVER** | Heurística Gulosa | $\mathcal{O}(\|X\| \cdot \|\mathcal{F}\| \cdot \min)$ | $\mathcal{O}(\|X\| \cdot \|\mathcal{F}\|)$ | $\mathcal{O}(\|X\|)$ | $H(d)$-aproximação harmônica |
| **Simulated Annealing** | Metaheurística Estocástica | $\mathcal{O}(N \cdot m)$ | $\mathcal{O}(N \cdot m)$ | $\mathcal{O}(m)$ | $N$ iterações, $m$ graus de liberdade rotacionais |

---

## 📈 A Parede Exponencial: Teoria vs Resultados Empíricos

### 1. Projeção Teórica (Processador a 1 GHz = $10^9$ operações por segundo)

| $n$ | Força Bruta TSP: $(n-1)!/2$ | Held-Karp: $n^2 2^n$ | Vertex Cover: $2^n$ |
|:---:|:---:|:---:|:---:|
| **5** | $0{,}01\ \mu\text{s}$ | $0{,}8\ \mu\text{s}$ | $0{,}03\ \mu\text{s}$ |
| **10** | $181{,}4\ \mu\text{s}$ | $102{,}4\ \mu\text{s}$ | $1{,}0\ \mu\text{s}$ |
| **15** | **$43{,}6\ \text{s}$** | $7{,}4\ \text{ms}$ | $32{,}8\ \mu\text{s}$ |
| **20** | **$1{,}9\ \text{anos}$** | $419{,}4\ \text{ms}$ | $1{,}0\ \text{ms}$ |
| **25** | **$9{,}8\ \text{milhões de anos}$** | **$21{,}0\ \text{s}$** | $33{,}6\ \text{ms}$ |
| **50** | $9{,}6 \times 10^{36}\ \text{bilhões de anos}$ | **$89{,}3\ \text{anos}$** | **$13{,}0\ \text{dias}$** |
| **100** | $\gg 10^{130}\ \text{bilhões de anos}$ | $4{,}0 \times 10^8\ \text{bilhões de anos}$ | $4{,}0 \times 10^4\ \text{bilhões de anos}$ |

*(Idade estimada do Universo observável: $\approx 13{,}8$ bilhões de anos).*

### 2. Resultados Reais Medidos no Projeto
* **TSP ($n = 10$ cidades):** Held-Karp resolve em **$5{,}41\ \text{ms}$**, enquanto a Força Bruta leva **$886{,}89\ \text{ms}$** (**Held-Karp é 163× mais rápido**).
* **TSP ($n = 11$ cidades):** Força Bruta congela o terminal (> 10 s); Held-Karp resolve em **$9{,}18\ \text{ms}$**.
* **Verificadores Polinomiais:** A rota ótima de 12 cidades foi verificada com sucesso em apenas **$26{,}3\ \mu\text{s}$**.
* **Razões de Aproximação Empíricas:**
  * *Vertex Cover:* Razão média entre **1,42 e 1,70** (sempre abaixo do teto teórico 2,0).
  * *TSP Euclidiano:* Razão média entre **1,08 e 1,20** (custo real apenas 8% a 20% acima do ótimo).
  * *Set Cover:* Razão média entre **1,00 e 1,06** (quase idêntico à solução ótima, bem abaixo do teto $H(d) \approx 2{,}75$).

---

## 🗂️ Estrutura de Arquivos

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml                      # Workflow de Integração Contínua (CI)
├── src/
│   ├── exact/
│   │   ├── vertex_cover.py                # Vertex Cover: Força Bruta e Branch-and-Bound
│   │   └── tsp.py                         # TSP: Força Bruta e Programação Dinâmica de Held-Karp
│   ├── approximation/
│   │   ├── vertex_cover.py                # APPROX-VERTEX-COVER (2-aproximação polinomial)
│   │   ├── tsp.py                         # APPROX-TSP-TOUR (2-aproximação métrica via Prim)
│   │   └── set_cover.py                   # GREEDY-SET-COVER (H(d)-aproximação harmônica)
│   ├── metaheuristics/
│   │   └── simulated_annealing.py         # Simulated Annealing aplicado ao Molecular Docking
│   ├── verification/
│   │   └── verifier.py                    # Verificadores de Certificado Polinomial (O(|V|+|E|) e O(n))
│   └── generators/
│       └── instances.py                   # Geradores com semente determinística (reprodutibilidade)
├── tests/
│   ├── test_generators.py                 # Testes de reprodutibilidade e desigualdade triangular
│   ├── test_vertex_cover.py               # Testes de Vertex Cover em grafos clássicos
│   ├── test_tsp.py                        # Testes de equivalência Força Bruta vs Held-Karp
│   ├── test_verifier.py                   # Validação de certificados válidos e inválidos
│   ├── test_approx_vertex_cover.py        # Validação do fator 2 de aproximação
│   ├── test_approx_tsp.py                 # Validação de Prim, pré-ordem e fator 2 em TSP
│   ├── test_greedy_set_cover.py           # Validação da cobertura completa e fator H(d)
│   └── test_simulated_annealing.py        # Testes de conformações moleculares e convergência
├── benchmarks/
│   ├── benchmark_exact.py                 # Medição progressiva dos algoritmos exatos
│   ├── demo_combinatorial_explosion.py   # Script de demonstração ao vivo para o seminário
│   ├── benchmark_approximation.py         # Avaliação de razão empírica vs fator teórico
│   ├── benchmark_simulated_annealing.py   # Desempenho e curvas de energia do Annealing
│   ├── tune_simulated_annealing.py        # Ajuste sistemático de hiperparâmetros
│   ├── analyze_simulated_annealing_tuning.py # Análise estatística dos experimentos
│   ├── results/                           # Dados brutos em formato CSV
│   └── plots/                             # Gráficos em alta resolução
├── slides/
│   ├── slides_algoritmos_exatos.md       # Slides Marp: Algoritmos Exatos e Intratabilidade
│   ├── roteiro_apresentacao_kairo.md      # Roteiro de fala cronometrado: Algoritmos Exatos
│   ├── slides_aproximacoes.md             # Slides Marp: Algoritmos de Aproximação
│   └── roteiro_apresentacao_heitor.md     # Roteiro de fala cronometrado: Aproximações
├── relatorio/
│   ├── main.tex                           # Artigo científico em LaTeX no padrão IEEEtran
│   ├── referencias.bib                    # Base bibliográfica BibTeX
│   └── main.pdf                           # PDF compilado do relatório
├── docs/
│   ├── pratica.pdf                        # Enunciado do trabalho prático
│   ├── estudo_de_caso_docking.md          # Modelagem detalhada do Molecular Docking
│   └── ajuste_parametros_simulated_annealing.md # Protocolo de ajuste do Annealing
├── pyproject.toml                         # Configurações de ferramentas Python (pytest)
├── requirements.txt                       # Dependências do projeto
└── README.md
```

---

## 💻 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos.git
cd Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos
```

### 2. Configurar o Ambiente Virtual
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

---

## 🧪 Testes Automatizados (101 Testes)

A integridade do código e a correção matemática dos algoritmos são validadas por **101 testes unitários**:

```bash
pytest -v
```

---

## 🚀 Execução dos Experimentos e Demonstrações

### 1. Demonstração Interativa ao Vivo (Seminário)
Demonstração no terminal comparando o tempo real do Held-Karp contra a Força Bruta e executando os verificadores polinomiais:
```bash
python benchmarks/demo_combinatorial_explosion.py
```

### 2. Benchmarks dos Algoritmos Exatos
```bash
python benchmarks/benchmark_exact.py
```
*Gera os gráficos `benchmarks/plots/benchmark_tsp.png` e `benchmarks/plots/benchmark_vertex_cover.png`.*

### 3. Benchmarks dos Algoritmos de Aproximação
```bash
python benchmarks/benchmark_approximation.py
```
*Gera o gráfico comparativo `benchmarks/plots/approximation_ratio.png` e tabelas em `benchmarks/results/`.*

### 4. Benchmarks de Metaheurísticas (Molecular Docking)
```bash
python benchmarks/benchmark_simulated_annealing.py
python benchmarks/tune_simulated_annealing.py
```
*Gera gráficos de convergência de energia e distribuição de tempos em `benchmarks/plots/`.*

---

## 📄 Relatório Técnico (LaTeX IEEEtran)

O relatório técnico-científico está configurado no padrão IEEE (`IEEEtran`), disponível em [`relatorio/`](relatorio/):

```bash
cd relatorio
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 📑 Apresentações (Slides Marp)

Os slides estão em formato Markdown compatível com [Marp](https://marp.app/):

```bash
npx @marp-team/marp-cli slides/slides_algoritmos_exatos.md --pdf
npx @marp-team/marp-cli slides/slides_aproximacoes.md --pdf
```
