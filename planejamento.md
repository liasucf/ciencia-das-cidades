# Planejamento do trabalho final

**Tema:** Escala e desigualdade espacial no acesso ao pronto-atendimento nas capitais brasileiras

Disciplina: Ciência de Dados Aplicada à Ciência de Cidades (PPGIA). Formato exigido pelo [Manual do trabalho escrito](Manual%20do%20trabalho%20escrito.pdf): no máximo 3 páginas, ao menos uma figura, respondendo "qual é o problema", "o que foi feito" e "quais são os resultados e conclusões" (com limitações).

Regra do trabalho: toda a teoria vem das aulas (`Aula 1–5.pptx`) e da pasta [Bibliografia](Bibliografia/). Só os dados vêm de fora (CNES, IBGE, OpenStreetMap).

**Forma de trabalho (04/11/2026):** todas as fases de análise devem ser feitas em notebooks Jupyter (`notebooks/`), com explicações, código e resultados visíveis. Scripts ficam para coleta de dados. Novas decisões metodológicas devem ser discutidas com a autora antes de serem executadas. Os scripts de análise existentes são mantidos como histórico.

**Atualização da retomada:** a autora pediu adiar o aprofundamento de favela/não favela e revisar as ideias dos slides, especialmente agrupamentos e mapas. As menções a favela adiante registram o planejamento e os resultados anteriores; não representam uma obrigação de desenvolver essa comparação agora. Ver [CHECKLIST_PESQUISA.md](CHECKLIST_PESQUISA.md) para o estado atual e a revisão dos slides.

---

## 1. Pergunta central

> Os pronto-atendimentos estão bem localizados, considerando ao mesmo tempo a **densidade** de cada região e a **renda** de quem mora nela?

Perguntas derivadas:

1. **Escala:** o número de pronto-atendimentos de uma capital cresce na mesma proporção da sua população? (L1)
2. **Densidade:** dentro das capitais, as unidades se distribuem como prevê a lei ótima para serviços públicos? (L2)
3. **Densidade e renda:** depois de levar a densidade em conta, quem tem menor renda fica mais longe? (seção 6, o centro do trabalho)
4. **Distribuição:** como se distribui a distância até a unidade mais próxima, e a cauda (quem mora muito longe) é diferente para os mais pobres? (L3)

"UPA" no título original passa a significar **todo pronto-atendimento** (tipo 73 do CNES), que inclui UPAs, PAs, AMA 24h e SPAs. O texto deve deixar essa definição clara logo na introdução.

---

## 2. O que é uma "boa localização"

Precisamos definir isso antes de medir. Usamos dois critérios, ambos com base na bibliografia:

| Critério | Pergunta | Como se mede | Base |
|---|---|---|---|
| **Eficiência** | As unidades estão onde minimizam a distância média da população? | Expoente α de $D \propto \rho^\alpha$ comparado com 2/3. Opcional: razão entre a distância real e a ótima | Gastner & Newman 2006; Um et al. 2009 (Aula 4, slide 44); Xu et al. 2020 |
| **Equidade** | Quem tem menor renda fica mais longe, mesmo em regiões igualmente densas? | Distância por densidade × renda (6.1); resíduos da lei de densidade contra a renda (6.2) | Xu et al. 2020 (Gini, relação com a riqueza); Bruno et al. 2024 (desigualdade de acesso) |

Uma localização é "boa" se for eficiente **e** se a distância não piorar sistematicamente para os mais pobres. As duas coisas podem divergir: uma distribuição pode ser eficiente na média e ainda assim deixar bairros pobres e densos longe das unidades.

---

## 3. Visão geral da análise

| Etapa | Escala | Entrada | Saída | Painel |
|---|---|---|---|---|
| L1: lei de escala | Entre capitais (26 pontos) | Nº de unidades e população | β | (b) |
| Dijkstra | Dentro de cada capital | Rede viária, unidades, setores | Distância por setor e área de atendimento de cada unidade | (a) |
| L2: lei de densidade | 245 áreas SUS; 273 com todos (274 estabelecimentos) | Área, população e número de unidades do grupo | α e resíduos | (c) |
| Densidade × renda | Setores (~92 mil) | Distância, densidade, renda | Tabela 4×4 de distância relativa | (e) |
| L3: distribuição | Setores | Distância ponderada pela população | γ e Gini, por grupo de renda | (d) |

---

## 4. L1: lei de escala entre capitais

$$\text{PA}_i = A \cdot P_i^{\beta} \quad\Longrightarrow\quad \log \text{PA}_i = \log A + \beta \log P_i$$

- **Leitura:** β = 1, o número de unidades cresce na mesma proporção da população. β < 1 (sublinear), capitais maiores têm menos unidades por habitante. β > 1 (superlinear), têm mais.
- **Método:** OLS em log-log, com intervalo de confiança de β por bootstrap (reamostrar as capitais com reposição, como Melo et al. 2014). O Nadaraya-Watson que eles usam não faz sentido com tão poucos pontos.
- **Dados:** contagens de 1 (Boa Vista) a 64 (São Paulo). População de 302.692 (Palmas) a 11.451.999 (São Paulo), cerca de 1,6 década, Censo 2022.
- **Aracaju sai do ajuste** (zero unidades do tipo 73; ver limitações), então o ajuste usa **26 capitais**.
- **Cuidado:** com 26 pontos, o intervalo de β será largo. O texto deve mostrar o intervalo, e não só o valor pontual.
- **Extensão opcional:** repetir L1 usando a "concentração urbana" do IBGE no lugar do limite municipal. Arcaute et al. 2015 e a Aula 5 (slide 18) mostram que β muda com a definição de cidade.
- **Base:** Bettencourt et al. 2007 (Aula 4, slide 22; Aula 5, slide 15); Melo et al. 2014.

---

## 5. Distância com Dijkstra

Usamos a distância **pela rua**, não a linha reta. Xu et al. 2020 mostram que a distância euclidiana subestima o custo real dentro da cidade. O tempo de viagem fica de fora, porque Maia et al. 2023 mostram que distância e tempo não são proporcionais na rede viária.

### Entradas

| Objeto | Fonte | Quantidade nas capitais |
|---|---|---|
| Pronto-atendimentos (pontos) | CNES, latitude e longitude | 274 |
| Setores censitários (polígonos) | IBGE, malha de setores 2022 por UF | 92.494 habitados |
| Malha viária (grafo) | OpenStreetMap, rede para carro | uma por capital |

**Que rede é essa:** todas as ruas e estradas por onde passa carro (rodovias, avenidas, ruas de bairro e residenciais), com comprimento e sentido. É o `network_type="drive"` do `osmnx`. **Não é a rede de ônibus.** Escolhemos essa porque o deslocamento até uma urgência é feito de carro, táxi, aplicativo ou ambulância, e porque é a mesma base de Xu et al. e Maia et al. A rede de ônibus exigiria tempo, espera e baldeação (fora do escopo) e dados GTFS, que não existem de forma padronizada nas 27 capitais.

**Teste de robustez:** repetir com a rede de pedestres (`network_type="walk"`, que inclui vielas e ignora mão única) e verificar se a conclusão sobre renda se mantém.

### Passo a passo (para cada capital)

1. **Limite:** união dos setores da capital, ampliada por uma faixa de 5 km, para que rotas que passam pelo município vizinho não sejam cortadas.
2. **Grafo:** rede viária do OSM para carro, dentro desse limite. Nós são interseções e arestas são trechos de rua, com peso igual ao comprimento em metros. A rede é dirigida, por causa das ruas de mão única.
3. **Inverter o grafo:** rodar o Dijkstra a partir das unidades no grafo com as setas invertidas dá a distância **da casa até a unidade**, respeitando as mãos de direção.
4. **Ligar os pontos à rede:** cada unidade e cada setor (pelo seu ponto representativo, que sempre cai dentro do polígono) é ligado ao nó mais próximo. Guardar essa distância de ligação e marcar ligações acima de 500 m para conferência.
5. **Dijkstra multi-fonte:** uma única execução, partindo de todas as unidades ao mesmo tempo, devolve para cada nó a menor distância e qual unidade é a mais próxima.
6. **Distância do setor:** $d_i$ = distância do nó + ligação do setor + ligação da unidade.
7. **Áreas de atendimento:** setores com a mesma unidade mais próxima formam a área de atendimento dela (as "comunidades de serviço" de Xu et al.). Área $A_j$, população $P_j$ e renda média $\bar r_j$ (média dos setores ponderada pela população) são somadas sobre esses setores.

### Conferências

- A distância de rede deve ser maior ou igual à distância em linha reta em todos os setores. Se não for, há erro na ligação à rede.
- Setores em ilhas sem ligação viária (Belém, Salvador) ficam com distância infinita: contar as pessoas, reportar e excluir.
- No mapa de uma capital, as áreas de atendimento devem formar manchas contíguas em volta de cada unidade.

**Ferramentas:** Python com `osmnx`, `networkx`, `geopandas` e a implementação de Dijkstra em `scipy.sparse.csgraph` no grafo invertido. Toda a continuação das análises e as correções estão em notebooks.

---

## 6. A localização é boa? Densidade e renda juntas

Esta é a seção que responde à pergunta central. São três níveis, do mais simples ao mais exigente. Os níveis 6.1 e 6.2 são obrigatórios; o 6.3 é opcional.

### 6.1 Nível do setor: tabela densidade × renda

Pergunta: em regiões **igualmente densas**, os setores mais pobres ficam mais longe?

1. Em cada capital, dividir os setores em **quartis de densidade** e **quartis de renda média**. Os quartis são calculados dentro de cada capital, porque renda e densidade têm níveis muito diferentes entre as capitais.
2. Normalizar a distância pela média da própria capital: $\tilde d_i = d_i / \bar L_{\text{capital}}$, com $\bar L = \sum p_i d_i / \sum p_i$. Assim, $\tilde d = 1$ é "a média da sua cidade", e as capitais podem ser juntadas.
3. Montar uma tabela 4 × 4 (densidade × renda) com a distância relativa média ponderada pela população em cada célula, juntando as 27 capitais. Mostrar também a fração da população de cada célula que está na cauda da distribuição de distância ($d_i \ge x_{\min}$ de L3).

| | Renda Q1 (menor) | Q2 | Q3 | Q4 (maior) |
|---|---|---|---|---|
| **Densidade Q4 (maior)** | $\tilde d$ | | | |
| **Densidade Q3** | | | | |
| **Densidade Q2** | | | | |
| **Densidade Q1 (menor)** | | | | |

**Como ler:**
- Variação só **vertical** (a distância cai com a densidade, sem diferença entre as colunas de renda): as unidades seguem a população, e a renda não pesa. Isso indica equidade.
- Variação **horizontal** dentro da mesma linha (Q1 de renda mais longe que Q4, com a mesma densidade): sinal de desigualdade por renda.
- A célula "denso e pobre" (Densidade Q4 × Renda Q1) é a mais importante: é onde há mais pessoas com menos alternativas, como carro próprio ou plano de saúde.

Esta tabela também é a **tipologia de setores** que discutimos (seção 8): cada célula é um tipo de área.

### 6.2 Nível da área de atendimento: resíduos da lei de densidade

Pergunta: depois de descontar o efeito da densidade, a renda explica onde há unidades de menos?

1. Ajustar L2 com as áreas de atendimento dos setores corrigidos: 245 na versão SUS e 273 na versão com todos. As 273 áreas representam 274 estabelecimentos, porque as duas unidades de Bom Jesus ligadas ao mesmo nó compartilham uma área (alternativa A aprovada pela autora em 04/11/2026). Para cada grupo, $m_j$ conta seus estabelecimentos:

$$D_j = \frac{m_j}{A_j}, \qquad \rho_j = \frac{P_j}{A_j}, \qquad \log D_j = c + \alpha \log \rho_j$$

   - Nas demais áreas, $m_j=1$, recuperando $D_j=1/A_j$. População e área nunca são duplicadas para contar dois estabelecimentos. Os setores com várias partes geométricas foram unidos e têm uma observação por código, com população e área oficial uma única vez. Ver `notebooks/01_correcao_setores.ipynb`.
   - **Resultado concluído (04/11/2026):** SUS, α = 0,860, IC 95% 0,794–0,934; todos, α = 0,881, IC 95% 0,810–0,960. OLS log-log, 2.000 reamostragens das áreas, semente 42. Ambos os intervalos ficam acima de 2/3 e abaixo de 1, sob as hipóteses do procedimento. Não constitui comprovação de eficiência ou causalidade. Ver `notebooks/02_L2_densidade.ipynb`.

   - **Referência:** α = 2/3 é o ótimo para serviço público (minimiza a distância média). α ≈ 1 é o padrão de serviços com fins lucrativos (Um et al. 2009: $\rho^{1.13}$ para ambulatórios e $\rho^{0.69}$ para escolas públicas nos EUA).
2. Calcular o **resíduo** de cada área: $\xi_j = \log D_j - (\hat c + \hat\alpha \log \rho_j)$.
   - $\xi_j < 0$: a área tem **menos** unidades do que a densidade dela prevê (área grande em relação à quantidade de estabelecimentos do grupo).
   - $\xi_j > 0$: tem **mais** do que a densidade prevê.
   - É a mesma ideia dos indicadores ajustados pela escala de Bettencourt (SAMIs): medir o desvio em relação à lei em vez do valor bruto. Ver *Introduction to Urban Science*, pp. 127–143, que inclui cidades brasileiras.
3. Relacionar $\xi_j$ com a renda média da área, $\log \bar r_j$. Se as áreas mais pobres tiverem resíduos sistematicamente negativos, a localização é pior para os mais pobres, **já descontado o efeito da densidade**.
4. Forma equivalente em uma só regressão: $\log D_j = c + \alpha \log \rho_j + \delta \log \bar r_j$. Interessa o sinal de δ e o seu intervalo de confiança por bootstrap.
   - Intervalo de δ incluindo zero: não há evidência de associação diferente de zero segundo esse modelo e seu bootstrap; não comprova ausência de desigualdade.
   - δ > 0: áreas mais ricas têm mais unidades do que a densidade justifica.
   - δ < 0: a oferta é **compensatória** e favorece as áreas mais pobres.

**Escolha e resultado em 04/11/2026:** a autora preferiu somente o modelo conjunto simples, pela limitação de três páginas. Não incluímos efeitos fixos ou renda relativa à capital; o modelo mistura diferenças dentro e entre capitais e essa limitação deve acompanhar a interpretação. **SUS: δ=−0,195, IC 95% −0,354 a −0,027; todos: δ=0,031, IC 95% −0,121 a 0,190.** Foram usadas 2.000 reamostragens das áreas por versão, semente 42. Ver `notebooks/03_renda_residuos.ipynb`. A regressão conjunta exige ajustar densidade e renda simultaneamente; uma regressão do resíduo da oferta contra renda bruta não é em geral equivalente quando renda e densidade se relacionam. O gráfico do notebook retira a densidade de ambos os eixos, visualizando o mesmo δ do modelo.

**Cuidados:**
- Densidade e renda são correlacionadas (favelas são densas e pobres). Por isso o resíduo e a regressão com as duas variáveis são necessários, e a correlação simples com a renda não basta.
- $D_j$ e $\rho_j$ têm a mesma área no denominador, o que já cria alguma correlação entre os dois. O método é o de Gastner & Newman, mas isso deve ser mencionado.

### 6.3 (Opcional) Comparação com a distribuição ótima

Pergunta: quanto a distância cairia se as **mesmas** unidades fossem realocadas da melhor forma, e quem ganharia com isso?

- Xu et al. 2020 resolvem o **problema da p-mediana**: escolher N locais que minimizam a distância total ponderada pela população, com N igual ao número de unidades que já existem.
- **Índice de ganho por setor:** $r_i = d_i^{\text{real}} / d_i^{\text{ótimo}}$. $r_i > 1$ significa que o setor está pior servido do que estaria no ótimo.
- **Índice da cidade:** $R = \sum p_i d_i^{\text{ótimo}} / \sum p_i d_i^{\text{real}}$, entre 0 e 1. R = 1 significa que a distribuição real já é ótima.
- Cruzar $r_i$ com a tabela de 6.1: os setores densos e pobres são os que mais ganhariam com a realocação?
- **Custo:** é a etapa mais pesada, porque exige uma matriz de distâncias e uma heurística de otimização. Só entra se 6.1 e 6.2 ficarem prontas com folga.

---

## 7. L3: distribuição da distância

**Decisão aprovada (04/11/2026):** curvas por capital e renda, Gini e tabela densidade × renda refeitos com os dados corrigidos em `notebooks/04_distancias_L3.ipynb`. A autora confirmou manter L3 descritiva, sem escolher `x_min`, estimar γ ou afirmar rejeição estatística de potência pela visualização. As instruções de ajuste abaixo são apenas uma possibilidade para um estudo futuro, que dependeria de nova discussão; não fazem parte da versão atual.

- **Variável:** distância $d_i$ de cada setor, ponderada pela população.
- **Curva:** distribuição acumulada complementar $P(d \ge x)$ = população com $d_i \ge x$ / população total, em log-log.
- **Expoente:** estimador de máxima verossimilhança de Newman, $\gamma = 1 + n\left[\sum \ln(x_i/x_{\min})\right]^{-1}$, com erro $\sigma = (\gamma-1)/\sqrt{n}$. Aqui **n é o número de setores**, não de pessoas: contar pessoas deixaria σ artificialmente pequeno.
- Escolher $x_{\min}$ como o início do trecho em que a curva é reta em log-log (Newman, seção II).
- **Isso é um teste, não uma premissa.** Se a cauda não for lei de potência, isso é resultado e deve ser reportado.
- **Prévia em Fortaleza:** a curva em log-log mostra mudanças de inclinação e queda no extremo da amostra. Isso motiva cautela ao descrever toda a distribuição como potência, mas não constitui sozinho um teste de rejeição de uma cauda. As leis de escala ajustadas do trabalho permanecem em L1 e L2; a L3 descritiva foi aprovada pela autora.
- **Por grupo:** curvas separadas por quartil de renda e por favela/não favela.
- **Desigualdade:** Gini da distância ponderada pela população (Xu et al., Bruno et al., Ponte et al.).
- **Base:** Newman, *Power laws, Pareto distributions and Zipf's law* (eqs. 3–6); Aulas 2 e 3.

---

## 8. Clusterização

Métodos genéricos como k-means não estão no material do curso. Por isso usamos agrupamentos que o curso apresenta, mais cortes justificados nas aulas:

| Agrupamento | O que faz | Uso | Base |
|---|---|---|---|
| **Áreas de atendimento** (obrigatório) | Agrupa setores pela unidade mais próxima na rede | L2 e 6.2 | Xu et al. 2020 |
| **Tipologia densidade × renda** (obrigatório) | Células da tabela 4×4 de 6.1, com favela como destaque | 6.1 e mapa | Aula 5, slide 5; Aula 2, slide 17 |
| **Limiar de densidade** | Setores acima ou abaixo de 1.500 hab/km² | Contraste denso/não denso | Aula 5, slide 5 |
| Percolação na rede viária (opcional) | Agrupa interseções por comprimento de rua | Mancha urbana em várias escalas | Aula 5, slides 19–21 |
| CCA (opcional) | Agrupa células densas próximas | Repetir L1 com outra fronteira | Aula 5, slides 10–12; Oliveira et al. 2018 |

A tipologia **descreve, não prova**. O que dá a referência normativa é a lei (α comparado com 2/3) e o resíduo (6.2).

---

## 9. Dados

Baixados em 26/10/2026 para a pasta `dados/` (fora do repositório original).

| Variável | Fonte | Status | Situação |
|---|---|---|---|
| Pronto-atendimentos | CNES, CSV nacional do OpenDataSUS (atualizado em 24/10/2026) | ✅ baixado | 274 ativos do tipo 73 nas capitais, todos com coordenadas; 245 atendem o SUS, 236 funcionam 24h |
| População municipal | IBGE, Censo 2022 (agregado 4709) | ✅ baixado | 27 capitais |
| Setores (atributos) | IBGE, Censo 2022, malha com atributos | ✅ baixado | 92.494 setores habitados, com população, área, urbano/rural, favela e concentração urbana |
| Renda | IBGE, Censo 2022, rendimento do responsável por setor (publicado em 08/05/2026) | ✅ baixado | Média (V06004) e mediana (V06006); valor em 99% dos setores habitados |
| Setores (polígonos) | IBGE, GeoPackage por UF | ✅ baixados | Arquivos das 27 UFs; setores com várias partes corrigidos no notebook 01 |
| Malha viária | OpenStreetMap, extratos regionais do Geofabrik (o Overpass estava sobrecarregado) | ✅ baixada | Extratos das cinco regiões e redes `drive` das 26 capitais analisadas em cache |

**Observações dos dados:**
- **Renda:** usar a **média**. A mediana fica em R$ 1.212 (o salário mínimo de 2022) em 11 capitais e não separa os setores.
- **Urbano/rural do IBGE quase não varia** dentro das capitais: a população rural é no máximo 7,4% (Porto Velho) e é praticamente zero em 10 capitais. No lugar, usamos densidade e favela.
- **Favela:** de 0,9% da população (Campo Grande) a 57,2% (Belém).

**Scripts:**
- [scripts/01_upas_capitais.py](scripts/01_upas_capitais.py) gera `dados/processados/pa_capitais.csv` e `capitais_resumo.csv`.
- [scripts/02_setores_capitais.py](scripts/02_setores_capitais.py) gera `dados/processados/setores_capitais.csv` e `setores_capitais_resumo.csv`.

---

## 10. Figura planejada

Uma figura com cinco painéis:

| Painel | Conteúdo | Eixos |
|---|---|---|
| **(a)** Mapa de uma capital | Rede viária, unidades, áreas de atendimento, setores coloridos pelo tipo densidade × renda, favelas destacadas | mapa |
| **(b)** L1 | 26 capitais, ajuste com β, banda de bootstrap, reta de referência β = 1 | log P × log nº de unidades |
| **(c)** L2 | Áreas de atendimento **coloridas pelo quartil de renda**, ajuste com α, retas de referência 2/3 e 1 | log ρ × log D |
| **(d)** L3 | $P(d \ge x)$ por quartil de renda, com γ | log distância × log P(d ≥ x) |
| **(e)** Densidade × renda | Mapa de calor 4×4 da distância relativa $\tilde d$ | quartil de renda × quartil de densidade |

Os painéis (c) e (e) respondem juntos à pergunta central. Em (c), se os pontos de renda baixa ficarem sistematicamente abaixo da reta, há menos unidades do que a densidade justifica nas áreas pobres.

---

## 11. Texto em 3 páginas

| Parte | Conteúdo | Espaço |
|---|---|---|
| Qual é o problema | Acesso a urgência como serviço público; leis de escala; lei de 2/3; eficiência vs equidade; pergunta central | ~0,6 pág |
| O que foi feito | Dados; Dijkstra; áreas de atendimento; L1, L2, L3; tabela densidade × renda; resíduos | ~0,8 pág |
| Figura | Painéis (a)–(e) com legenda | ~0,8 pág |
| Resultados e conclusões | β, α, γ comparados com as referências; resposta sobre densidade e renda; limitações | ~0,8 pág |

---

## 12. Escopo

**Dentro:**
- L1, L2 e L3 (β, α, γ)
- Distância na rede viária com Dijkstra
- Áreas de atendimento e tipologia densidade × renda
- Resíduos da lei de densidade contra a renda
- Gini da distância

**Opcional:**
- Comparação com o ótimo (p-mediana, 6.3)
- L1 com concentração urbana
- Percolação ou CCA

**Fora:**
- Tempo de viagem
- Betweenness e pequeno mundo (não estão nas aulas)
- k-means e outros métodos que não estão no material
- Uso do solo como tema principal

---

## 13. Limitações já previstas

- **Só 26 pontos em L1:** o β das capitais tem incerteza grande e não deve ser apresentado como lei universal.
- **Aracaju fica fora de L1:** suas duas unidades de urgência municipais estão cadastradas no CNES como hospitais (tipo 5). É um efeito do cadastro, não ausência de atendimento.
- **O tipo 73 é heterogêneo:** inclui UPAs, AMA 24h, PAs especializados (oftalmologia, saúde mental) e 29 unidades que não atendem o SUS. Repetir as contas só com unidades do SUS. Em Fortaleza isso muda o resultado: o único PA privado fica na Aldeota e, sem ele, a distância do quartil mais rico sobe de 3,40 para 4,35 km.
- **Coordenadas erradas no CNES:** 41 das 274 unidades (15%) estavam longe do bairro do endereço, fora do município ou num ponto genérico compartilhado com outras unidades. Foram corrigidas pela busca do endereço no OpenStreetMap ou aproximadas por um ponto do bairro. Outras 20 ficaram sem confirmação.
- **Capital não é região metropolitana:** moradores de municípios vizinhos usam as unidades da capital (Aula 5, slide 7).
- **Efeito de borda:** quem mora perto do limite pode usar uma unidade do município vizinho, que não entra na conta.
- **Setor reduzido a um ponto:** todos os moradores de um setor recebem a mesma distância.
- **Capacidade ignorada:** a unidade mais próxima pode estar lotada (Xu et al. também não consideram capacidade).
- **Distância não é tempo** (Maia et al. 2023), e urgência não é deslocamento cotidiano (Hansen 1959: a sensibilidade à distância muda com o motivo da viagem).
- **Mesma distância, esforço diferente:** quem tem menos renda tem menos acesso a carro e depende mais de ônibus. A distância pela rua não capta isso (sobre a heterogeneidade das viagens de ônibus em Fortaleza, ver Ponte et al. 2018).
- **Mapeamento do OSM nas favelas:** vielas e becos costumam estar incompletos, o que aumenta a distância de ligação dos setores à rede. As ligações acima de 500 m são conferidas.
- **Renda como indicador de necessidade:** é só um indicador. Não mede saúde nem acesso a plano privado.
- **Fronteiras mudam os expoentes:** Arcaute et al. 2015; problema da unidade espacial modificável (Aula 5, slide 8).

---

## 14. Decisões

- [x] Recorte: 27 capitais (26 no ajuste de L1)
- [x] O que conta: pronto-atendimentos ativos do tipo 73. **Versão principal: só os do SUS (245)**; todos os 274 como teste de robustez (decidido em 04/11/2026)
- [x] Censo 2022, por setor censitário; renda média
- [x] Título e texto usam "pronto-atendimento", não "UPA"
- [x] Capital do mapa do painel (a): Fortaleza
- [x] Texto final em LaTeX
- [ ] Fazer ou não a comparação com o ótimo (6.3)

---

## 15. Próximos passos

- [x] Contar pronto-atendimentos por capital e verificar coordenadas
- [x] Confirmar e baixar a renda por setor do Censo 2022
- [x] Instalar `geopandas` e `osmnx` (ambiente em `.venv/`)
- [x] Rodar o Dijkstra em Fortaleza e validar (ver [exploracao.md](exploracao.md), seção 10)
- [x] Conferir as coordenadas das 274 unidades: 41 movidas, 20 a revisar à mão (ver [exploracao.md](exploracao.md), seção 11)
- [ ] Revisar à mão as 20 unidades marcadas `revisar_manual` em `dados/processados/conferencia_coordenadas.csv` (opcional)
- [x] Baixar os polígonos dos setores e os extratos do OSM de todas as regiões
- [x] Rodar o Dijkstra nas 26 capitais com unidades (todos os PAs e só SUS)
- [x] Prévia da tabela densidade × renda com as 26 capitais (ver [exploracao.md](exploracao.md), seção 12)
- [x] Ajustar L1 (β), SUS e todos, em notebook com IC 95% bootstrap
- [x] Ajustar L2 (α) com os dados corrigidos; SUS e todos, IC 95% bootstrap e gráficos explicativos em notebook
- [x] Relacionar resíduos e renda no modelo conjunto simples escolhido pela autora
- [x] Refazer a tabela densidade × renda com setores corrigidos
- [x] Curvas L3 e Gini com setores corrigidos; notebook 04
- [x] L3 descritiva aprovada pela autora; sem escolha de `x_min`, ajuste de γ ou afirmação de rejeição estatística
- [x] Gerar e revisar a figura (a)–(e) em notebook, PDF vetorial e PNG
- [x] Preparar e compilar rascunho LaTeX com até 3 páginas, a partir do notebook 07
- [x] Preencher autoria/afiliação (Lia Sucupira — Universidade de Fortaleza), registrar L3 descritiva aprovada e recompilar a versão para revisão da autora

---

## Referências (todas na pasta Bibliografia ou nas aulas)

- Bettencourt et al. 2007, *Growth, innovation, scaling, and the pace of life in cities* (Aula 4, slide 22; Aula 5, slide 15)
- Bettencourt, *Introduction to Urban Science* (SAMIs, pp. 127–143)
- Melo et al. 2014, *Statistical signs of social influence on suicides*
- Arcaute et al. 2015, *Constructing cities, deconstructing scaling laws*
- Gastner & Newman 2006, *Optimal design of spatial distribution networks*
- Um et al. 2009, *Scaling laws between population and facility densities* (Aula 4, slide 44; o artigo não está na pasta)
- Xu et al. 2020, *Deconstructing laws of accessibility and facility distribution in cities*
- Bruno et al. 2024, *A universal framework for inclusive 15-minute cities*
- Maia et al. 2023, *A global empirical study on how street networks facilitate driving longer distances*
- Hansen 1959, *How accessibility shapes land use*
- Ponte et al. 2018, *Traveling heterogeneity in public transportation*
- Newman, *Power laws, Pareto distributions and Zipf's law*
- Oliveira et al. 2018, *A worldwide model for boundaries of urban settlements*
- Arcaute et al. 2016, percolação hierárquica (Aula 5, slides 19–21; o artigo não está na pasta)


---

## Atualização após reexecução com a menor distância total — 04/11/2026

A autora aprovou atribuir cada setor ao pronto-atendimento que minimiza ligação setor–rua + percurso na rede + ligação unidade–rua. Esta regra substitui, nos resultados atuais, a seleção somente pelo trecho entre nós. A implementação e a comparação estão em `notebooks/retomada/03_distancias_completas.ipynb`; as análises L2, renda, L3, P90, mapas e figura foram executadas novamente.

A versão Todos tem uma exceção de área: o PA Ilha de Maré em Salvador recebeu dois setores com 1.178 moradores, mas as ligações dos pontos à rua (4.904 m e 6.136 m) excedem o filtro de 2 km. A autora aprovou manter a unidade no cadastro e excluí-la apenas dos ajustes por áreas sem setores válidos. A ligação da unidade à rede considerada é 5.166 m. Conferência detalhada em `notebooks/retomada/05_diagnostico_areas_sem_setores.ipynb`.

Valores atuais: L2 SUS α=0,861 [0,797; 0,935], 245 áreas/245 unidades; Todos α=0,899 [0,834; 0,973], 272 áreas/273 unidades. Modelo de renda: δ SUS=−0,196 [−0,353; −0,029]; Todos δ=0,029 [−0,122; 0,188]. Esses resultados são associativos e não testam localização ótima. O artigo foi atualizado com a figura atual e compilado em duas páginas; verificação final e discussão didática com a autora continuam pendentes.
