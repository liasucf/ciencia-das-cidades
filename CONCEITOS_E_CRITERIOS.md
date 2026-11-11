# Conceitos do curso e critérios do trabalho

Revisão de 04/11/2026, feita para acompanhar a pesquisa com Lia Sucupira. Este documento separa exigências do professor, conceitos realmente usados e ferramentas de cálculo. Não é necessário incluir todas as aulas nem contar cada gráfico como um conceito diferente.

## 1. O que o manual do professor exige

Fonte: [Manual do trabalho escrito.pdf](Manual%20do%20trabalho%20escrito.pdf).

| Critério explícito | Como o projeto o aborda | Conferência necessária |
|---|---|---|
| Análise de dados ou modelo relacionado a cidades | População, renda, setores, estabelecimentos e rede de ruas de capitais brasileiras. | Verificar o recorte, a origem dos dados e suas limitações. |
| Usar algum tema e técnica comentados no curso | Leis de escala e distribuição espacial de serviços são o núcleo. | Mostrar a ligação com os slides e referências, conforme a tabela abaixo. O manual não fixa quantidade mínima de conceitos. |
| Até três páginas | Existe um PDF compilado com três páginas. | Conferir novamente depois de revisar as análises e o texto. |
| Pelo menos um elemento gráfico | Existem mapas e gráficos, além da composição de cinco painéis. | Selecionar figuras legíveis que sustentem as conclusões, após inspeção das saídas. |
| Explicar o problema e contextualizar com referências | Pergunta sobre densidade, renda e localização do pronto-atendimento SUS. | A autora precisa conseguir formular a pergunta e explicar sua importância. |
| Descrever dados e métodos | Processamento em notebooks; distâncias, grupos, ajustes e comparações. | Executar e conferir o percurso inteiro. A migração completa está sendo feita na retomada. |
| Apresentar resultados e conclusões, discutindo limitações | Comparar os expoentes com referências e examinar a distância nos grupos de renda/densidade. | Não confundir associação com causalidade, comparação de expoentes com otimização ou desenho de curva com rejeição estatística. |

O uso de dados brasileiros é uma recomendação do manual. O projeto a segue. O manual não exige utilizar CCA, percolação, um algoritmo de clusterização específico ou um número mínimo de técnicas.

## 2. Conceitos efetivamente presentes

| Conceito | Explicação em palavras simples | Onde entra no trabalho | Vínculo com o material |
|---|---|---|---|
| Leis de escala urbana | Comparar como um indicador varia entre cidades com populações diferentes. | L1: número de unidades em função da população; interpretar β e comparar com 1. | Aula 4, slides 22–26; Aula 5, slide 15; Bettencourt e Melo. |
| Escala intraurbana e densidade de serviços | Estudar a relação entre moradores e estabelecimentos por área, dentro do conjunto das cidades. | L2: densidade de estabelecimentos versus densidade populacional; comparar α com 2/3 e 1. | Aula 4, slides 33 e 42–44; Gastner e Newman; Xu et al. |
| Acessibilidade espacial | Medir quão longe uma região está de um serviço, considerando as ruas disponíveis. | Distância do ponto de cada setor até o atendimento na rede; mapas e parcela de moradores além do P90. | Aula 4, slides 40–44; Maia et al. e Xu et al. na Bibliografia. |
| Representação por redes | Representar cruzamentos como nós e trechos de rua como arestas, com comprimento e direção. | Grafo dirigido e Dijkstra; explicar por que o sentido do percurso importa. | Representação nó/rua na Aula 5, slide 19; Dijkstra nos métodos de Maia et al. Não estamos usando o método de percolação desse slide. |
| Distribuições estatísticas | Observar toda a variação das distâncias em vez de olhar só a média. | Histogramas e curvas da fração de moradores acima de cada distância. | Aula 2, slide 40; Aula 3, slide 25; Newman na Bibliografia. Uma análise descritiva não é ajuste de potência da cauda. |
| Heterogeneidade espacial | Reconhecer que diferentes partes da mesma cidade têm população, renda e acesso diferentes. | Mapas separados de renda/densidade; 16 combinações de quatro faixas de cada variável. | Aula 2, slide 26; Aula 3, slides 11 e 29. A classificação por faixas não é CCA nem descoberta automática de grupos. |
| Áreas de atendimento | Juntar setores associados à mesma unidade para estudar a região representada por ela. | Agrupamento por atendimento; área, população, renda e número de unidades dos grupos entram em L2. | Xu et al. na Bibliografia. Não são áreas oficiais do SUS. |
| Desigualdade de acesso | Comparar a distribuição de distâncias e verificar se grupos enfrentam situações diferentes. | Gini da distância, comparação entre faixas de renda/densidade e parcela além do P90. | Xu et al. na Bibliografia; discussão de acessibilidade e heterogeneidade nas aulas. |
| Definição e escala da unidade espacial | Reconhecer que o resultado depende da região usada como unidade de observação. | Capital para L1, área de atendimento para L2, setor para mapas; limites municipais e efeitos de borda. | Aula 5, slides 7–8 e 16–18; Arcaute et al. Essa questão é uma limitação discutida, não um experimento de fronteiras alternativas já realizado. |

L1 e L2 são aplicações relacionadas do conceito de escala, não duas teorias independentes. Acessibilidade e redes também se conectam. A qualidade vem da articulação dessas ideias para responder à pergunta, não do tamanho da lista.

**Precisão sobre o Gini:** Xu et al. calculam o Gini de um índice de ganho relativo à localização ótima. O nosso indicador é o Gini das distâncias observadas, ponderado pelos moradores. A medida é inspirada pela pergunta distributiva, mas não é o mesmo indicador nem reproduz a comparação com uma localização ótima.

## 3. Ferramentas de apoio: o que significam

| Ferramenta | Para que usamos | Cuidado |
|---|---|---|
| Média ponderada pela população | Um setor com mais moradores pesa mais na medida de acesso. | Uma medida por setor não é a mesma coisa que uma medida por morador. |
| Quartis | Dividir os setores em quatro faixas de uma variável, por capital. | Quatro faixas com números semelhantes de setores não contêm necessariamente números semelhantes de moradores. |
| P90 ponderado | Identificar a distância que alcança 90% dos moradores da capital, segundo as distâncias atribuídas aos setores. | Empates e setores indivisíveis podem deixar mais de 10% na condição distância ≥ P90. É um critério relativo de análise, não um padrão clínico. |
| Regressão em logaritmos | Estimar o expoente de uma relação multiplicativa e sua associação com renda/densidade. | O expoente e o sinal do coeficiente não demonstram causalidade. |
| Bootstrap | Repetir ajustes em amostras sorteadas para examinar sua variação. | O sorteio de áreas não incorpora explicitamente dependência espacial ou entre áreas da mesma cidade. |

São ferramentas estatísticas usadas na pesquisa; não serão apresentadas artificialmente como várias teorias urbanas novas.

## 4. Avaliação da ideia e pontos que podem enfraquecer a execução

A pergunta é pertinente porque uma contagem municipal pode ocultar regiões com situações distintas de acesso. Relacionar densidade, renda e rede de ruas permite investigar essa diferença com conceitos do curso. Isso não antecipa uma nota nem comprova que toda a implementação esteja validada.

O trabalho perderia força se:

- exibisse muitos gráficos sem explicar qual pergunta cada um responde;
- chamasse cortes em quatro faixas de CCA ou tratasse cores iguais como prova de grupos descobertos automaticamente;
- interpretasse α próximo de uma referência como prova de localização ótima;
- tratasse um coeficiente conjunto entre capitais como efeito causal da renda ou exclusivamente como diferença entre bairros da mesma cidade;
- apresentasse uma curva em log-log como teste formal de lei de potência;
- ocultasse as aproximações dos pontos dos setores, das coordenadas e das ligações à rede;
- encerrasse a pesquisa pela compilação do PDF, sem conferir cálculos, imagens e interpretação com a autora.

## 5. Ordem de trabalho confirmada

1. Refazer e executar o processamento em notebooks.
2. Conferir cálculos, associações, tabelas e saídas.
3. Inspecionar os mapas e gráficos e explicar o que eles mostram.
4. Discutir correções ou escolhas novas com a autora.
5. Atualizar o relatório/artigo somente a partir das análises conferidas. **Concluído em 04/11/2026:** artigo atualizado, compilado em 2 páginas e inspecionado visualmente.
6. Fazer a revisão didática com a autora; a existência de notebooks executados não substitui sua compreensão e a revisão do texto antes da entrega.

CCA, percolação, pedestres, otimização de localização, mapa separado de favela e mapas detalhados da rede/propagação não fazem parte da versão escolhida pela autora. O exemplo pequeno de Dijkstra foi mantido por escolha expressa. O acompanhamento dos itens está em [CHECKLIST_PESQUISA.md](CHECKLIST_PESQUISA.md).


## Atualização dos artefatos — 04/11/2026

A regra adotada agora é a menor distância total com custos das ligações à rua. Os valores L2 e de renda em notebooks e artigo foram recalculados. A autora autorizou excluir o grupo do PA Ilha de Maré apenas dos ajustes por áreas, pois seus dois setores (1.178 moradores) não passam pelo filtro de 2 km; o caso está explicado no notebook de diagnóstico. O artigo responde aos critérios de formato e foi visualmente conferido, mas a conversa de aprendizagem e a revisão da autora ainda são necessárias.
