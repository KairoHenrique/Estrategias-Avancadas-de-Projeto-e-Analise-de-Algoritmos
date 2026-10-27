# Estudo de Caso: Otimização de uma Pose em um Modelo Inspirado em Docking Molecular

## 1. Introdução

O docking molecular é um problema computacional relacionado à investigação de possíveis configurações espaciais de uma molécula em relação a um alvo molecular. A busca por configurações favoráveis envolve a exploração de diferentes posições e orientações, considerando critérios que representam a qualidade de cada configuração.

Neste projeto, esse contexto é utilizado como inspiração para construir um problema artificial de otimização contínua. O objetivo é investigar e comparar o comportamento de duas estratégias de busca: **Simulated Annealing**, uma metaheurística probabilística, e **Random Search**, uma estratégia de busca aleatória utilizada como referência experimental.

O problema foi simplificado para permitir o estudo dos algoritmos em um ambiente controlado, com função objetivo, variáveis de decisão, restrições e parâmetros definidos explicitamente.

> **Limitação importante:** este modelo é exclusivamente educacional. Ele não realiza docking molecular real, não calcula afinidade molecular de maneira físico-química e não deve ser utilizado para avaliar ou selecionar medicamentos.

## 2. Definição do problema de otimização

O problema consiste em encontrar uma configuração espacial do ligante que minimize uma função de energia artificial. Essa função considera a atração dos pontos que representam o ligante em relação aos alvos, a proximidade de obstáculos e a ultrapassagem de limites espaciais.

Formalmente, o problema pode ser representado por:

$$
\min_{P} E(P)
$$

Em que:

- $P$ representa a pose candidata;
- $E(P)$ representa a energia artificial associada à pose;
- o objetivo é encontrar uma pose de menor energia dentro do espaço de busca definido.

A qualidade de uma solução é determinada exclusivamente pela função objetivo implementada no modelo. Portanto, uma energia menor indica uma solução melhor segundo os critérios artificiais adotados, não necessariamente uma configuração molecular biologicamente favorável.

### 2.1. Variáveis de decisão

Cada solução, denominada *pose*, é representada por três variáveis contínuas:

$$
P = (x, y, \theta)
$$

Em que:

- $x$: coordenada horizontal da posição do ligante;
- $y$: coordenada vertical da posição do ligante;
- $\theta$: ângulo de rotação do ligante, expresso em radianos.

As variáveis $x$ e $y$ determinam a translação do ligante no plano, enquanto $\theta$ determina sua orientação.

A região de busca é definida pelas restrições:

$$
-4 \leq x \leq 4
$$

$$
-4 \leq y \leq 4
$$

$$
-\pi \leq \theta < \pi
$$

Assim, cada solução corresponde a um ponto em um espaço de busca contínuo com três dimensões.

### 2.2. Representação geométrica do ligante

O ligante é representado por quatro pontos bidimensionais:

$$
L = \{(0,0), (0.8,0), (0,0.8), (0.8,0.8)\}
$$

Esses pontos funcionam como uma representação geométrica simplificada da estrutura do ligante.

Para avaliar uma pose, cada ponto é rotacionado pelo ângulo $\theta$ e transladado pelas coordenadas $x$ e $y$.

Para um ponto original $(a_i,b_i)$, suas coordenadas transformadas são:

$$
x_i' = x + a_i\cos(\theta) - b_i\sin(\theta)
$$

$$
y_i' = y + a_i\sin(\theta) + b_i\cos(\theta)
$$

Essa transformação permite calcular a posição de cada ponto do ligante para qualquer pose candidata.

## 3. Construção das instâncias

Cada instância do problema contém três componentes:

- **Ligante:** conjunto fixo de quatro pontos bidimensionais.
- **Alvos:** pontos que contribuem negativamente para a energia quando estão próximos dos pontos transformados do ligante.
- **Obstáculos:** pontos que geram penalidades quando estão próximos demais do ligante.

A quantidade de alvos e obstáculos é controlada pelo parâmetro de complexidade $C$:

$$
N_{\text{alvos}} = C
$$

$$
N_{\text{obstáculos}} = 2C
$$

As coordenadas dos alvos são geradas aleatoriamente no intervalo $[-2,2]$, enquanto as coordenadas dos obstáculos são geradas no intervalo $[-4,4]$.

A geração utiliza números pseudoaleatórios com uma semente explícita. Dessa forma, uma mesma combinação de complexidade e semente permite reproduzir a mesma instância.

O aumento de $C$ eleva a quantidade de elementos considerados no cálculo da energia, permitindo investigar como o custo de avaliação cresce conforme a instância se torna maior.

## 4. Função objetivo

A função objetivo é implementada pelo método `DockingProblem.energy()`.

A energia total é composta por três parcelas:

$$
E(P) =
E_{\text{atração}}(P)
+
E_{\text{repulsão}}(P)
+
E_{\text{limite}}(P)
$$

Cada parcela representa um aspecto diferente da avaliação da pose.

### 4.1. Componente de atração

Para cada ponto transformado do ligante, calcula-se a distância euclidiana até o alvo mais próximo.

Sejam $(x_i',y_i')$ as coordenadas transformadas do ponto $i$ e $(t_j^x,t_j^y)$ as coordenadas do alvo $j$. A distância até o alvo mais próximo é:

$$
d_i =
\min_j
\sqrt{
(x_i' - t_j^x)^2 +
(y_i' - t_j^y)^2
}
$$

A contribuição de atração desse ponto é:

$$
E_{\text{atração},i}
=
-\exp\left(
-\frac{d_i^2}{2\sigma^2}
\right)
$$

Em que:

- $d_i$ é a distância até o alvo mais próximo;
- $\sigma$ controla a escala espacial da atração.

A contribuição é negativa e se aproxima de $-1$ quando a distância até o alvo mais próximo se aproxima de zero. Conforme a distância aumenta, essa contribuição se aproxima de zero.

Considerando todos os pontos do ligante:

$$
E_{\text{atração}}(P)
=
\sum_i E_{\text{atração},i}
$$

Portanto, essa parcela favorece poses nas quais os pontos do ligante estão próximos dos alvos.

### 4.2. Componente de repulsão

A segunda parcela penaliza a proximidade excessiva entre os pontos do ligante e os obstáculos.

Para cada par formado por um ponto transformado do ligante e um obstáculo, calcula-se a distância $d_{ij}$.

A penalidade é definida por:

$$
E_{\text{repulsão},ij}
=
k\left(\max(0,r-d_{ij})\right)^2
$$

Em que:

- $d_{ij}$ é a distância entre o ponto $i$ do ligante e o obstáculo $j$;
- $r$ é a distância de repulsão;
- $k$ é a intensidade da penalidade.

Quando $d_{ij} \geq r$, não há penalidade para esse par. Quando $d_{ij} < r$, a contribuição cresce quadraticamente conforme a distância diminui.

A energia de repulsão total é:

$$
E_{\text{repulsão}}(P)
=
\sum_i\sum_j
k\left(\max(0,r-d_{ij})\right)^2
$$

Essa parcela procura evitar configurações que aproximem excessivamente o ligante dos obstáculos definidos artificialmente.

### 4.3. Penalidade por ultrapassagem dos limites

A terceira parcela penaliza pontos do ligante que ultrapassam os limites espaciais estabelecidos pelo parâmetro `boundary`.

Para uma coordenada $z$, a penalidade é:

$$
E_{\text{limite}}(z)
=
\left(\max(0,|z|-b)\right)^2
$$

Em que $b$ representa o limite espacial.

A contribuição é zero quando a coordenada está dentro do intervalo permitido. Quando o ponto ultrapassa o limite, a penalidade cresce quadraticamente com a magnitude da ultrapassagem.

A energia total dessa parcela considera as coordenadas dos pontos transformados do ligante, tanto na direção horizontal quanto na vertical.

### 4.4. Interpretação da energia total

A energia de uma pose resulta da soma das contribuições de atração, repulsão e penalidade por ultrapassagem dos limites.

As três parcelas atuam de maneira complementar:

- A atração favorece a proximidade dos alvos.
- A repulsão desfavorece a proximidade excessiva dos obstáculos.
- A penalidade espacial desfavorece configurações que ultrapassem os limites definidos.

O problema consiste em encontrar:

$$
P^* = \arg\min_{P} E(P)
$$

A função não exige que a solução pertença a um conjunto discreto de configurações. Como as variáveis de decisão são contínuas, o algoritmo explora diferentes posições e orientações dentro do domínio estabelecido.

## 5. Restrições e parâmetros do modelo

Os principais parâmetros utilizados na implementação são apresentados a seguir.

| Elemento | Parâmetro | Valor padrão |
|---|---|---:|
| Limite inferior das coordenadas de busca | `SEARCH_MIN` | -4,0 |
| Limite superior das coordenadas de busca | `SEARCH_MAX` | 4,0 |
| Temperatura inicial | `initial_temperature` | 2,0 |
| Temperatura final | `final_temperature` | 0,01 |
| Desvio-padrão das perturbações de posição | — | 0,6 |
| Desvio-padrão da perturbação angular | — | 0,25 |
| Escala espacial da atração | `attraction_sigma` | 1,2 |
| Distância de repulsão | `repulsion_distance` | 0,9 |
| Intensidade da repulsão | `repulsion_strength` | 8,0 |
| Limite espacial da função de energia | `boundary` | 5,0 |

Os parâmetros da função de energia definem como uma pose é avaliada. Já os parâmetros do Simulated Annealing controlam a geração e a aceitação de soluções candidatas.

É importante distinguir os limites de busca dos limites da função de energia. As coordenadas do centro do ligante são mantidas no intervalo de busca, mas seus pontos transformados podem ultrapassar o limite espacial de avaliação. Nesse caso, a função de energia aplica a penalidade correspondente.

O limite angular também é respeitado durante a geração das poses, mantendo a rotação no intervalo $[-\pi,\pi)$.

## 6. Metaheurística: Simulated Annealing

O Simulated Annealing é uma metaheurística probabilística inspirada no processo de recozimento utilizado em materiais. No contexto deste projeto, seu propósito é explorar o espaço contínuo de poses e procurar configurações com menor energia.

### 6.1. Inicialização

O algoritmo gera uma pose inicial aleatória dentro do espaço de busca e calcula sua energia.

Essa pose passa a ser a solução atual e, inicialmente, também a melhor solução encontrada.

### 6.2. Geração de vizinhos

Em cada iteração, uma nova pose candidata é produzida por perturbações aleatórias nas coordenadas de posição e no ângulo.

As coordenadas $x$ e $y$ recebem perturbações gaussianas com desvio-padrão de $0.6$. O ângulo recebe uma perturbação gaussiana com desvio-padrão de $0.25$ radiano.

As coordenadas de posição são limitadas ao intervalo de busca, enquanto o ângulo é ajustado para permanecer em $[-\pi,\pi)$.

A energia da pose candidata é então calculada.

### 6.3. Critério de aceitação

Se a nova pose apresenta energia menor ou igual à energia da pose atual, ela é aceita.

Se apresenta energia maior, ainda pode ser aceita com uma probabilidade determinada pela expressão:

$$
p = \exp\left(-\frac{\Delta E}{T}\right)
$$

Em que:

$$
\Delta E = E_{\text{candidata}} - E_{\text{atual}}
$$

e $T$ representa a temperatura atual.

Essa regra permite que o algoritmo aceite ocasionalmente soluções piores, evitando que a busca fique limitada exclusivamente a melhorias imediatas.

Quando a temperatura diminui, a probabilidade de aceitar soluções piores também diminui para uma mesma diferença positiva de energia.

### 6.4. Resfriamento

A temperatura diminui geometricamente ao longo das iterações, segundo a expressão:

$$
T_k =
T_0
\left(\frac{T_f}{T_0}\right)^{\frac{k}{I-1}}
$$

para $I>1$, em que:

- $T_0$ é a temperatura inicial;
- $T_f$ é a temperatura final;
- $I$ é a quantidade de iterações;
- $k$ é o índice da iteração, começando em zero.

Quando há apenas uma iteração, a implementação utiliza a temperatura inicial.

O resfriamento controla a transição entre uma exploração mais permissiva e uma busca progressivamente menos propensa a aceitar soluções piores.

### 6.5. Registro da melhor solução

Durante a execução, o algoritmo mantém o registro da melhor pose encontrada. Ao final, retorna essa pose, sua energia, a quantidade de avaliações realizadas e o tempo de execução.

Na implementação, uma execução com $I$ iterações realiza $I+1$ avaliações: uma avaliação inicial e uma avaliação por iteração.

Esse detalhe é importante para comparar o Simulated Annealing com o Random Search sob orçamentos equivalentes de avaliações da função objetivo.

## 7. Algoritmo de referência: Random Search

O Random Search é utilizado como referência para avaliar o comportamento do Simulated Annealing.

Em cada avaliação, o algoritmo gera uma pose aleatória dentro do mesmo domínio de busca e calcula sua energia. A melhor solução encontrada é mantida até o término da execução.

Diferentemente do Simulated Annealing, o Random Search não utiliza uma solução atual, não gera vizinhos a partir da pose anterior e não possui um mecanismo de aceitação probabilística ou de resfriamento.

A comparação entre os métodos permite investigar se a exploração guiada por vizinhança e pelo critério de aceitação do Simulated Annealing oferece vantagens em relação à amostragem aleatória, considerando o orçamento de avaliações adotado.

Para tornar a comparação consistente, os algoritmos são executados sobre a mesma instância e com a mesma quantidade total de avaliações da função objetivo. As sementes utilizadas são definidas explicitamente.

### 8.1. Relação com a intratabilidade computacional

O docking molecular é um problema de otimização computacionalmente desafiador, principalmente quando são consideradas a flexibilidade do ligante, a flexibilidade do receptor e a necessidade de avaliar um grande número de configurações espaciais. Os algoritmos de docking utilizam estratégias de busca e funções de pontuação para explorar e classificar possíveis poses moleculares (PAGADALA; SYED; TUSZYNSKI, 2017).

Em sistemas moleculares reais, encontrar uma pose favorável pode exigir a exploração de diferentes posições, orientações e conformações internas do ligante. A consideração da flexibilidade molecular amplia o espaço de busca, enquanto as funções de pontuação apresentam desafios para distinguir corretamente as configurações candidatas. Esses aspectos são discutidos em avaliações de algoritmos de docking com ligantes flexíveis (HUANG, 2018).

Essas dificuldades são especialmente relevantes em processos de triagem virtual de fármacos, nos quais um grande número de compostos precisa ser avaliado. Explorar todas as configurações possíveis pode exigir um custo computacional elevado. Por isso, métodos de busca aproximada e metaheurísticas podem ser utilizados para explorar o espaço de soluções sem exigir a enumeração de todas as possibilidades.

A análise da complexidade computacional permite estudar como os recursos necessários à execução de um algoritmo variam em função do tamanho da entrada. Essa análise ajuda a compreender os limites de eficiência dos algoritmos e a distinguir o custo de uma implementação específica da classificação teórica de um problema computacional (CORMEN et al., 2012).

Neste projeto, o Simulated Annealing é empregado como uma estratégia de busca probabilística. O algoritmo gera soluções candidatas, avalia suas energias e utiliza um critério de aceitação que permite, em determinadas condições, aceitar soluções piores que a atual. Esse mecanismo busca favorecer a exploração do espaço de soluções e reduzir a dependência de melhorias imediatas. Entretanto, o método não garante encontrar a solução global ótima em todas as execuções.

É importante distinguir a dificuldade computacional do docking molecular real da complexidade da representação simplificada implementada neste trabalho.

No modelo proposto, a pose é representada por três variáveis contínuas: duas coordenadas de posição e um ângulo de rotação. O ligante possui quatro pontos fixos, e a função de energia considera a atração em relação aos alvos, a repulsão dos obstáculos e a penalização por ultrapassagem dos limites espaciais.

Como o número de pontos do ligante é constante, o custo de uma avaliação da função de energia cresce linearmente com o parâmetro de complexidade da instância, resultando em um custo de busca de ordem \(O(AC)\), em que \(A\) representa o número de avaliações e \(C\) representa o parâmetro de complexidade definido neste estudo.

Essa expressão descreve o custo computacional da implementação analisada. Ela não demonstra que o modelo simplificado seja NP-difícil, nem permite concluir que sua resolução exija necessariamente uma quantidade exponencial de tempo.

Portanto, a relação com a intratabilidade está no contexto mais amplo do docking molecular e nas dificuldades associadas à exploração de espaços de busca complexos. O modelo implementado permite investigar experimentalmente o comportamento de uma metaheurística em um problema controlado, mas não constitui uma demonstração teórica da intratabilidade do docking molecular ou de sua própria formulação.

## 9. Metodologia experimental

Os experimentos foram organizados para comparar a qualidade das soluções e o custo computacional dos algoritmos sob diferentes condições.

### 9.1. Configurações avaliadas

Foram utilizados cinco níveis de complexidade:

$$
C = \{2,4,6,8,10\}
$$

Para cada nível, foram avaliados cinco orçamentos de avaliações:

$$
B = \{100,1000,10000,100000,1000000\}
$$

Cada combinação de complexidade e orçamento foi executada 30 vezes.

O número total de comparações pareadas é:

$$
5 \times 5 \times 30 = 750
$$

Portanto, foram realizadas 750 execuções do Simulated Annealing e 750 execuções do Random Search, totalizando 1.500 execuções dos algoritmos.

### 9.2. Reprodutibilidade

As instâncias e as execuções utilizam sementes explícitas, definidas de maneira determinística a partir da complexidade e do número da repetição.

Cada par de execuções utiliza a mesma instância e o mesmo orçamento de avaliações, permitindo comparar os resultados obtidos nas mesmas condições experimentais.

A reprodutibilidade permite repetir os experimentos e verificar os resultados, desde que sejam mantidas as mesmas condições relevantes, incluindo implementação, parâmetros, sementes e ambiente computacional.

### 9.3. Métricas de avaliação

Os resultados são analisados por meio das seguintes métricas:

- **Energia média:** representa a qualidade média das soluções encontradas.
- **Desvio-padrão da energia:** indica a variabilidade dos resultados entre as repetições.
- **Tempo médio de execução:** permite comparar o custo computacional observado.
- **Desvio-padrão do tempo:** indica a variabilidade dos tempos medidos.
- **Diferença pareada de energia:** compara diretamente os dois algoritmos em cada repetição.
- **Intervalo de confiança bootstrap de 95%:** estima a incerteza da média das diferenças pareadas.
- **Teste exato dos sinais:** avalia se a frequência de vitórias de um algoritmo difere da esperada sob a hipótese nula de probabilidades iguais, desconsiderando empates.

A diferença pareada é definida por:

$$
D = E_{\text{SA}} - E_{\text{Random}}
$$

Sua interpretação é:

- $D<0$: o Simulated Annealing encontrou menor energia;
- $D>0$: o Random Search encontrou menor energia;
- $D=0$: os algoritmos encontraram energias iguais.

Como o objetivo é minimizar a energia, valores negativos favorecem o Simulated Annealing, enquanto valores positivos favorecem o Random Search.

O intervalo de confiança bootstrap é calculado a partir de reamostragens com reposição das diferenças observadas. O teste exato dos sinais utiliza a quantidade de vitórias e derrotas, desconsiderando empates.

Essas análises permitem observar tanto a magnitude das diferenças quanto a consistência das vitórias entre as repetições. Os resultados devem ser interpretados em conjunto, sem concluir que um algoritmo é universalmente superior com base em uma única métrica.

### 9.4. Artefatos experimentais

Os resultados dos experimentos são armazenados em arquivos CSV, permitindo consultar os valores obtidos e realizar análises posteriores.

Os gráficos de energia permitem comparar a qualidade média das soluções conforme o orçamento de avaliações aumenta. Os gráficos de tempo de execução permitem observar como o custo computacional varia entre os algoritmos e os níveis de complexidade.

Os arquivos gerados pelo experimento devem ser interpretados em conjunto com os parâmetros utilizados e com a metodologia descrita nesta documentação.

### 9.5. Análise de custos computacionais e gargalos de execução

O custo computacional dos experimentos depende tanto das características da implementação quanto dos recursos disponíveis no ambiente de execução. Neste projeto, os principais fatores considerados são a quantidade de avaliações da função objetivo, a complexidade das instâncias e o número de repetições realizadas para cada configuração experimental.

A função de energia calcula as distâncias entre os pontos transformados do ligante e os alvos e obstáculos. Como o ligante possui quatro pontos fixos, o aumento da quantidade de alvos e obstáculos eleva o custo de cada avaliação. Consequentemente, execuções com orçamentos maiores e instâncias mais complexas tendem a exigir mais tempo de processamento.

O Simulated Annealing e o Random Search realizam avaliações repetidas da função objetivo. Por isso, o orçamento de avaliações constitui um fator importante para o custo total dos experimentos. A realização de várias repetições também aumenta o trabalho computacional, embora seja necessária para observar a variabilidade dos resultados e comparar os algoritmos com maior consistência.

Em relação ao hardware, a velocidade do processador influencia o tempo necessário para executar as operações da função objetivo e as iterações dos algoritmos. A disponibilidade de memória também pode ser relevante quando são armazenados resultados de muitas execuções ou processados conjuntos maiores de dados. Entretanto, os experimentos apresentados não incluem medições específicas de utilização da CPU ou do consumo de memória. Portanto, esses aspectos são considerados possíveis fatores de influência, e não gargalos de hardware comprovadamente identificados.

A implementação utiliza Python, linguagem que oferece recursos para desenvolver algoritmos e organizar experimentos de maneira clara. Entretanto, operações executadas repetidamente em código Python podem representar um custo de desempenho, especialmente quando envolvem cálculos numéricos em grande quantidade. Neste projeto, o cálculo das distâncias e das contribuições da função de energia é uma parte relevante do trabalho realizado em cada avaliação.

Uma possível otimização seria reduzir operações redundantes, utilizar estruturas de dados adequadas ou empregar bibliotecas numéricas especializadas. Contudo, qualquer alteração desse tipo deve preservar o comportamento da função objetivo e ser acompanhada de testes para garantir a equivalência dos resultados. Não foi realizada uma comparação experimental entre linguagens de programação, de modo que não é possível quantificar uma eventual vantagem de desempenho de outra linguagem neste estudo.

Assim, a análise dos custos deve considerar conjuntamente o tamanho das instâncias, o orçamento de avaliações, o número de repetições, a implementação da função de energia e os recursos do ambiente de execução. Essas considerações ajudam a interpretar os tempos medidos sem atribuir diferenças observadas a causas que não foram avaliadas diretamente.

## 10. Limitações do estudo

A interpretação dos resultados deve considerar as limitações do modelo:

1. **Representação geométrica simplificada:** o ligante é representado por apenas quatro pontos bidimensionais.
2. **Função de energia artificial:** as contribuições de atração, repulsão e penalização não correspondem a um modelo físico-químico validado.
3. **Ausência de flexibilidade molecular completa:** o modelo considera apenas translação e rotação, sem representar mudanças internas na estrutura do ligante.
4. **Alvos e obstáculos artificiais:** suas posições são geradas aleatoriamente e não representam estruturas moleculares reais.
5. **Ausência de validação experimental:** os resultados não são comparados com dados reais de docking ou de atividade farmacológica.
6. **Dependência das condições experimentais:** o desempenho observado depende da função objetivo, dos parâmetros, das instâncias, das sementes e dos orçamentos de avaliação utilizados.

Essas limitações impedem que os resultados sejam extrapolados diretamente para aplicações farmacêuticas reais.

## 11. Conclusão

Este estudo implementa um problema artificial de minimização inspirado no docking molecular para investigar o comportamento do Simulated Annealing em comparação com o Random Search.

A representação contínua das poses, a função de energia composta por três parcelas e o controle dos orçamentos de avaliação permitem realizar experimentos reproduzíveis em diferentes níveis de complexidade.

A análise conjunta da energia, do tempo de execução e das métricas estatísticas permite investigar as vantagens e limitações de cada estratégia dentro das condições avaliadas.

A comparação não pressupõe superioridade universal de uma das abordagens. As conclusões devem ser fundamentadas nos resultados experimentais, considerando tanto a qualidade das soluções quanto o custo computacional.

Por fim, o projeto demonstra como uma metaheurística pode ser aplicada a um problema de otimização contínua e como uma metodologia experimental estruturada pode apoiar a análise comparativa de algoritmos.

## 12. Referências

HUANG, Sheng-You. Comprehensive assessment of flexible-ligand docking algorithms: current effectiveness and challenges. *Briefings in Bioinformatics*, v. 19, n. 5, p. 982–994, 2018. DOI: https://doi.org/10.1093/bib/bbx030.

PAGADALA, Nataraj S.; SYED, Khajamohiddin; TUSZYNSKI, Jack. Software for molecular docking: a review. *Biophysical Reviews*, v. 9, n. 2, p. 91–102, 2017. DOI: https://doi.org/10.1007/s12551-016-0247-1.

CORMEN, Thomas H.; LEISERSON, Charles E.; RIVEST, Ronald L.; STEIN, Clifford. *Algoritmos: teoria e prática*. 3. ed. Rio de Janeiro: Elsevier, 2012.