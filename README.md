# Tema 6: Problemas NP-Completos e Aproximações

Trabalho teórico da disciplina (enunciado em [`docs/pratica.pdf`](docs/pratica.pdf)). Entregáveis: relatório técnico-científico, seminário de 40 min e implementação de referência neste repositório.

**Disciplina:** Estratégias Avançadas de Projeto e Análise de Algoritmos — Prof. Michel Pires (CEFET-MG)
**Livro-base:** Cormen et al., *Algoritmos: Teoria e Prática* — Cap. 34 (NP-Completude) e Cap. 35 (Algoritmos de Aproximação)
**Integrantes:** Heitor, Igor, Jade, Maria e Kairo (papéis ainda não atribuídos — usar Pessoa 1 a 5)

## Prazos

| Marco | Data |
|---|---|
| Fundamentação + esqueleto do código prontos | 18/10/2026 |
| Implementação + experimentos concluídos | 25/10/2026 |
| Revisão final do relatório e slides | 30/10/2026 |
| **Submissão no AVA** | **01/11/2026** |
| Seminário (40 min) | 05 e 06/11/2026 |

## Escopo técnico do grupo

- **Classes de complexidade:** P, NP, NP-Difícil, NP-Completo; verificadores polinomiais e certificados.
- **Discussão breve sobre P ≠ NP:** o que significa o problema do milênio, consequências caso P = NP (criptografia, otimização) e por que a comunidade acredita que P ≠ NP.
- **Reduções polinomiais:** SAT → 3-SAT → CLIQUE → VERTEX-COVER (Teorema de Cook-Levin como ponto de partida).
- **Explosão combinatória:** demonstração matemática (ex.: \(2^n\) subconjuntos para Vertex Cover, \((n-1)!/2\) rotas para TSP).
- **Algoritmos de aproximação (Cap. 35):** APPROX-VERTEX-COVER (fator 2), APPROX-TSP-TOUR via MST (fator 2, desigualdade triangular), GREEDY-SET-COVER (fator \(H(n)\)).
- **Heurísticas/metaheurísticas:** Simulated Annealing e/ou Algoritmo Genético aplicados a um estudo de caso real (triagem virtual de fármacos / *molecular docking* simplificado).

## Papéis

### Pessoa 1 — Relatório (parte teórica)
- [#1](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/1) Montar o template LaTeX do relatório (estrutura monografia, `algorithm2e`, bibliografia BibTeX).
- [#2](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/2) **Cap. 1 — Introdução** (técnica de funil, objetivos, roteiro de leitura).
- [#3](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/3) **Cap. 2 — Fundamentação Teórica:** classes P/NP/NPC, discussão breve de P ≠ NP, reduções polinomiais com demonstrações, explosão combinatória.
- [#4](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/4) **Cap. 6 — Conclusões e Referências.**

### Pessoa 2 — Relatório (engenharia e custos)
- [#5](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/5) **Cap. 3 — Paradigma Algorítmico:** pseudocódigos em `algorithm2e` e diagramas/fluxogramas passo a passo (árvore de busca exata, MST → tour pré-ordem, escolha de arestas no Vertex Cover).
- [#6](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/6) **Cap. 4 — Análise Assintótica Rigorosa:** O, Ω e Θ de tempo e memória para exatos vs. aproximados, e prova dos fatores de aproximação.
- [#7](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/7) **Apêndice — Cheat Sheet** (1–2 páginas): definição em uma frase, diagrama "Quando usar?", tabela de complexidades, esqueleto de pseudocódigo.
- [#8](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/8) Integração do Cap. 5 e revisão final de formatação e consistência do relatório.

### Pessoa 3 — Implementação: algoritmos exatos e infraestrutura
- [#9](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/9) Estrutura do repositório (pastas `src/`, `tests/`, `benchmarks/`, README com instruções de execução).
- [#10](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/10) Soluções exatas (força bruta / backtracking para Vertex Cover e TSP, Held-Karp opcional), verificador polinomial de certificado e testes unitários.

### Pessoa 4 — Implementação: algoritmos de aproximação
- [#11](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/11) Implementar APPROX-VERTEX-COVER, APPROX-TSP-TOUR (MST) e GREEDY-SET-COVER, com testes unitários.
- [#12](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/12) Comparar solução aproximada vs. ótima (razão de aproximação empírica).

### Pessoa 5 — Metaheurísticas, estudo de caso e experimentos
- [#13](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/13) Metaheurística (Simulated Annealing ou Algoritmo Genético) aplicada ao estudo de caso de triagem virtual de fármacos / docking simplificado.
- [#14](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/14) Benchmarks com entradas progressivas, gráficos de tempo e qualidade, e material do **Cap. 5 — Estudo de Caso e Implementação Prática** (gargalos de hardware e de linguagem) entregue à Pessoa 2.

### Todos — Seminário (40 min)
- [#15](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues/15) Slides e ensaio da apresentação.
- Problema motivador sugerido: *"Por que nenhum computador do mundo encontra a rota ótima de entrega para 100 cidades?"*
- Cada pessoa apresenta a parte que produziu (~8 min cada).
- Todos devem dominar o relatório, o código e a discussão P ≠ NP (exigência da avaliação).

## Acompanhamento

- Quadro de tarefas: [GitHub Project](https://github.com/users/KairoHenrique/projects/6)
- Todas as tasks: [issues do repositório](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/issues)
- Filtrar por papel: labels `pessoa-1` a `pessoa-5`; por área: `relatorio`, `implementacao`, `seminario`
- Prazo final: milestone [Entrega AVA - 01/11/2026](https://github.com/KairoHenrique/Estrategias-Avancadas-de-Projeto-e-Analise-de-Algoritmos/milestone/1)
