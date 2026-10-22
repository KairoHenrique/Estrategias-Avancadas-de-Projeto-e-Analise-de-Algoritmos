---
marp: true
theme: default
paginate: true
header: "Estratégias Avançadas de Projeto e Análise de Algoritmos — CEFET-MG"
footer: "Tema 6: NP-Completude e Aproximações | Pessoa 3: Kairo Henrique"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 24px;
    padding: 40px;
  }
  h1 {
    color: #1a365d;
    font-size: 38px;
  }
  h2 {
    color: #2b6cb0;
    font-size: 30px;
  }
  code {
    background-color: #edf2f7;
    color: #c53030;
  }
  table {
    font-size: 19px;
  }
---

# Tema 6: Problemas NP-Completos e Aproximações
## Parte 3: Algoritmos Exatos, Fronteira da Computabilidade e Verificação Polinomial

**Integrante:** Kairo Henrique (Pessoa 3)  
**Disciplina:** Estratégias Avançadas de Projeto e Análise de Algoritmos  
**Professor:** Michel Pires da Silva — DECOM / CEFET-MG  
**Livro-Base:** Cormen et al., *Algoritmos: Teoria e Prática* (Cap. 34 e 35)

---

# 1. O Problema Motivador

> *"Por que nenhum supercomputador do mundo consegue encontrar a rota ótima de entrega para 100 cidades?"*

- **O Problema do Caixeiro-Viajante (TSP):**
  - Número de rotas possíveis: $\frac{(n-1)!}{2}$.
  - Para $n = 100$ cidades:
    $$\frac{99!}{2} \approx 4.66 \times 10^{155} \text{ rotas alternativas.}$$
  - No universo observável existem aproximadamente $10^{80}$ átomos.
  - Se cada átomo do universo fosse um supercomputador calculando $10^{12}$ rotas por segundo desde o Big Bang ($13.8 \times 10^9$ anos), teríamos verificado apenas uma fração desprezível de $10^{110}$ rotas!

---

# 2. A Fronteira da Computabilidade: P vs NP

- **Classe P (Polinomial):**
  - Problemas tratáveis e eficientes. Existe algoritmo determinístico que resolve em tempo $O(n^c)$ (ex: Caminho Mínimo de Dijkstra, Ordenação).
- **Classe NP (Nondeterministic Polynomial):**
  - Problemas onde uma solução proposta (certificado) pode ser **verificada** em tempo polinomial.
- **NP-Completo (NPC):**
  - Os problemas mais difíceis de NP. Se qualquer problema NPC tiver um algoritmo polinomial exato, então **P = NP**.
- **NP-Difícil (NP-Hard):**
  - Tão ou mais difíceis que qualquer problema em NP (não precisam estar em NP).

---

# 3. O Dilema do Milênio: P ≠ NP

- **Por que a comunidade científica acredita que P ≠ NP?**
  1. Mais de 50 anos de buscas intensas pelos matemáticos e cientistas da computação mais brilhantes do planeta sem encontrar algoritmo polinomial para nenhum dos milhares de problemas NPC catalogados.
  2. Barreiras teóricas provadas: Relativização (Baker-Gill-Solovay) e Provas Naturais (Razborov-Rudich).
- **E se P = NP fosse verdadeiro? Consequências drásticas:**
  - **Criptografia moderna colapsada:** Quebra instantânea de RSA, Curvas Elípticas (ECC) e assinaturas digitais — base de toda segurança bancária e da internet.
  - **Otimização universal:** Automação total de logística, alocação de recursos, síntese molecular e descoberta de fármacos.
  - **Matemática automatizada:** Qualquer demonstração matemática verificável seria gerada automaticamente por computador.

---

# 4. A Essência de NP: Verificadores em Tempo Polinomial

O Cormen (Cap. 34) define formalmente:
> *"Um problema pertence a NP se um certificado $c$ pode ser verificado em tempo polinomial $|x|^{O(1)}$."*

### Nossos Verificadores Implementados no Repositório:
1. **Verificador de Vertex Cover ($O(|V| + |E|)$):**
   - Dada instância $(G, k)$ e certificado $C \subseteq V$:
   - Checa se $|C| \le k$ em $O(1)$.
   - Checa se para toda aresta $(u, v) \in E$, $u \in C \lor v \in C$ em $O(|E|)$.
   - Tempo estritamente linear e polinomial!
2. **Verificador de TSP ($O(n)$):**
   - Dada matriz de distâncias $D$, limitante $L$ e rota $P = [v_0, \dots, v_{n-1}]$:
   - Checa se $P$ é permutação válida em $O(n)$.
   - Soma o ciclo $\sum D[P[i]][P[(i+1)\%n]]$ e checa $\le L$ em $O(n)$.

---

# 5. Algoritmos Exatos Implementados

Resolvemos as instâncias buscando a solução exata ótima:

### 1. Vertex Cover Exato:
- **Força Bruta Enumerativa:** Testa combinações de subconjuntos de tamanho $k=0, 1, \dots, n$.
  - Complexidade de Tempo: $O(2^n \cdot |E|)$ | Espaço: $O(n)$.
- **Branch-and-Bound (Backtracking):** Escolhe aresta $(u, v)$ não coberta e ramifica: ou inclui $u$, ou inclui $v$, com poda de ramos não promissores.
  - Complexidade de Tempo: $O(2^k \cdot |E|)$, onde $k \le n$ é a cobertura ótima.

### 2. TSP Exato:
- **Força Bruta Permutacional:** Fixa vértice 0 e permuta $(n-1)!$ caminhos.
  - Complexidade: $\Theta((n-1)! \cdot n)$ tempo | $O(n)$ espaço.
- **Held-Karp (Programação Dinâmica com Bitmask):**
  - Subproblema $C(S, j) = \min_{i \in S \setminus \{j\}} \{ C(S \setminus \{j\}, i) + D[i][j] \}$.
  - Complexidade: $\Theta(n^2 2^n)$ tempo | $\Theta(n 2^n)$ espaço.

---

# 6. A Parede Exponencial: Tabela Teórica

Tempo estimado para um processador de **1 GHz ($10^9$ operações por segundo)**:

| $n$ | Força Bruta TSP: $(n-1)!/2$ | Held-Karp: $n^2 2^n$ | Vertex Cover: $2^n$ |
|:---:|:---:|:---:|:---:|
| **5** | $0.01\ \mu\text{s}$ | $0.8\ \mu\text{s}$ | $0.03\ \mu\text{s}$ |
| **10** | $181.4\ \mu\text{s}$ | $102.4\ \mu\text{s}$ | $1.0\ \mu\text{s}$ |
| **15** | **$43.6\ \text{s}$** | $7.4\ \text{ms}$ | $32.8\ \mu\text{s}$ |
| **20** | **$1.9\ \text{anos}$** | $419.4\ \text{ms}$ | $1.0\ \text{ms}$ |
| **25** | **$9.8\ \text{milhões de anos}$** | **$21.0\ \text{s}$** | $33.6\ \text{ms}$ |
| **50** | $9.6 \times 10^{36}\ \text{bilhões de anos}$ | **$89.3\ \text{anos}$** | **$13.0\ \text{dias}$** |
| **100** | $\gg 10^{130}\ \text{bilhões de anos}$ | $4.0 \times 10^8\ \text{bilhões de anos}$ | $4.0 \times 10^4\ \text{bilhões de anos}$ |

*Idade do Universo observável: $\approx 13.8$ bilhões de anos.*

---

# 7. Resultados Experimentais (Benchmarks Reais)

Medições reais realizadas no hardware da máquina do projeto:

- **Para $n = 10$ cidades:**
  - Held-Karp: **$5.41\ \text{ms}$**
  - Força Bruta: **$886.89\ \text{ms}$** (Held-Karp foi **163x mais rápido**).
- **Para $n = 11$ cidades:**
  - Held-Karp: **$9.18\ \text{ms}$**
  - Força Bruta: **Intratável (> 10 segundos)**.
- **Para $n = 14$ cidades:**
  - Held-Karp: **$235.13\ \text{ms}$**
  - Força Bruta estimada: $\approx 17.5$ horas!
- **A Barreira de Memória:** Para $n > 25$, o consumo de memória do Held-Karp ($\Theta(n 2^n)$) excede dezenas de gigabytes de RAM.

*(Gráficos completos salvos em `benchmarks/plots/`).*

---

# 8. Demonstração ao Vivo no Seminário

Execução interativa ao vivo via terminal:
```bash
python benchmarks/demo_combinatorial_explosion.py
```

### O que o público verá:
1. Impressão da progressão matemática e cálculo de tempo em anos.
2. Execução das instâncias em tempo real no terminal até a força bruta congelar.
3. Execução dos verificadores polinomiais aceitando e rejeitando certificados em microssegundos ($35.5\ \mu\text{s}$).

---

# 9. Conexão com o Mundo Real: Triagem de Fármacos e *Molecular Docking*

O problema da intratabilidade não é abstrato — ele impacta diretamente a medicina e a farmacologia moderna:

- **O Desafio do Molecular Docking:**
  - Descobrir a conformação tridimensional ótima de uma molécula candidata a remédio (ligante) dentro do sítio de ligação de uma proteína receptora.
  - Cada ligação química rotacionável introduz um ângulo contínuo de torção $\theta_i \in [0, 2\pi)$.
- **Explosão Combinatória no Espaço Conformacional:**
  - Se um ligante modesto possui $10$ ligações rotacionáveis e discretizamos os ângulos em passos de $30^\circ$ ($12$ estados por ângulo):
    $$\text{Espaço de Busca} = 12^{10} \approx 6.19 \times 10^{10} \text{ conformações!}$$
- **A Solução:** Métodos exatos são inviáveis. É imprescindível recorrer a **Algoritmos de Aproximação (Cap. 35)** e **Metaheurísticas (Simulated Annealing e Algoritmos Genéticos)** — apresentados a seguir pelos colegas Heitor e Jade!

---

# 10. Conclusão da Parte 3

- **Algoritmos Exatos** garantem otimalidade matemática absoluta, mas batem na barreira da intratabilidade quando $n$ cresce além de pequenos limites ($n \approx 15 \dots 25$).
- **Verificadores Polinomiais** mostram a assimetria fundamental da computação: resolver pode levar eras, mas conferir uma solução leva microssegundos.
- A infraestrutura construída no repositório (`src/`, `tests/`, `benchmarks/`, CI com GitHub Actions) fornece a base exata e os geradores com semente fixa para a validação empírica das aproximações e metaheurísticas.

**Repositório:** [github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos)
