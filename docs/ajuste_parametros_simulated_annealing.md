# Ajuste de parâmetros do Simulated Annealing

## 1. Objetivo

Este experimento tem como objetivo comparar diferentes configurações de temperatura do algoritmo Simulated Annealing aplicado a um modelo simplificado de docking molecular. Busca-se identificar uma configuração adequada considerando a qualidade das soluções encontradas, a variabilidade dos resultados e o custo computacional.

## 2. Metodologia

Foram avaliadas três configurações de temperatura inicial, mantendo constante a temperatura final e os demais parâmetros do algoritmo.

| Configuração | Temperatura inicial | Temperatura final |
|---|---:|---:|
| A — Moderada | 1,0 | 0,01 |
| B — Intermediária | 2,0 | 0,01 |
| C — Exploratória | 5,0 | 0,01 |

Os experimentos consideraram três níveis de complexidade: 2, 6 e 10. Para cada combinação de configuração e complexidade, foram realizadas 30 repetições, com orçamento de 10.000 avaliações da função objetivo por execução.

As configurações foram comparadas utilizando as mesmas instâncias e sementes aleatórias em cada repetição, buscando tornar a comparação mais consistente.

A métrica principal foi a melhor energia encontrada em cada execução. Como o problema é formulado como uma minimização, valores menores de energia representam soluções melhores segundo a função objetivo adotada.

Também foi registrado o tempo de execução para avaliar o custo computacional de cada configuração.

### 2.1 Análise estatística

Além das estatísticas descritivas, foram realizadas comparações pareadas entre as configurações.

Foram calculadas diferenças médias entre os resultados, intervalos de confiança bootstrap de 95% para essas diferenças e valores-p do teste dos sinais.

Para a energia, a diferença foi calculada como:

**Diferença = energia da configuração 1 − energia da configuração 2.**

Consequentemente, uma diferença negativa favorece a configuração 1, pois indica menor energia média. Uma diferença positiva favorece a configuração 2.

Foi adotado um nível de significância de 5% para interpretar os valores-p do teste dos sinais. Os resultados estatísticos foram utilizados para avaliar se as diferenças observadas forneciam evidências suficientes de uma vantagem consistente entre as configurações.

## 3. Resultados

As médias e os desvios padrão observados para a melhor energia foram:

| Complexidade | Configuração | Energia média | Desvio padrão |
|---:|---|---:|---:|
| 2 | A — Moderada | -3,646859 | 0,091056 |
| 2 | B — Intermediária | -3,646633 | 0,091311 |
| 2 | C — Exploratória | -3,646764 | 0,090998 |
| 6 | A — Moderada | -3,735169 | 0,100855 |
| 6 | B — Intermediária | -3,739090 | 0,095846 |
| 6 | C — Exploratória | -3,738709 | 0,097312 |
| 10 | A — Moderada | -3,734216 | 0,189323 |
| 10 | B — Intermediária | -3,731155 | 0,194156 |
| 10 | C — Exploratória | -3,765461 | 0,100953 |

### 3.1 Análise dos resultados

Na complexidade 2, as três configurações apresentaram energias médias muito próximas. A configuração A obteve o menor valor médio, mas a diferença foi pequena.

Na complexidade 6, a configuração B apresentou a menor energia média, seguida de perto pela configuração C. Novamente, as diferenças observadas foram pequenas.

Na complexidade 10, a configuração C obteve o melhor resultado médio, com energia de -3,765461. Além disso, apresentou desvio padrão de 0,100953, inferior aos valores observados nas configurações A e B.

Esses resultados sugerem que a temperatura inicial mais alta pode favorecer a exploração do espaço de busca nos problemas de maior complexidade considerados neste experimento. Entretanto, os resultados descritivos, isoladamente, não demonstram que essa configuração seja superior.

## 4. Comparação estatística

As comparações pareadas foram realizadas considerando 30 repetições por configuração em cada nível de complexidade.

Os intervalos de confiança bootstrap de 95% das diferenças médias de energia incluíram zero em todas as comparações.

Além disso, nenhum dos testes dos sinais apresentou valor-p inferior a 0,05. Portanto, não foram encontradas evidências estatísticas suficientes, segundo esses testes, para afirmar que uma configuração apresenta desempenho superior às demais.

Na complexidade 10, a diferença média entre a configuração A e a configuração C foi de aproximadamente 0,031245, considerando a subtração A − C. Isso favorece a configuração C em termos de energia média. Entretanto, o intervalo de confiança de 95% dessa diferença foi de aproximadamente -0,000905 a 0,090731, incluindo zero.

De maneira semelhante, a diferença média entre B e C foi de aproximadamente 0,034306, também favorecendo C descritivamente. O intervalo de confiança de 95% foi de aproximadamente -0,000582 a 0,095429, igualmente incluindo zero.

Assim, embora a configuração C tenha apresentado o melhor resultado médio na complexidade 10, a análise estatística não permite concluir que sua vantagem seja estatisticamente significativa.

Esses resultados devem ser interpretados considerando o número de repetições, a variabilidade observada e o fato de terem sido realizadas múltiplas comparações.

## 5. Custo computacional

Os tempos médios de execução foram:

| Complexidade | A — Moderada | B — Intermediária | C — Exploratória |
|---:|---:|---:|---:|
| 2 | 0,0584 s | 0,0571 s | 0,0554 s |
| 6 | 0,0864 s | 0,0862 s | 0,0849 s |
| 10 | 0,1129 s | 0,1132 s | 0,1131 s |

Os tempos de execução foram próximos entre as três configurações em todos os níveis de complexidade.

A configuração C apresentou o menor tempo médio nas complexidades 2 e 6, enquanto a configuração B apresentou o menor tempo na complexidade 10. As diferenças foram pequenas e não indicam uma vantagem computacional expressiva de uma configuração sobre as demais.

Portanto, neste experimento, a escolha da configuração deve considerar principalmente a qualidade e a variabilidade das soluções encontradas, sem atribuir importância excessiva às pequenas diferenças de tempo observadas.

## 6. Configuração selecionada

Com base nos resultados disponíveis, a configuração C, com temperatura inicial de 5,0 e temperatura final de 0,01, é selecionada como candidata para experimentos posteriores envolvendo problemas de maior complexidade.

A escolha se justifica por apresentar a menor energia média e o menor desvio padrão na complexidade 10. Esses resultados indicam um comportamento empiricamente promissor nesse cenário.

Entretanto, a análise estatística não demonstrou superioridade significativa da configuração C em relação às demais. Por isso, a seleção deve ser entendida como uma decisão baseada nos resultados observados, e não como uma comprovação de superioridade geral.

A configuração não foi a melhor em todos os níveis de complexidade, portanto não se pode afirmar que seja universalmente superior. Novos experimentos poderão investigar se essa tendência se mantém em outras instâncias e condições.

## 7. Limitações

O experimento utiliza uma função objetivo artificial para representar aspectos simplificados do docking molecular. Portanto, os resultados permitem comparar o comportamento das configurações nesse modelo, mas não demonstram eficácia em docking molecular real ou em triagem de fármacos.

O estudo considerou três temperaturas iniciais, uma temperatura final fixa, três níveis de complexidade e 30 repetições por configuração e nível. Outros valores de temperatura, critérios de resfriamento e condições experimentais poderiam produzir resultados diferentes.

Embora tenham sido realizadas comparações estatísticas, não foi identificada evidência suficiente para afirmar a superioridade de uma configuração pelo teste dos sinais ao nível de significância de 5%. As comparações múltiplas também recomendam cautela na interpretação dos resultados.

Por fim, os tempos de execução dependem do ambiente computacional utilizado e não devem ser generalizados diretamente para outras máquinas ou implementações.

## 8. Arquivos gerados

Os resultados individuais, os resumos estatísticos e as comparações pareadas são armazenados no diretório `benchmarks/results/`.

Principais arquivos:

- `benchmarks/results/simulated_annealing_tuning_results.csv`
- `benchmarks/results/simulated_annealing_tuning_summary.csv`
- `benchmarks/results/simulated_annealing_tuning_statistical_summary.csv`
- `benchmarks/results/simulated_annealing_tuning_comparisons.csv`

Esses arquivos permitem consultar os resultados das execuções, as estatísticas descritivas e as comparações entre as configurações.

Os experimentos podem ser executados pelo script `benchmarks/tune_simulated_annealing.py`, e a análise estatística pode ser reproduzida pelo script `benchmarks/analyze_simulated_annealing_tuning.py`.