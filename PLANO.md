# PLANO: trabalho final de Ciência de Cidades

Documento de passagem para o agente que vai continuar o projeto. Ele resume o que já foi decidido, o que já está pronto e o que falta. Os detalhes estão em [planejamento.md](planejamento.md) (o plano completo) e em [exploracao.md](exploracao.md) (a exploração dos dados, com figuras e resultados preliminares).

**Prioridade atual — retomada solicitada pela usuária em 04/11/2026:** deixar a edição do artigo de lado e focar na pesquisa, nos códigos e no aprendizado acompanhado. A usuária precisa explicar cada escolha, código, gráfico e conclusão ao professor. Os rótulos de etapas "concluídas" abaixo indicam implementação e execução, não encerramento da revisão metodológica ou do processo de aprendizagem. Não avançar para a escrita para substituir essa revisão.

**Controle dos pedidos:** consultar [CHECKLIST_PESQUISA.md](CHECKLIST_PESQUISA.md), que reúne os pedidos desta conversa e as ideias do planejamento, incluindo agrupamentos, CCA/percolação, mapas de entendimento, lacunas de migração e evidências de execução. Não usar os checks antigos como substitutos desse controle. A autora voltou a destacar clusterização e mapas; as ideias opcionais continuam registradas, sem escolha automática de implementá-las ou descartá-las.

**Ajuste mais recente:** a autora pediu deixar favela/não favela para depois. Não cobrar suas curvas ou aprofundamentos como obrigação atual. O indicador existe nos arquivos atuais, mas isso não garante qualidade/completude das rotas. A revisão das aulas, documentada no checklist, recuperou CCA (Aula 5, slides 10–12), percolação (19–20), comparação dos grupos com renda (21) e definição de manchas urbanas (5 e 17). São possibilidades a discutir, não novos métodos ou parâmetros já escolhidos.

**Seleção posterior da autora:** manter os agrupamentos por atendimento, os 16 grupos de densidade × renda, separação por densidade, mapas de renda/densidade, áreas de atendimento e Fortaleza, processamento integral em notebooks e registro. Manter o exemplo pequeno de Dijkstra e medir “muito longe” pelo **P90 ponderado pela população de cada capital**. Não desenvolver CCA, percolação, mapa separado de favela, mapa detalhado da rede, mapa de propagação de distâncias, pedestres ou p-mediana nesta versão. O artigo foi atualizado e compilado; a prioridade segue sendo compreender os notebooks e resultados. Ver o checklist para os estados atualizados; as opções antigas abaixo permanecem como histórico.

**Lacuna confirmada na retomada:** o notebook 01 recalcula apenas os 63 setores com várias partes e preserva as distâncias dos demais setores, produzidas anteriormente por `scripts/03_distancias_capital.py`. Assim, a migração do pipeline analítico completo para notebooks ainda não terminou. Também é preciso rastrear com a usuária o preparo dos dados nos scripts anteriores. Não afirmar que todo o processamento está reproduzido de ponta a ponta em notebooks só porque os ajustes finais e as figuras foram executados neles. A existência de saídas sem erros de execução não comprova correção metodológica.

---

## 1. Objetivo final

Entregar um **artigo de no máximo 3 páginas, em português**, com **pelo menos uma figura** (painéis (a), (b), (c)…). Ele deve analisar dados de cidades brasileiras com temas e técnicas do curso. As regras estão em [Manual do trabalho escrito.pdf](Manual%20do%20trabalho%20escrito.pdf), e o texto precisa responder a três perguntas:

1. **Qual é o problema?** Contexto e referências.
2. **O que foi feito?** Dados e métodos.
3. **Quais são os resultados e as conclusões?** Incluindo as limitações.

**Título (decidido):** "Escala e desigualdade espacial no acesso ao pronto-atendimento nas capitais brasileiras". Usar "pronto-atendimento" em todo o texto, não "UPA". A introdução deve definir o termo: estabelecimentos do tipo 73 do CNES (UPAs, PAs, AMA 24h, SPAs) que atendem o SUS.

**Pergunta central:**

> Os pronto-atendimentos estão bem localizados, considerando ao mesmo tempo a **densidade** de cada região e a **renda** de quem mora nela?

**"Boa localização"** tem dois critérios (planejamento, seção 2):
- **Eficiência:** a lei de densidade D ∝ ρ^α comparada com o ótimo para serviço público, α = 2/3 (Gastner & Newman).
- **Equidade:** com a mesma densidade, quem tem menor renda fica mais longe?

---

## 2. Regras que não podem ser quebradas

1. **Toda a teoria e todas as citações vêm do repositório:** as aulas (`Aula 1.pptx` a `Aula 5.pptx`) e a pasta [Bibliografia/](Bibliografia/). Não inventar referências nem métodos de fora. Só os **dados** vêm de fora (CNES, IBGE, OpenStreetMap), e isso precisa ser dito no texto.
2. **Leis de potência são o eixo do trabalho.** Cada análise termina num expoente comparado com um valor de referência. Se um teste der negativo (por exemplo, a distribuição não segue lei de potência), isso é resultado e deve ser reportado como tal.
3. **Distância = distância pela rua, calculada com Dijkstra** na rede viária de carro do OpenStreetMap. Tempo de viagem fica fora do escopo e aparece só como limitação (Maia et al. 2023).
4. **Não usar k-means, DBSCAN nem outros métodos fora do material do curso.** Os agrupamentos permitidos são as áreas de atendimento (Xu et al.), o limiar de densidade, quartis de densidade e renda, CCA e percolação (Aula 5).
5. **Não usar betweenness nem "pequeno mundo".** Não estão nas aulas.
6. Documentos de trabalho ficam em `.md` no repositório (não em páginas HTML).
7. **Todas as fases de análise devem ficar em notebooks Jupyter (`.ipynb`)**, com explicações, fórmulas, código, tabelas e gráficos visíveis. Scripts ficam para coleta de dados. Os scripts antigos de análise são histórico; novas análises e sua reprodução devem estar nos notebooks (pedido da usuária em 04/11/2026).
8. **Discutir novas decisões com a usuária antes de executá-las**, explicando os motivos e as consequências para que ela consiga apresentar o trabalho ao professor.
9. **Construir os gráficos progressivamente nos notebooks, conforme os resultados**, especialmente ao discutir área, população e densidade. Cada visualização deve explicar a pergunta, os eixos, as unidades e a interpretação, incluindo limites do que permite concluir. A escolha de apresentação não substitui a discussão prévia de decisões metodológicas (orientação da usuária em 04/11/2026).
10. **Acompanhamento da pesquisa:** explicar cada etapa antes de avançar: pergunta, vínculo com aulas/bibliografia, dados de entrada, unidade de observação, blocos do código, execução e conferências, leitura do gráfico, conclusão permitida e limitações. Distinguir exigências explícitas do manual, escolhas do plano e interpretações do agente. A prioridade é a compreensão da autora; um PDF compilado não encerra o trabalho de pesquisa.

---

## 3. Decisões tomadas

| Tema | Decisão | Motivo |
|---|---|---|
| Recorte | As **27 capitais**. A lei de escala L1 usa **26**, porque Aracaju tem 0 unidades do tipo 73 | Aracaju cadastra suas urgências como hospital (tipo 5) |
| O que conta como "UPA" | **Todo estabelecimento ativo do tipo 73 do CNES** ("Pronto Atendimento"): UPA, PA, AMA 24h, SPA etc. São **274** nas capitais | Só "UPA" no nome deixava Manaus, Vitória e Porto Alegre quase sem unidades |
| Versão principal × robustez | **Principal = só SUS** (245 unidades; arquivos `_drive_sus_*`, flag `--so-sus`). Robustez = todos os 274 tipo 73 (arquivos `_drive_*`) | A pergunta é sobre serviço público; os PAs privados distorcem em algumas capitais (em Fortaleza, o único privado fica na Aldeota) |
| L1 (lei de escala) | Usar a contagem de PAs **do SUS** por capital (`n_pa_sus` em `capitais_resumo.csv`); repetir com `n_pa` como robustez | Coerência com a versão principal. A prévia β = 0,88 foi feita com `n_pa` e precisa ser refeita |
| Unidade espacial | **Setor censitário do Censo 2022** (~500 moradores em média) | Traz população, área, renda e favela |
| Renda | **Renda média do responsável (V06004)** | A mediana (V06006) fica travada em R$ 1.212 (salário mínimo) em 17% dos setores |
| Urbano/rural | Substituído por **quartis de densidade** e **favela** (`CD_TIPO = 1`) | Dentro das capitais, a população rural é no máximo 7,4% |
| Quartis | Calculados **dentro de cada capital** | Os níveis de renda e densidade variam muito entre capitais |
| Rede viária | Rede **para carro** (`drive`), dirigida, com faixa de 5 km além do limite municipal | Urgência não se faz a pé; mão única importa |
| Fonte da rede | Extratos regionais do **Geofabrik** (`dados/osm/pbf/`), recortados com `pyosmium` | O servidor Overpass estava sobrecarregado |
| Coordenadas | Conferidas e corrigidas (script 07). Usar sempre `pa_capitais_corrigido.csv` | 41 de 274 estavam erradas |
| Setores excluídos | Setores com ligação à rua **> 2 km** | São ilhas e áreas ribeirinhas; até 4,4% da população (Porto Velho) |
| Figura principal | Painéis (a)–(e) (seção 7.5 deste plano); o mapa do painel (a) é de **Fortaleza** | Já validada na exploração |
| Formato do texto | **LaTeX** (pasta `artigo/`) | Decisão da usuária |

---

## 4. Dados (todos em `dados/`)

| Arquivo | Conteúdo |
|---|---|
| `dados/cnes/cnes_estabelecimentos.csv` | CNES nacional (OpenDataSUS, 24/10/2026), `;`, latin1 |
| `dados/ibge/pop2022.json` | População municipal do Censo 2022 (agregado 4709) |
| `dados/ibge/censo2022/BR_setores_CD2022.csv` | Atributos dos setores (população `v0001`, área, situação, tipo, bairro) |
| `dados/ibge/censo2022/Agregados_por_setores_renda_responsavel_BR.csv` | Renda por setor (publicada em 08/05/2026) |
| `dados/ibge/setores_gpkg/<UF>_setores_CD2022.gpkg` | Polígonos dos setores, um arquivo por UF (EPSG:4674) |
| `dados/osm/pbf/*.osm.pbf` | Extratos do OpenStreetMap por região |
| `dados/osm/<capital>_drive.graphml` | Rede viária já recortada de cada capital (cache) |
| `dados/correcoes_manuais.csv` | Correções manuais de coordenadas (`CO_CNES,lat,lon,nota`); vazio |

**Saídas processadas (`dados/processados/`):**

| Arquivo | Conteúdo |
|---|---|
| `capitais_resumo.csv` | Uma linha por capital: população, nº de PAs (total, SUS, 24h) |
| `pa_capitais_corrigido.csv` | Os 274 PAs com coordenadas corrigidas, `status` e `metodo` da correção |
| `conferencia_coordenadas.csv` | Diagnóstico de cada coordenada, com links de mapa |
| `setores_capitais.csv` | 92.494 setores habitados: população, área, densidade, renda média e mediana, favela |
| `distancias/<capital>_drive[_sus]_setores.csv` | Por setor: `d_m` (distância pela rua até o PA mais próximo), `CO_CNES` do PA, `ligacao_m`, `euclid_m`, população, renda, densidade, favela |
| `distancias/<capital>_drive[_sus]_comunidades.csv` | Por PA (área de atendimento): área, população, renda média ponderada, `D`, `rho` |
| `resumo_distancias_capitais.csv` | Por capital: distância média, Gini, distância do Q1 e do Q4 de renda, favela |
| `corrigidos/distancias/<capital>_drive[_sus]_setores.csv` | Versão corrigida: um código por setor, população e área oficial uma vez; pontos e rotas recalculados para os setores com várias partes. Usar nas próximas análises |
| `corrigidos/grupos_unidades.csv` | Nó de atendimento representado por um código CNES, códigos de todas as unidades do grupo e multiplicidade `n_unidades` |
| `corrigidos/auditoria_*.csv`, `resumo_correcao.csv`, `manifesto_entradas.csv` | Dentro de `corrigidos/`: mudanças por setor/capital, fechamento dos totais e hashes que conferem a preservação dos originais |
| `analises/L2/areas_sus.csv`, `areas_todos.csv` | Áreas de atendimento após a correção e o filtro, multiplicidade, densidades, renda ponderada, cobertura da renda e resíduos da L2 |
| `analises/L2/resultados_L2.csv`, `bootstrap_*.csv` | Expoentes, IC 95%, R² e as 2.000 reamostragens de cada versão |

---

## 5. Pipeline e como rodar

**Atualização de 04/11/2026:** a lista de scripts abaixo registra o pipeline anterior. A continuação das análises será feita em `notebooks/`. O primeiro notebook é `notebooks/00_conferencia_dados.ipynb`, que audita os arquivos existentes antes de L2. Não executar os scripts antigos de análise como substitutos dos notebooks. A migração das demais etapas será acompanhada fase a fase com a usuária.

**Ordem atual dos notebooks, já executados:** 00 (conferência) → 01 (correção) → 02 (L2) → 03 (renda) → 04 (distâncias, curvas L3 e Gini) → 05 (L1) → 06 (figura) → 07 (artigo). Ver `notebooks/README.md` para os links. Explicações e resultados ficam salvos em cada um; selecionar o Python da `.venv` para reexecutar. Distâncias, renda e Gini foram refeitos com os dados corrigidos. Os dados e as figuras antigas foram preservados como histórico. A usuária aprovou L3 descritiva e informou autoria/afiliação: **Lia Sucupira — Universidade de Fortaleza**. Essas respostas estão registradas no notebook 07 e no artigo compilado.

Ambiente: `.venv/` (Python 3.12; ver [requirements.txt](requirements.txt): osmnx 2.0.6, geopandas 1.1.1, osmium 4.3.2, scipy, matplotlib).

```bash
cd /home/liasucf/ciencia-de-cidades
.venv/bin/python scripts/01_upas_capitais.py          # PAs por capital
.venv/bin/python scripts/02_setores_capitais.py       # tabela de setores
.venv/bin/python scripts/07_conferir_coordenadas.py   # confere/corrige coordenadas (usa Nominatim com cache)
bash scripts/08_todas_capitais.sh                     # Dijkstra nas 26 capitais, todos e só SUS (lento na 1ª vez, quando recorta as redes)
cd scripts && ../.venv/bin/python 09_resumo_capitais.py && cd ..   # resumo + figuras 13 e 14
.venv/bin/python scripts/04_exploracao.py             # figuras exploratórias 01–08
cd scripts && ../.venv/bin/python 06_figuras_rede.py "Fortaleza - CE" && cd ..   # figuras 10–12
```

**Cuidados:**
- Os scripts 05, 06 e 09 importam `03_distancias_capital` com `import_module`, então precisam rodar **de dentro de `scripts/`**.
- O estilo das figuras (cores, fontes) está em `scripts/estilo.py`. Reutilizar.
- O script 07 consulta o Nominatim a 1 requisição por segundo, com cache em `dados/processados/geocodificacao_cache.json`. Não apagar o cache.
- O Dijkstra usa a matriz do grafo **invertido** (`grafo_para_matriz_invertida`) e `scipy.sparse.csgraph.dijkstra` com `min_only=True` a partir de todos os PAs: a distância é da casa até o PA.
- Ao ler os CSVs de distância, **excluir setores com `ligacao_m > 2000`** e `populacao == 0`, como faz `09_resumo_capitais.py`. Os CSVs `_comunidades.csv` **não** têm essa exclusão: recalcular as áreas de atendimento a partir dos `_setores.csv`.
- **Usar os CSVs em `dados/processados/corrigidos/distancias/`**, com população positiva, ligação ≤ 2.000 m e distância finita. Nos arquivos originais, 63 setores aparecem em várias linhas, repetindo os totais oficiais. Foram unidos no notebook 01. O grupo compartilhado de Porto Alegre conta duas unidades na versão com todos: usar `D = n_unidades / area_km2`.

---

## 6. O que já está pronto (resultados preliminares)

- **Correção e L2 concluídas em 04/11/2026:** 63 setores com várias partes corrigidos em 13 capitais; 92.782 códigos nos arquivos das 26 capitais, 90.985 setores após o filtro, 45.770.048 moradores. Originais preservados e conferidos por hash. **L2 SUS:** α = **0,860**, IC 95% **0,794–0,934** (245 áreas, 245 estabelecimentos). **Todos:** α = **0,881**, IC 95% **0,810–0,960** (273 áreas, 274 estabelecimentos). OLS log-log, 2.000 reamostragens por área, semente 42. Ambos os intervalos ficam acima de 2/3 e abaixo de 1, sob as hipóteses desse bootstrap. Não comprova eficiência/ineficiência nem responde ainda sobre renda. Ver notebook 02.
- **Renda, modelo conjunto simples escolhido pela usuária:** SUS, **δ = −0,195**, IC 95% **−0,354 a −0,027**; todos, **δ = 0,031**, IC 95% **−0,121 a 0,190**. No SUS, associação no sentido compensatório considerando a densidade; com todos, o intervalo inclui zero. O modelo mistura diferenças dentro e entre capitais e não identifica causalidade. Ver notebook 03.
- **L1 final:** SUS, **β = 0,870**, IC 95% **0,693–1,021**; todos, **β = 0,883**, IC 95% **0,695–1,051**. São 26 capitais; Aracaju sai por zero unidades do recorte. Os intervalos incluem 1. Ver notebook 05.
- **Distâncias, Gini e quartis refeitos com os setores corrigidos:** em 12 de 26 capitais, Q1 de renda tem distância média menor que Q4; em 18 de 26, setores de favela têm média menor que os demais. Na menor densidade, a distância relativa é **1,721** para Q1 de renda e **1,215** para Q4. Os quartis são por capital e os resumos são ponderados pela população. Ver notebook 04 e `analises/distancias/`.
- **L3 descritiva aprovada:** curvas das 26 capitais e curvas relativas por renda, com Gini. Nenhum `x_min` foi escolhido e γ não foi estimado. A visualização não é uma rejeição estatística de lei de potência. A usuária confirmou essa abordagem em 04/11/2026.
- **Figura e artigo:** notebooks 06 e 07 geram a figura de quatro painéis (PDF vetorial e PNG) e o artigo LaTeX de até 3 páginas, com referências locais. A autoria/afiliação foi confirmada: **Lia Sucupira — Universidade de Fortaleza**. Não há pendências de preenchimento ou de tratamento da L3; o PDF local está preparado para a revisão da autora antes da entrega.
- As 14 figuras antigas em `figuras/exploracao/` e [exploracao.md](exploracao.md) permanecem como histórico anterior à correção. Os notebooks atuais são a referência para os resultados.

---

## 7. O que falta, em ordem

### 7.1 L2: lei de densidade nas áreas de atendimento — concluída
- Notebook: `notebooks/02_L2_densidade.ipynb`, após a correção feita no notebook 01. Figuras em `figuras/L2/` (PNG e PDF).
- Para cada grupo de atendimento j, somar sobre os setores válidos corrigidos: área A_j, população P_j e renda média ponderada pela população r̄_j. Aplicar população > 0, ligação ≤ 2.000 m e distância finita.
- D_j = m_j/A_j, ρ_j = P_j/A_j, com m_j igual ao número de unidades no nó (alternativa A aprovada). Ajustar log D = c + α log ρ com as 245 áreas SUS ou 273 áreas com todos, das 26 capitais (OLS + IC por bootstrap).
- Comparar α com **2/3** (ótimo público; Gastner & Newman; Um et al., Aula 4, slide 44) e com **1** (padrão comercial).
- **Critério cumprido:** α com IC 95% para "só SUS" (principal) e para "todos" (robustez). Resultados na seção 6. A análise de renda também foi concluída segundo a escolha registrada em 7.2.

### 7.2 Resíduos contra a renda — concluída no modelo simples aprovado
- Resíduo ξ_j = log D_j − (ĉ + α̂ log ρ_j). ξ < 0 significa menos PAs do que a densidade prevê.
- Regressão log D = c + α log ρ + δ log r̄ com IC de δ por bootstrap. δ < 0 indica associação no sentido compensatório; δ > 0 indica maior oferta relativa em áreas de maior renda. Um intervalo que inclui zero não prova ausência de desigualdade ou ausência de efeito.
- Efeitos fixos por capital e renda relativa foram discutidos como opções e não adotados nesta etapa por escolha da usuária.
- **Escolha da usuária em 04/11/2026:** por enquanto fazer somente o modelo conjunto `log D = c + α log ρ + δ log renda`, sem efeitos fixos ou renda relativa à capital, priorizando a simplicidade e o limite de três páginas. Comparar SUS e todos e registrar que o ajuste mistura diferenças dentro e entre capitais. Não acrescentar outra especificação sem discutir com a usuária.
- Base teórica: os SAMIs de Bettencourt (*Introduction to Urban Science*, pp. 127–143).
- **Critério cumprido:** δ com IC e interpretação nas duas versões, em `notebooks/03_renda_residuos.ipynb`, com gráficos e saídas em `analises/renda/` e `figuras/renda/`.

### 7.3 L3: curvas e Gini concluídos; apresentação descritiva aprovada
- Distribuição acumulada complementar P(d ≥ x) ponderada pela população, por capital e juntando todas as capitais com a distância normalizada pela média da capital.
- Notebook: `notebooks/04_distancias_L3.ipynb`. Curvas por capital e renda, Gini e tabela densidade × renda refeitos com os setores corrigidos; saídas em `analises/distancias/` e `figuras/distancias/`.
- A usuária aprovou apresentar curvas e Gini sem ajustar γ, mantendo o escopo simples. Não declarar rejeição estatística de lei de potência pela inspeção visual.
- Caso a usuária queira discutir uma cauda, o estimador previsto é o de Newman: γ = 1 + n[Σ ln(x_i/x_min)]⁻¹, σ = (γ−1)/√n, com **n = número de setores**, não de pessoas. Será necessário discutir `x_min` e explicar a distinção entre curva ponderada pela população e amostra de setores; nenhuma dessas escolhas foi feita.

### 7.4 L1 final — concluída
- Notebook: `notebooks/05_L1_escala.ipynb`, OLS + 2.000 reamostragens bootstrap das capitais, semente 42, com `n_pa_sus` e `n_pa`. As contagens foram conferidas contra o cadastro. Aracaju é a única exclusão por zero nas duas versões. Resultados na seção 6; saídas em `analises/L1/` e `figuras/L1/`.
- Opcional: repetir usando a "concentração urbana" do IBGE (`NM_CONCURB`) no lugar do limite municipal (Arcaute et al. 2015).

### 7.5 Figura final (em notebook, com saídas em `figuras/final/`)

Gerada em `notebooks/06_figura_final.ipynb`: `figuras/final/figura_principal.pdf` e `.png`. A composição foi revisada para impressão. O painel (d) é descritivo, conforme a decisão aprovada pela usuária.

| Painel | Conteúdo |
|---|---|
| (a) | Mapa de **Fortaleza**: os 12 PAs do SUS, áreas de atendimento, setores coloridos pelo tipo densidade × renda, favelas |
| (b) | L1: 26 capitais, reta ajustada com β, banda de bootstrap, referência β = 1 |
| (c) | L2: áreas de atendimento coloridas pelo quartil de renda, reta com α, referências 2/3 e 1 |
| (d) | L3: curva observada da distância relativa por renda; descrição sem ajuste de potência, aprovada pela usuária |
| (e) | Mapa de calor densidade × renda (26 capitais) |

Precisa caber em ~0,8 página e ser legível impresso. Usar `scripts/estilo.py`. Salvar em **PDF** (vetorial, para o LaTeX) e em PNG.

### 7.6 Texto (≤ 3 páginas, em LaTeX)
- Artigo gerado e compilado por `notebooks/07_artigo.ipynb`, em `artigo/artigo.tex`, `referencias.bib` e `artigo.pdf`, com autoria **Lia Sucupira — Universidade de Fortaleza** e L3 descritiva aprovada. A geração incorpora os resultados dos CSVs e a figura vetorial. O notebook verifica limite de 3 páginas, referências resolvidas e caixas largas; `artigo/verificacao.json` registra os resultados. Configurações e texto estão no notebook 07; não há campos ou decisões pendentes no PDF.
- Pasta `artigo/`: `artigo.tex`, `referencias.bib` e a figura incluída de `../figuras/final/`. Compilar com `pdflatex` + `bibtex` (ou `latexmk -pdf`) e conferir que o PDF tem **no máximo 3 páginas**.
- Antes de começar, verificar se há LaTeX instalado (`which pdflatex latexmk`). Se não houver, perguntar à usuária antes de instalar.
- Português: `\usepackage[brazil]{babel}`, `\usepackage[utf8]{inputenc}`, `\usepackage[T1]{fontenc}`. Margens e fonte devem seguir o que o manual não proíbe; ele só limita a 3 páginas.
- Seguir a divisão do planejamento, seção 11: problema (~0,6 pág), métodos (~0,8), figura (~0,8), resultados e conclusões (~0,8).
- **Limitações obrigatórias** (planejamento, seção 13):
  - só 26 pontos em L1;
  - tipo 73 heterogêneo;
  - coordenadas corrigidas;
  - distância ≠ tempo;
  - capital ≠ região metropolitana e efeito de borda;
  - setor reduzido a um ponto;
  - capacidade ignorada;
  - mapeamento do OSM nas favelas;
  - renda como indicador de necessidade;
  - acesso desigual a carro.
- Referências: só as da lista no fim do [planejamento.md](planejamento.md).

### 7.7 Opcionais (só se sobrar espaço/tempo)
- Robustez com a rede de pedestres (`--rede walk` no script 03).
- Comparação com a distribuição ótima (p-mediana, Xu et al.; planejamento, seção 6.3).
- Revisar à mão as 20 coordenadas com `metodo = revisar_manual` em `conferencia_coordenadas.csv`.

---

## 8. Decisões da usuária (fechadas em 04/11/2026)

1. **Termo:** "pronto-atendimento" no título e no texto, não "UPA".
2. **Versão principal:** **só SUS**. "Todos os PAs" vira teste de robustez.
3. **Formato do texto final:** **LaTeX**.
4. **Capital do painel (a):** **Fortaleza**.
5. **Análises:** todas em notebooks Jupyter, com explicações e resultados salvos; scripts apenas para coleta de dados. A usuária acompanha e decide antes de novas escolhas metodológicas.
6. **L2:** autorizadas 2.000 reamostragens bootstrap das áreas de atendimento, seguindo a prévia. A conferência dos dados antecede o ajuste.
7. **Ambiente:** autorizada a instalação de `ipykernel`, `nbformat` e `nbclient` na `.venv` do projeto para executar e salvar os notebooks.
8. **Setores com várias partes:** autorizada a união dos polígonos por código de setor, contando população e área oficial uma única vez e recalculando a distância pelo ponto representativo da geometria unida. Salvar resultados corrigidos separados dos originais.
9. **Unidades no mesmo nó (alternativa A):** autorizada uma área compartilhada, com densidade de estabelecimentos $D=m/A$, onde $m$ é o número de unidades representadas no nó. Em Porto Alegre, a versão com todos conta os dois estabelecimentos de Bom Jesus na mesma área; na versão SUS apenas um deles entra segundo o cadastro. Manter os códigos das duas unidades no registro do grupo, sem duplicar população ou área.
10. **Renda:** autorizada somente a opção 1, modelo conjunto com densidade e renda, por enquanto. Priorizar simplicidade pelo limite de três páginas. Efeitos fixos por capital e renda relativa à capital não serão implementados nesta etapa; diferenças entre capitais serão uma limitação. Manter SUS como principal, todos como robustez e 2.000 reamostragens das áreas por bootstrap.
11. **L3:** aprovada a apresentação descritiva pelas curvas e pelo Gini, sem estimar γ, selecionar `x_min` ou afirmar rejeição estatística de lei de potência (04/11/2026).
12. **Autoria/afiliação:** **Lia Sucupira — Universidade de Fortaleza**, conforme informado pela usuária em 04/11/2026.

**Conferência:** foram detectados códigos de setor em múltiplas linhas da malha e dos CSVs de distância. O mesmo total de população e área é repetido por parte geométrica. Há também dois estabelecimentos de Porto Alegre ligados ao mesmo nó da rede; o script anterior mantém o primeiro como fonte. Os tratamentos foram autorizados nos itens 8 e 9 acima. Ver `notebooks/00_conferencia_dados.ipynb`.

**Discussão e autorização em 04/11/2026:** após pedir explicações, a usuária escolheu a alternativa A para Porto Alegre e confirmou a correção dos setores. As seções 8 e 9 do notebook de conferência mostram um exemplo real de Belo Horizonte (171 moradores repetidos em duas linhas, totalizando 342 na soma), o mapa das unidades de Porto Alegre (coordenadas separadas por cerca de 126 m) e as alternativas discutidas. A correção foi concluída em `notebooks/01_correcao_setores.ipynb` e o ajuste em `notebooks/02_L2_densidade.ipynb`, ambos executados e validados. Para a renda, a usuária escolheu o modelo conjunto simples (item 10), sem ajustes específicos por capital nesta etapa.


## Atualização metodológica e resultados — 04/11/2026

**Decisão da autora:** calcular o atendimento mais acessível pela menor soma total: ligação do setor à rua + rota dirigida pela rede + ligação da unidade à rua. O notebook `notebooks/retomada/03_distancias_completas.ipynb` implementa cada unidade como fonte auxiliar com o seu custo de ligação. Todas as 52 tabelas de distância foram recalculadas; a regra anterior foi preservada como comparação, não como fonte dos resultados atuais. Em 389 setores SUS (179.670 moradores) e 405 Todos (194.163 moradores), a distância caiu mais de 1 m; máximo de 5,13 km em Salvador. Os grupos de moradores se sobrepõem entre versões.

**Exceção autorizada pela autora:** o PA Ilha de Maré (Salvador, versão Todos) está no cadastro, mas seu grupo não tem área válida após o filtro aprovado de ligação setor–rua de até 2 km. Dois setores, com 1.178 moradores, foram associados a ele e têm ligações de 4.904 e 6.136 m; a ligação da própria unidade ao componente viário considerado mede 5.166 m. A autora autorizou manter a unidade no cadastro/contagem municipal e excluí-la apenas dos ajustes baseados em áreas que exigem setores válidos. O diagnóstico está em `notebooks/retomada/05_diagnostico_areas_sem_setores.ipynb`.

**L2 atualizada:** SUS α=0,861, IC95% [0,797; 0,935], 245 áreas/245 unidades; Todos α=0,899, IC95% [0,834; 0,973], 272 áreas/273 unidades representadas. Ambos os intervalos ficam acima de 2/3 e abaixo de 1; isso compara o ajuste observado com uma referência teórica, sem demonstrar eficiência ou ineficiência.

**Renda atualizada:** δ SUS=−0,196, IC95% [−0,353; −0,029]; δ Todos=0,029, IC95% [−0,122; 0,188]. O modelo mistura variação dentro e entre capitais e não indica causalidade. L3, mapas, síntese e artigo foram refeitos. O PDF do artigo tem 2 páginas, referências resolvidas e sem avisos de caixas largas; a inspeção visual foi feita. A autora ainda precisa revisar a interpretação junto ao agente antes de entregar.
