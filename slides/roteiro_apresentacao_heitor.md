# Roteiro de Apresentação — Heitor Henrique (Pessoa 4)
## Seminário: Tema 6 — Problemas NP-Completos e Aproximações (Cap. 35)
**Tempo total da Pessoa 4:** ~8 minutos (dentro dos 40 minutos totais do grupo)  
**Tópicos:** O que são Algoritmos de Aproximação, Definição Formal da Razão $\rho(n)$, APPROX-VERTEX-COVER (fator 2), APPROX-TSP-TOUR (fator 2), GREEDY-SET-COVER (fator $H(d)$), Análise do Gráfico Experimental e Transição para Metaheurísticas.

---

### Minuto 0:00 – 1:15 | Introdução e a Filosofia das Aproximações (Slides 1 e 2)
- **O que falar:**
  > *"Obrigado, Kairo! Olá a todos, sou o Heitor Henrique. Fiquei responsável pela Pessoa 4: estudo, implementação e análise experimental dos Algoritmos de Aproximação do Capítulo 35 do Cormen.*  
  > *Como o Kairo acabou de demonstrar, quando enfrentamos um problema NP-completo, a barreira exponencial nos impede de encontrar a solução exata em tempo hábil. Mas na engenharia do mundo real — seja uma rota da Amazon, a otimização de antenas de celular ou o desenho de medicamentos —, nós não podemos simplesmente desistir e dizer que é impossível.*  
  > *É aqui que entra a filosofia dos Algoritmos de Aproximação: nós abrimos mão da perfeição estrita em troca de velocidade instantânea. Porém, com uma diferença crucial em relação a um chute cego: nós temos uma garantia matemática formal de que o erro da nossa resposta é limitado por um teto conhecido como razão de aproximação $\rho(n)$."*

---

### Minuto 1:15 – 2:30 | Definição Formal da Razão e Algoritmo 1: Vertex Cover (Slides 2, 3 e 4)
- **O que falar:**
  > *"Formalmente, dizemos que um algoritmo tem fator de aproximação $\rho$ quando o custo da solução encontrada dividido pelo custo da solução ótima nunca ultrapassa $\rho$. Para um problema de minimização com fator 2, isso significa que garantimos que o custo nunca será mais que o dobro do ótimo.*  
  > *O primeiro algoritmo que implementei foi o APPROX-VERTEX-COVER. O objetivo é escolher o menor número de vértices para vigiar todas as arestas do grafo.*  
  > *Enquanto o algoritmo exato do Kairo precisava testar combinações exponenciais de vértices, a sacada genial do Cormen é olhar para as arestas: o algoritmo pega uma aresta qualquer não vigiada, coloca os dois vértices das pontas dela na solução, e descarta todas as arestas vizinhas. E repete isso até o grafo estar totalmente coberto.*  
  > *Por que isso garante no máximo o dobro do ótimo? Porque as arestas que nós escolhemos são totalmente independentes — elas formam um emparelhamento. Qualquer solução ótima no universo é obrigada a escolher pelo menos um vértice para cada uma dessas arestas. Como o ótimo precisa de pelo menos 1 por aresta e o nosso algoritmo pegou os 2, nós gastamos no máximo duas vezes o tamanho do ótimo! E o algoritmo roda em tempo estritamente linear: $O(V + E)$."*

---

### Minuto 2:30 – 4:00 | Algoritmo 2: APPROX-TSP-TOUR via Árvore Geradora Mínima (Slides 5 e 6)
- **O que falar:**
  > *"O segundo algoritmo é o APPROX-TSP-TOUR, para o Caixeiro-Viajante Métrico.*  
  > *Achar a rota perfeita para 20 cidades levaria séculos por força bruta. Mas o Cormen propõe uma solução em três passos elegantes:*  
  > *1. Primeiro, nós ligamos todas as cidades usando a menor quantidade de estradas possível: calculamos uma Árvore Geradora Mínima com o Algoritmo de Prim.*  
  > *2. Segundo, nós percorremos essa árvore em pré-ordem, listando a ordem em que as cidades são descobertas.*  
  > *3. Terceiro, para não dar ré em galhos sem saída e não repetir cidades, o carro pega atalhos diretos em linha reta para a próxima cidade nova, e fecha o ciclo voltando ao início.*  
  > *Por que isso é uma 2-aproximação? Porque se você apagar qualquer estrada da rota ótima, você obtém uma árvore geradora. Logo, a nossa árvore de Prim custa menos que a rota ótima. Caminhar pela árvore ida e volta custaria no máximo duas vezes a árvore. E como no plano euclidiano vale a Desigualdade Triangular — onde andar em linha reta é sempre mais curto que fazer desvios —, os atalhos não aumentam o custo! Logo, a nossa rota nunca ultrapassa duas vezes o custo do tour ótimo."*

---

### Minuto 4:00 – 5:15 | Algoritmo 3: GREEDY-SET-COVER (Slide 7)
- **O que falar:**
  > *"O terceiro algoritmo é o GREEDY-SET-COVER para a Cobertura de Conjuntos.*  
  > *Aqui temos um universo de elementos e vários subconjuntos candidatos. O objetivo é escolher a menor quantidade de subconjuntos para cobrir todo mundo.*  
  > *O algoritmo adota uma estratégia puramente gulosa: a cada rodada, ele avalia todos os conjuntos disponíveis e escolhe aquele que cobre o maior número de elementos que ainda estão descobertos. Marca esses elementos como cobertos e repete até o universo estar completo.*  
  > *O Cormen prova que, embora essa escolha gulosa não seja sempre ótima, o custo acumulado nunca ultrapassa o número harmônico $H(d)$, que é aproximadamente $\ln(d) + 1$, onde $d$ é o tamanho do maior subconjunto. É uma garantia matemática sólida para um algoritmo que roda em frações de milissegundo."*

---

### Minuto 5:15 – 7:00 | Análise dos Resultados Experimentais e Gráfico (Slides 8 e 9)
- **O que falar:**
  > *"Para validar essas garantias na prática, eu desenvolvi o script de benchmark empírico comparando os nossos três algoritmos aproximados contra as soluções exatas do Kairo nas mesmíssimas instâncias com semente pseudoaleatória fixa.*  
  > *Vejam o gráfico gerado na tela:*  
  > *A linha cinza pontilhada em 1.0 é a perfeição ótima absoluta. A linha vermelha tracejada no topo é o teto teórico garantido pelo Cormen. E a linha azul com as barras de erro mostra os nossos algoritmos rodando na prática.*  
  > *Tiramos duas conclusões fundamentais desses experimentos:*  
  > *Primeira: 100% dos testes ficaram estritamente abaixo da linha vermelha, comprovando que a teoria do livro se sustentou em todos os casos.*  
  > *Segunda: na prática, o comportamento médio é muito superior ao pior caso teórico!*  
  > *No TSP, a teoria dizia que a rota podia ser até o dobro, mas a nossa média ficou entre 1.08 e 1.20 — ou seja, apenas 10% a 20% mais longa que a rota ótima, mas calculada em 0,09 milissegundos!*  
  > *No Set Cover, a média ficou entre 1.00 e 1.06, praticamente idêntica à solução ótima.*  
  > *No Vertex Cover, a barra chegou a encostar no 2.0, o que demonstra experimentalmente que o limitante do Cormen é justo e apertado."*

---

### Minuto 7:00 – 8:00 | Limitações e Passagem para a Pessoa 5 (Slide 10)
- **O que falar:**
  > *"Para finalizar: se os algoritmos de aproximação são tão rápidos e têm garantias matemáticas, por que não usamos eles para tudo?*  
  > *Porque nem todo problema aceita uma aproximação de fator constante. Além disso, em problemas contínuos e altamente acidentados — como a conformação molecular 3D que o Kairo mencionou —, abordagens gulosas e de árvore geradora não se aplicam diretamente.*  
  > *Quando precisamos explorar paisagens de busca não lineares com bilhões de estados, nós recorremos às Metaheurísticas.*  
  > *Passo a palavra agora para a Jade, que vai explicar como o Simulated Annealing e os Algoritmos Genéticos resolvem o problema de Molecular Docking na triagem de novos medicamentos."*

---

### Dicas para a Apresentação:
- Fale com clareza e ritmo tranquilo; o tempo de 8 minutos é ideal e confortável para esse conteúdo.
- Ao projetar o gráfico do Slide 8, aponte diretamente com a mão ou laser para a linha azul mostrando como ela ficou perto do 1.0.
- Lembre-se: o seu papel é demonstrar que aproximação é a ponte entre a matemática rigorosa e a engenharia viável!
