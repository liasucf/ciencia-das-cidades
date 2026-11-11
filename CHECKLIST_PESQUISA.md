# Checklist da pesquisa e dos pedidos da Lia

Conferência em **04/11/2026**, a partir dos pedidos desta conversa, de [PLANO.md](PLANO.md), de [planejamento.md](planejamento.md), de [exploracao.md](exploracao.md) e dos códigos e arquivos existentes.

**Objetivo:** investigar se os pronto-atendimentos do SUS estão bem localizados nas capitais brasileiras, considerando densidade populacional e renda. As leis de potência são o eixo teórico; as distâncias são calculadas pelas ruas com Dijkstra.

**Prioridade atual:** revisão acompanhada dos códigos, mapas, agrupamentos e interpretação para a autora explicar a pesquisa. O artigo foi atualizado e compilado em duas páginas; a autora deve revisar o texto antes de entregar. Extensões opcionais continuam dependendo de escolha.

**Recorte confirmado pela autora (04/11/2026):** manter todo o processamento analítico em notebooks, registro, áreas de atendimento, 16 combinações de quatro faixas de densidade e quatro de renda, separação por densidade, mapas separados de renda/densidade, mapa com uma cor por área de atendimento, mapa de Fortaleza e a parcela de moradores muito longe. Manter o exemplo pequeno de Dijkstra. Para “muito longe”, usar **P90 ponderado pela população de cada capital**; incluir o setor no corte quando sua distância for maior ou igual ao P90 e explicitar que empates/setores indivisíveis podem resultar em mais de 10% dos moradores. **Não desenvolver nesta versão:** CCA, percolação, mapa separado de favela, mapa detalhado da rede/sentidos, mapa de propagação de distâncias, rede de pedestres e otimização de localização. Artefatos antigos são preservados como histórico. A seleção dos 16 grupos é classificação por faixas, sem CCA/percolação.

**Ajuste solicitado pela autora em 04/11/2026:** deixar a comparação favela/não favela para depois. Não tratar suas curvas ou aprofundamentos como obrigação pendente agora. Os dados e resultados já existentes são preservados; não remover nem refazer automaticamente o artigo. A revisão atual dos slides identifica possibilidades, sem escolher novos métodos ou parâmetros.

## Como ler os checks

- **✅ Implementado:** há código/artefato e evidência de execução ou saída. Isso **não significa** que a autora já tenha compreendido a etapa nem que a revisão metodológica esteja encerrada.
- **🟡 Parcial:** alguma parte existe, mas falta migrar, executar por completo, conferir ou desenvolver a apresentação pedida.
- **⬜ Não implementado:** não encontrei a implementação correspondente. Quando a ideia era opcional, isso está indicado; não foi transformada em obrigação.
- **⏸ Em segundo plano:** já foi produzido, mas não é a prioridade atual.
- **➖ Fora da versão atual:** exclusão ou simplificação já combinada; não é tarefa esquecida.

Nenhuma nova escolha metodológica foi feita nesta conferência. A tabela distingue o pedido direto da autora das possibilidades que estavam registradas no planejamento.

## A. Forma de trabalhar e aprendizado

| ID | Pedido/compromisso | Situação | Evidência e o que falta |
|---|---|---|---|
| A01 | Manter a pergunta sobre localização, densidade e renda como objetivo | ✅ Registrado | Objetivo confirmado novamente pela autora; [PLANO.md](PLANO.md), seção 1. Cada análise precisa voltar a essa pergunta. |
| A02 | Fazer todas as fases analíticas em notebooks; scripts só para coleta pura | ✅ Fluxo analítico atual em notebooks | A retomada começa nos arquivos brutos, confere coordenadas pelo cache local, prepara tabelas e executa as distâncias completas em notebooks. Scripts antigos permanecem como histórico/coleta. |
| A03 | Rodar os notebooks e mostrar as saídas | ✅ Executados e artigo atualizado | Auditoria, correção histórica, L1–L3 e os notebooks novos 01–04 da retomada e figura de síntese foram executados sem erros salvos. O artigo foi refeito após a escolha da distância total e compilado em duas páginas. A revisão explicada com a autora continua pendente. |
| A04 | Explicar passos, variáveis, funções e resultados para a autora defender o trabalho | 🟡 Insuficiente | Há textos nos notebooks, mas a autora explicitou que a condução não permitiu compreender a pesquisa. O acompanhamento não recebeu check. |
| A05 | Explicar termos antes de usá-los | 🟡 A corrigir na condução | Exemplos: densidade de população versus de unidades; quartil; agrupamento; resíduo; intervalo; o que significa o sinal do coeficiente da renda. Evitar termos como “compensatório” sem tradução em palavras simples. |
| A06 | Discutir novas decisões antes de implementá-las | 🟡 Processo a cumprir continuamente | Há decisões autorizadas registradas; a progressão ficou rápida demais. Novas escolhas de clusterização ou de análise devem ser explicadas e discutidas. |
| A07 | Usar teoria, técnicas e referências das aulas e da Bibliografia | ✅ Fontes locais usadas; revisão explicada pendente | Referências do artigo conferidas nos PDFs. Falta mostrar à autora, em cada etapa, a ligação entre código, hipótese e material do curso. |
| A08 | Construir gráficos progressivamente para compreender a pesquisa | 🟡 Parcial | Gráficos foram produzidos, mas faltou construí-los e interpretá-los junto com a autora. A qualidade e clareza não recebem check apenas pela existência de PNGs. |
| A09 | Manter registro para não esquecer pedidos e ideias | ✅ Iniciado | Este arquivo passa a reunir o acompanhamento. Mudanças devem ser registradas com evidência, sem apagar as ideias opcionais. |

## B. Dados, preparação e distâncias

| ID | Pedido/ideia | Situação | Evidência e o que falta |
|---|---|---|---|
| B01 | Dados das capitais: CNES, população, setores, renda e ruas | ✅ Preparação reproduzida em notebook | Notebook `retomada/01_dados.ipynb`; mapa/variável de favela existe nos dados, mas sua análise foi adiada. |
| B02 | Usar todos os estabelecimentos ativos do tipo 73, definindo “pronto-atendimento” | ✅ Implementado em notebook | Cadastro e regra descritos em `retomada/01_dados.ipynb`; 274 unidades em Todos e 245 no recorte SUS. |
| B03 | SUS como principal e todos como comparação | ✅ Implementado | 245 SUS e 274 no conjunto; notebooks 01–05 e CSVs separados por versão. |
| B04 | Usar a renda média do responsável e quartis dentro de cada capital | ✅ Implementado | V06004 agregada nas áreas; quartis por capital no notebook 04. A renda não é renda per capita e os quartis são de setores, não de moradores. |
| B05 | Conferir coordenadas e usar o arquivo corrigido | 🟡 Parcial | `conferencia_coordenadas.csv` e `pa_capitais_corrigido.csv`; procedimento antigo em script. Permanecem 20 registros `revisar_manual`, cuja revisão à mão estava como opcional. |
| B06 | Corrigir setores divididos em vários polígonos | ✅ Recalculado integralmente | Notebook `retomada/03_distancias_completas.ipynb`: une geometrias por código antes de contar população/área e recalcula os pontos representativos. Originais preservados. |
| B07 | Calcular distância pela rede de carro, dirigida, respeitando o sentido do trajeto | ✅ Distância total escolhida e recalculada | A autora aprovou minimizar a soma ligação setor–rua + percurso + ligação unidade–rua. O notebook 03 da retomada recalculou as 52 tabelas e comparou associações com a regra anterior. |
| B08 | Usar faixa de 5 km além do município e explicar o recorte da rede | ✅ Código e explicação em notebook | O recorte, maior componente e projeção estão no notebook 03 da retomada; interpretação acompanhada ainda pendente. |
| B09 | Excluir ligações à rua acima de 2 km, setores sem moradores e distâncias não finitas | ✅ Filtro implementado | Notebooks 01, 02 e 04; resumos de população excluída. Falta explicar à autora quem sai e como isso limita as conclusões. |
| B10 | Conferir distâncias e associações: rede versus linha reta, setores sem rota e ligações suspeitas | ✅ Conferido com a regra escolhida | O notebook 03 compara a menor soma completa com a regra anterior, valida que a nova distância não é maior e verifica setores sem rota e ligações. O diagnóstico da ilha está no notebook 05. |
| B11 | Representar as duas unidades de Bom Jesus ligadas ao mesmo nó | ✅ Alternativa A autorizada e aplicada | `corrigidos/grupos_unidades.csv`; área compartilhada, duas unidades na versão com todos, sem duplicar moradores ou área. |

## C. Clusterização e outros agrupamentos

Aqui existem ideias diferentes. **Agrupar pelo atendimento mais próximo**, **classificar por faixas de renda/densidade** e **descobrir manchas espaciais por CCA/percolação** não são a mesma operação.

| ID | Ideia registrada | Situação | Evidência e o que falta |
|---|---|---|---|
| C01 | Agrupar setores pela unidade mais próxima: áreas de atendimento | ✅ Recalculado em notebook | Notebook 03 da retomada gera áreas de atendimento e grupos de unidades que compartilham nós. A regra final de distância ainda depende da autora. |
| C02 | Tipologia densidade × renda: 16 combinações dos quatro quartis | ✅ Tabela e mapas executados | Notebook `retomada/04_mapas_grupos_P90.ipynb` calcula os 16 grupos para as capitais e produz mapas de calor. Classificação por faixas, não descoberta automática de grupos. As figuras e tabelas foram atualizadas com a regra de distância escolhida. |
| C03 | Destacar favelas dentro dos agrupamentos | ⏸ Aprofundamento adiado pela autora | Há indicador, médias de distância e contornos em artefatos existentes. Não expandir essa comparação nem tratá-la como obrigação atual. A existência do indicador não confirma completude da rede de acessos. |
| C04 | Separar setores acima/abaixo de 1.500 moradores/km² | ✅ Mapa em notebook | O notebook de mapas separa as faixas em Fortaleza e explica que o corte sozinho não forma manchas contíguas nem implementa CCA. |
| C05 | CCA: formar aglomerados de células densas próximas | ➖ Não desenvolver nesta versão, por escolha da autora | Possibilidade do curso preservada no histórico; a autora respondeu “CCA não”. |
| C06 | Percolação na rede: formar grupos variando um critério de conexão | ➖ Não desenvolver nesta versão, por escolha da autora | Possibilidade do curso preservada no histórico; a autora respondeu “percolação não”. |
| C07 | k-means, DBSCAN e métodos fora do material | ➖ Excluídos no plano atual | O plano proíbe acrescentá-los. Um novo pedido não será interpretado automaticamente como autorização para trocar o método. |

## D. Mapas e visualizações de entendimento

| ID | Pedido/ideia | Situação | Evidência e o que falta |
|---|---|---|---|
| D01 | Mapas separados de densidade e renda em Fortaleza | ✅ Mapas gerados em notebook | `retomada/04_mapas_grupos_P90.ipynb` gera mapas separados de quartis de renda e densidade, sem análise de favela. |
| D02 | Mapa da rede de ruas: interseções, trechos e sentidos | ➖ Não desenvolver nesta versão | A autora disse que não precisa desse mapa. A rede dirigida continua sendo usada para calcular as distâncias. |
| D03 | Exemplo pequeno para entender Dijkstra antes de usar a cidade inteira | ✅ Executado em notebook | `retomada/02_dijkstra_exemplo.ipynb`, com ruas de dois sentidos e mão única, tabela passo a passo e conferência independente. |
| D04 | Mapa da propagação das distâncias pela rede (“onda” do Dijkstra) | ➖ Não desenvolver nesta versão | A autora não quer esse mapa. A figura antiga permanece como histórico. |
| D05 | Mapa com uma cor por área de atendimento para entender os grupos | ✅ Mapa dedicado gerado | Fortaleza SUS, 12 grupos, uma cor por código CNES representativo; arquivo em `figuras/retomada/mapas/05_fortaleza_areas_atendimento.png`. |
| D06 | Mapas de entendimento em Fortaleza | ✅ Mapas dedicados gerados | Mapas separados de renda, densidade, áreas de atendimento e setores ≥ P90. Nenhum mapa de favela na versão atual. |
| D07 | Gráficos sobre população, área e densidades | ✅ Gerados em notebook | Notebook 02: histogramas, população × área e relação entre densidades. Falta interpretação acompanhada dos eixos e dos pontos. |
| D08 | Mapa de calor densidade × renda das 26 capitais | ✅ Calculado e desenhado | Notebook 04, SUS e todos. Cada célula tem distância relativa média ponderada pela população. Falta percorrer sua construção e leitura com a autora. |
| D09 | Curvas de distância das capitais e por renda | ✅ Geradas | Notebook 04: 26 curvas SUS e curvas relativas por renda nas duas versões. L3 descritiva aprovada. |
| D10 | Curvas de distância por favela/não favela | ⏸ Adiadas pela autora; não são tarefa obrigatória agora | Não foram implementadas; há somente médias no notebook 04. A autora pediu deixar essa comparação para depois em 04/11/2026. |
| D11 | Comparação visual entre SUS e todos | ✅ Em vários gráficos | Notebooks 02–05 e resumos. A figura atual de quatro painéis usa SUS. Falta explicar à autora o que cada comparação permite concluir. |
| D12 | Mostrar a parcela de moradores muito longe em cada grupo densidade × renda | ✅ Calculado em notebook | P90 ponderado por capital; mapas e tabela por 16 grupos disponíveis. Fortaleza SUS: P90 de 5,73 km e 10,0% dos moradores em setores ≥ P90. |
| D13 | Gráficos bonitos, legíveis, construídos de acordo com os resultados | 🟡 Avaliação com a autora pendente | Há paleta comum, saídas nos notebooks e figura vetorial. Produzir arquivos e fazer revisão técnica não substitui verificar se eles ajudam a autora a compreender. |

## E. Análises principais e extensões

| ID | Pedido/ideia | Situação | Evidência e o que falta |
|---|---|---|---|
| E01 | L1: unidades × população; comparar β com 1 | ✅ Implementada e executada | Notebook 05, SUS e todos, com 2.000 reamostragens e IC. Falta revisar o código e a interpretação com a autora. |
| E02 | L2: densidade de unidades × densidade de moradores; comparar α com 2/3 e 1 | ✅ Implementada e executada | Notebook 02, SUS e todos. A comparação de expoentes não calcula por si só a localização ótima. Falta revisão explicada. |
| E03 | Relacionar renda e oferta considerando densidade | ✅ Modelo simples autorizado e executado | Notebook 03, SUS e todos. O modelo reúne capitais; diferenças entre cidades e ausência de causalidade limitam a conclusão. Falta explicar o código e as palavras usadas na interpretação. |
| E04 | L3 descritiva, curvas e Gini da distância | ✅ Implementada e aprovada | Notebook 04. Não há estimativa de γ nem teste formal de rejeição de lei de potência. Falta leitura acompanhada. |
| E05 | Regressão específica por capital/efeitos fixos ou renda relativa | ➖ Não usada por escolha da autora | A autora escolheu somente o modelo conjunto simples. Não tratar essa opção descartada nesta etapa como obrigação não cumprida. |
| E06 | Estimar γ ajustando uma cauda | ➖ Não faz parte da versão aprovada | A autora confirmou L3 descritiva. Um estudo futuro de cauda exigiria nova discussão. |
| E07 | Comparar localização observada com distribuição ótima por p-mediana | ➖ Não desenvolver nesta versão | A autora recusou a comparação com uma localização otimizada. A referência teórica de α=2/3 continua parte da L2. |
| E08 | Testar robustez com rede de pedestres | ➖ Não desenvolver nesta versão | A autora recusou essa comparação. A versão atual usa somente a rede de carro. |
| E09 | Repetir L1 com concentração urbana/definição alternativa de cidade | ⬜ Não implementada; opcional | O dado `NM_CONCURB` existe, mas não foi encontrado esse ajuste. Ligação com CCA/limites da cidade precisa ser discutida. |
| E10 | Tempo de viagem, betweenness, “pequeno mundo” | ➖ Fora do escopo aprovado | Exclusões registradas no plano; não são etapas esquecidas. |

## F. Artigo e apresentação final

| ID | Pedido/decisão | Situação | Evidência e o que falta |
|---|---|---|---|
| F01 | Artigo em português, LaTeX, até três páginas, respondendo às três perguntas do manual | 🟡 Rascunho atualizado; revisão da autora pendente | Notebook 07 gera `artigo/artigo.pdf` com duas páginas, uma figura, problema, métodos, resultados e limitações; citações resolvidas e inspeção visual feita. Lia ainda deve aprovar o texto antes da entrega. |
| F02 | Figura de síntese com 16 grupos, P90 e mapas de Fortaleza | ✅ Gerada e conferida | Notebook 06 produz PDF vetorial e PNG com quatro painéis, atualizados após a decisão sobre a distância total. |
| F03 | Nome e instituição: Lia Sucupira — Universidade de Fortaleza | ✅ Preenchido | Configuração do notebook 07 e autoria visível no PDF. |
| F04 | Conseguir explicar a pesquisa, os códigos, escolhas e limitações ao professor | 🟡 Não concluído | A própria autora relatou que ainda não compreendeu o percurso. Este é o critério de acompanhamento que faltou cumprir; não pode receber check pela compilação do artigo. |

## Evidência de execução dos notebooks existentes — snapshot histórico anterior à retomada integral

Esta conferência **leu os registros e as saídas salvas**; não foi uma nova execução completa do pipeline. Os notebooks foram executados nas etapas anteriores da sessão. As contagens abaixo não provam que o processamento original inteiro foi reproduzido em notebook nem substituem revisão metodológica.

| Notebook | Células de código com execução registrada | Erros salvos | Figuras PNG nas saídas |
|---|---:|---:|---:|
| 00 — conferência | 9/9 | 0 | 4 |
| 01 — correção de setores | 7/7 | 0 | 2 |
| 02 — L2 | 8/8 | 0 | 4 |
| 03 — renda e resíduos | 5/5 | 0 | 3 |
| 04 — distâncias e L3 | 6/6 | 0 | 4 |
| 05 — L1 | 5/5 | 0 | 1 |
| 06 — figura histórica de síntese | 3/3 | 0 | 1 |
| 07 — artigo | 4/4 | 0 | 0 |
| **Total** | **47/47** | **0** | **19** |

Lacuna central: no notebook 01, apenas os setores com várias partes têm suas distâncias recalculadas. As demais distâncias são herdadas do processamento anterior. Logo, o pedido A02 continua **parcial**.

## Proposta de retomada — ainda não é uma nova escolha metodológica

1. Percorrer este checklist com a autora e corrigir qualquer pedido/ideia que ela acrescente.
2. Priorizar o núcleo que explica os dados, a rede e os agrupamentos: mapas separados de densidade e renda; exemplo pequeno de Dijkstra; mapa com uma cor por área de atendimento.
3. Completar a preparação dos dados e o Dijkstra integral em notebooks, com blocos pequenos, saídas visíveis e verificações explicadas.
4. Retomar os 16 grupos densidade × renda em mapas de entendimento, antes de interpretar os coeficientes.
5. Discutir separadamente se a autora quer avançar em CCA, percolação ou p-mediana. São ideias preservadas no checklist; não foram implementadas nem descartadas por decisão do agente.

Cada etapa deve mostrar: **pergunta → dados → código → execução/conferências → gráfico → interpretação em palavras simples → relação com a pergunta da pesquisa**. Novas decisões metodológicas continuam dependendo de conversa com a autora.

## Revisão das ideias nos slides — 04/11/2026

Foram lidos os textos das cinco apresentações e inspecionadas as imagens dos slides 10–12 e 19–21 da Aula 5. A tabela identifica conteúdos reais do material; não afirma que a autora já escolheu todas essas possibilidades.

| Conteúdo | Onde está | Ideia em palavras simples | Dados e cuidado antes de implementar | Situação |
|---|---|---|---|---|
| Formar uma mancha urbana por densidade | Aula 5, slide 5 | Selecionar células densas, juntar vizinhas e observar o conjunto que se forma. | O exemplo usa grade de 1 km², mais de 1.500 moradores/km², contiguidade, mínimo de 50 mil moradores e preenchimento de lacunas. Temos setores de áreas diferentes. Só pintar setores acima de 1.500 não reproduz esse procedimento; seria necessário preparar a grade ou discutir uma adaptação. | Ideia do curso; método completo não implementado. |
| CCA — City Clustering Algorithm | Aula 5, slides 10–12 | Começar por regiões densas e juntar regiões próximas para formar grupos espaciais. | As imagens mostram tanto uma grade quanto uma versão com polígonos/pontos e distância de vizinhança. Temos população e geometrias para discutir uma implementação; ainda é preciso escolher e justificar a versão e os parâmetros. | Opcional no plano; não implementado. |
| Comparar limite administrativo e cidade identificada nos dados | Aula 5, slides 7–8 e 16–18 | A cidade vivida pode ultrapassar o limite do município; a fronteira escolhida muda as medidas e os ajustes. | Na versão atual usamos limites municipais. Um novo recorte pode exigir ampliar também unidades, população e rede para os municípios vizinhos; não basta desenhar uma nova borda sobre as mesmas entradas. | Possibilidade a discutir; nenhum recorte novo adotado. |
| Unir aglomerados por deslocamentos entre eles | Aula 5, slide 17, passo 2 | Juntar grupos que trocam muitos deslocamentos de trabalho. | O passo requer fluxos origem–destino. Não foi identificada uma tabela desses fluxos no pipeline atual. O primeiro passo, por densidade/adjacência, é distinto desse segundo passo. | Informação adicional necessária; não implementado. |
| Percolação da rede viária | Aula 5, slides 19–20 | Variar um critério de conexão, observar quais partes da rede se juntam e desenhar o tamanho do maior grupo conforme esse critério muda. | Temos os grafos de ruas, nós e comprimentos. Antes de codificar, conferir a regra de ativação: o texto do slide 19 descreve uma desigualdade, enquanto a figura mostra o maior grupo crescendo com o limiar. Não assumir nem inverter silenciosamente a regra; esclarecer a leitura do material. | Opcional no plano; não implementado. |
| Comparar grupos da rede com a renda no mapa | Aula 5, slide 21 | Colocar lado a lado o mapa de renda e o mapa dos grupos formados pela rede, procurando relações espaciais. | Temos renda por setor e ruas, mas os grupos por percolação ainda não foram calculados. Comparar os mapas não demonstra causalidade. Esta é uma possibilidade identificada na revisão dos slides, ainda não uma nova etapa aprovada. | Boa candidata para discussão sobre mapas e agrupamentos. |
| Leis de escala entre indicadores urbanos e população | Aula 4, slides 22–26; Aula 5, slide 15 | Perguntar como um indicador varia entre cidades de populações diferentes. | É a base de L1; os ajustes existem, mas falta executar e interpretar os blocos junto com a autora. | Implementado; acompanhamento pendente. |
| Localização de serviços e densidade | Aula 4, slides 42–44 | Relacionar a densidade de estabelecimentos à densidade de moradores e discutir a referência de dois terços. | É a base de L2. Comparar expoentes não equivale a realocar serviços para encontrar a localização ótima. | Implementado; acompanhamento pendente. |

### O que a conferência esclareceu sobre favela

O arquivo atual `dados/processados/setores_capitais.csv` contém a coluna `favela`, construída no processamento a partir de `CD_TIPO`. A amostra SUS corrigida também contém a coluna. Portanto, hoje há uma marcação para separar os setores no nível mais básico. Isso não constitui uma auditoria da classificação nem garante que o OSM represente todas as ruas, becos e acessos dessas áreas. O plano registra essa limitação da rede. Não foi localizado nos documentos consultados um registro que permita reconstruir com certeza a conversa anterior sobre falta de dados; não atribuir uma lembrança específica à autora.

**Decisão atual é suficiente e prevalece:** favela/não favela fica para depois, independentemente da disponibilidade dessa coluna. O foco da retomada é densidade, renda, ruas, agrupamentos e mapas de entendimento.

## Retomada executada — 04/11/2026

O fluxo analítico foi executado em notebooks, incluindo a nova regra da menor distância total aprovada pela autora. As distâncias, L2, renda, L3, mapas, figura e artigo foram atualizados. A tabela abaixo registra a execução; a revisão didática com a autora continua pendente.

| Notebook | Execução atual | O que faz / evidência |
|---|---|---|
| `notebooks/retomada/01_dados.ipynb` | ✅ 10/10; sem erros | Prepara CNES, coordenadas, população, setores e renda. |
| `notebooks/retomada/02_dijkstra_exemplo.ipynb` | ✅ 7/7; sem erros | Exemplo didático de menor caminho dirigido. |
| `notebooks/retomada/03_distancias_completas.ipynb` | ✅ 8/8; sem erros | Recalcula 52 tabelas com a menor soma total e compara com a regra antiga. |
| `notebooks/retomada/05_diagnostico_areas_sem_setores.ipynb` | ✅ 5/5; sem erros | Identifica os setores excluídos e o grupo do PA Ilha de Maré sem área válida no L2. |
| `notebooks/02_L2_densidade.ipynb` | ✅ 8/8; sem erros | SUS: 245 áreas/245 unidades; Todos: 272 áreas/273 unidades representadas. |
| `notebooks/03_renda_residuos.ipynb` | ✅ 5/5; sem erros | Reajusta o modelo de renda com as áreas atualizadas. |
| `notebooks/04_distancias_L3.ipynb` | ✅ 6/6; sem erros | Curvas e Gini descritivos com distâncias atualizadas; favela fora do escopo atual. |
| `notebooks/retomada/04_mapas_grupos_P90.ipynb` | ✅ 11/11; sem erros | Atualiza mapas, grupos 4×4 e P90; legenda do mapa de densidade foi ajustada. |
| `notebooks/06_figura_final.ipynb` | ✅ 3/3; sem erros | Gera a figura vetorial atual com quatro painéis. |
| `notebooks/07_artigo.ipynb` | ✅ 4/4; sem erros | Gera e compila o artigo de duas páginas; referências resolvidas e PDF inspecionado. |

## Atualização após a escolha metodológica — 04/11/2026

A autora aprovou a menor distância total pela rede. Foi implementada no notebook 03 da retomada com uma fonte auxiliar por unidade, acrescentando o custo da ligação da unidade antes de selecionar o destino. A verificação confirmou que nenhuma unidade com ligação à rede acima de 2 km recebeu setores válidos; a maior ligação entre destinos atribuídos a setores válidos foi 437 m.

O notebook [05_diagnostico_areas_sem_setores.ipynb](notebooks/retomada/05_diagnostico_areas_sem_setores.ipynb) identificou uma exceção: PA Ilha de Maré, em Salvador, Todos, com ligação de 5.166 m ao componente viário selecionado; recebeu dois setores (1.178 moradores), ambos com ligação à rua de 4.904 m e 6.136 m. Ambos ficam fora pelo filtro de 2 km já aprovado. A autora autorizou que o grupo sem área válida seja excluído apenas de L2 e renda, mantendo a unidade no cadastro e registrando a exclusão.

**L2 atualizado:** SUS α=0,861 [0,797; 0,935], 245 áreas/245 unidades; Todos α=0,899 [0,834; 0,973], 272 áreas/273 unidades representadas. **Renda atualizada:** SUS δ=−0,196 [−0,353; −0,029]; Todos δ=0,029 [−0,122; 0,188]. L3, mapas, figura e artigo foram recalculados. O artigo compila em duas páginas, com citações resolvidas e inspeção visual concluída; falta a autora revisar e conversar sobre a interpretação.
