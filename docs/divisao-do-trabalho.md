# Divisão do Trabalho — Tema 6: Problemas NP-Completos e Aproximações

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
- Montar o template LaTeX do relatório (estrutura monografia, `algorithm2e`, bibliografia BibTeX).
- **Cap. 1 — Introdução** (técnica de funil, objetivos, roteiro de leitura).
- **Cap. 2 — Fundamentação Teórica:** classes P/NP/NPC, discussão breve de P ≠ NP, reduções polinomiais com demonstrações, explosão combinatória.
- **Cap. 6 — Conclusões e Referências.**

### Pessoa 2 — Relatório (engenharia e custos)
- **Cap. 3 — Paradigma Algorítmico:** pseudocódigos em `algorithm2e` e diagramas/fluxogramas passo a passo (árvore de busca exata, MST → tour pré-ordem, escolha de arestas no Vertex Cover).
- **Cap. 4 — Análise Assintótica Rigorosa:** O, Ω e Θ de tempo e memória para exatos vs. aproximados, e prova dos fatores de aproximação.
- **Apêndice — Cheat Sheet** (1–2 páginas): definição em uma frase, diagrama "Quando usar?", tabela de complexidades, esqueleto de pseudocódigo.
- Revisão final de formatação e consistência do relatório.

### Pessoa 3 — Implementação: algoritmos exatos e infraestrutura
- Estrutura do repositório (pastas `src/`, `tests/`, `benchmarks/`, README com instruções de execução).
- Implementar soluções exatas: força bruta / backtracking para Vertex Cover e TSP (Held-Karp opcional).
- Verificador polinomial (certificado) para demonstrar "NP = verificável em tempo polinomial".
- Testes unitários dos algoritmos exatos.

### Pessoa 4 — Implementação: algoritmos de aproximação
- Implementar APPROX-VERTEX-COVER, APPROX-TSP-TOUR (MST) e GREEDY-SET-COVER.
- Comparar solução aproximada vs. ótima (razão de aproximação empírica).
- Testes unitários dos algoritmos de aproximação.

### Pessoa 5 — Metaheurísticas, estudo de caso e experimentos
- Implementar metaheurística (Simulated Annealing ou Algoritmo Genético).
- Estudo de caso: triagem virtual de fármacos / docking simplificado modelado como problema de otimização.
- Scripts de benchmark com entradas progressivas, geração de gráficos de tempo e qualidade.
- Escrever o material do **Cap. 5 — Estudo de Caso e Implementação Prática** (experimentos, gráficos, gargalos de hardware e de linguagem) e entregar à Pessoa 2 para integração.

### Todos — Seminário (40 min)
- Problema motivador sugerido: *"Por que nenhum computador do mundo encontra a rota ótima de entrega para 100 cidades?"*
- Cada pessoa apresenta a parte que produziu (~8 min cada).
- Todos devem dominar o relatório, o código e a discussão P ≠ NP (exigência da avaliação).
