# Roteiro de Apresentação — Kairo Henrique (Pessoa 3)
## Seminário: Tema 6 — Problemas NP-Completos e Aproximações (Cap. 34 e 35)
**Tempo total da Pessoa 3:** ~8 minutos (dentro dos 40 minutos totais do grupo)  
**Tópicos:** Algoritmos Exatos, Intratabilidade, Explosão Combinatória, P ≠ NP, Verificadores de Certificado Polinomial e Demonstração Prática.

---

### Minuto 0:00 – 1:30 | Introdução e o Problema Motivador (Slides 1 e 2)
- **O que falar:**
  > *"Olá a todos, sou o Kairo Henrique. Fiquei responsável pela Pessoa 3: implementação dos algoritmos exatos, verificadores polinomiais e infraestrutura de código do projeto.*  
  > *Para começar, quero propor uma reflexão a partir da pergunta norteadora do nosso trabalho: Por que nenhum computador no planeta consegue encontrar a rota ótima de entrega para 100 cidades?*  
  > *No Caixeiro-Viajante, o espaço de busca para 100 cidades é de (99! / 2) rotas. Isso dá 4,66 vezes 10 elevado a 155. Para termos noção desse número: existem cerca de 10 elevado a 80 átomos em todo o universo observável. Se cada átomo fosse um supercomputador calculando 1 bilhão de rotas por segundo desde o Big Bang, não teríamos verificado nem um grão de areia desse total. É aqui que tocamos a fronteira da computabilidade."*

---

### Minuto 1:30 – 3:00 | A Discussão Teórica P ≠ NP e Classes de Complexidade (Slides 3 e 4)
- **O que falar:**
  > *"Isso nos traz diretamente ao problema do milênio: P versus NP.  
  > A classe P reúne problemas que conseguimos resolver eficientemente em tempo polinomial. Já a classe NP abrange problemas onde encontrar a resposta pode ser dificílimo, mas verificar se uma dada resposta está correta é rápido — é polinomial.  
  > Por que a comunidade científica acredita convictamente que P ≠ NP? Em mais de 50 anos de pesquisa rigorosa, ninguém encontrou um algoritmo polinomial para nenhum dos problemas NP-Completos. Além disso, barreiras teóricas provam que métodos simples de demonstração não são suficientes para provar a igualdade.  
  > E por que essa pergunta vale 1 milhão de dólares? Porque se P fosse igual a NP, toda a criptografia moderna — que protege contas bancárias, comunicações e blockchain — ruiria da noite para o dia, pois quebrar uma chave seria computacionalmente trivial. Por outro lado, resolveríamos otimizações industriais e sínteses químicas de forma perfeita e instantânea."*

---

### Minuto 3:00 – 4:30 | A Essência de NP: O Verificador Polinomial (Slide 4 e 5)
- **O que falar:**
  > *"No Cormen, a definição formal de NP é fundamentada no conceito de certificados polinomiais.  
  > Para demonstrar isso na prática, eu implementei no nosso repositório dois verificadores determinísticos estritos:  
  > 1. Para o Vertex Cover: dado um grafo e um conjunto candidato de vértices, o algoritmo verifica em tempo O(V + E) — linear na entrada — se todos os vértices cobrem todas as arestas e se o tamanho não excede k.  
  > 2. Para o TSP: dada uma matriz de distâncias e uma rota proposta, o verificador checa em O(n) se a rota visita cada cidade exatamente uma vez e se o custo total não ultrapassa o teto estipulado.  
  > Isso cristaliza a assimetria computacional: encontrar a agulha no palheiro pode levar eras, mas conferir se aquilo é uma agulha leva microssegundos."*

---

### Minuto 4:30 – 6:00 | Algoritmos Exatos e a Parede Exponencial (Slides 5, 6 e 7)
- **O que falar:**
  > *"Para a resolução exata, implementei duas frentes:  
  > No Vertex Cover, construí a Força Bruta por enumeração de subconjuntos O(2^n * |E|) e um Branch-and-Bound com poda de ramos não promissores O(2^k * |E|).  
  > No TSP, desenvolvi a Força Bruta O((n-1)! * n) e o clássico algoritmo de Held-Karp por Programação Dinâmica com máscara de bits, que reduz a complexidade de fatorial para O(n² 2^n).  
  > Vejam a diferença absurda: para 15 cidades, a força bruta testa 43 bilhões de rotas e leva quase 1 minuto; o Held-Karp resolve em 7 milissegundos!  
  > Contudo, mesmo o Held-Karp não escapa da barreira exponencial: para 50 cidades, ele exigiria 89 anos e excede qualquer memória RAM física disponível. A parede exponencial é implacável."*

---

### Minuto 6:00 – 7:15 | Demonstração Prática ao Vivo (Slide 8 e Terminal)
- **O que fazer e falar:**
  > *"Vou executar agora, ao vivo no terminal, o nosso script de demonstração de explosão combinatória:"*  
  *(Digitar no terminal: `python benchmarks/demo_combinatorial_explosion.py`)*  
  > *"Observem a tela:  
  > Com 8 cidades, ambos rodam instantaneamente.  
  > Com 10 cidades, a força bruta já demora quase 1 segundo, enquanto o Held-Karp roda em 5 milissegundos — uma aceleração de mais de 160 vezes!  
  > Com 11 cidades, a força bruta já congela o terminal por mais de 10 segundos, enquanto o Held-Karp resolve em 9 milissegundos.  
  > E logo abaixo, vejam a verificação do certificado: validar a rota ótima para 12 cidades levou apenas 35 microssegundos."*

---

### Minuto 7:15 – 8:00 | Conexão com o Estudo de Caso Real e Gancho para os Colegas (Slide 9 e 10)
- **O que falar:**
  > *"Para encerrar, por que isso importa fora da academia?  
  > O nosso grupo escolheu aplicar esse estudo de caso no Molecular Docking e na triagem virtual de fármacos. Quando a indústria farmacêutica desenha um medicamento contra uma doença, ela precisa simular como a molécula se encaixa no sítio receptor da proteína.  
  > Uma molécula modesta com apenas 10 ligações rotacionáveis, discretizadas em passos de 30 graus, possui mais de 61 bilhões de conformações espaciais possíveis. Nenhum algoritmo exato consegue avaliar isso em tempo clínico viável!  
  > É exatamente por isso que a engenharia de software recorre aos Algoritmos de Aproximação (Cap. 35 do Cormen) e às Metaheurísticas, como o Simulated Annealing e os Algoritmos Genéticos.  
  > Passo agora a palavra para o Heitor, que vai explicar como os algoritmos de aproximação garantem limites teóricos de qualidade para contornar essa barreira."*

---

### Dicas para a Apresentação:
- Mantenha o terminal aberto e na pasta do projeto antes de iniciar o seminário.
- Treine o comando `python benchmarks/demo_combinatorial_explosion.py` previamente.
- Use tom confiante e didático, mostrando domínio do livro do Cormen (Cap. 34 e 35).
