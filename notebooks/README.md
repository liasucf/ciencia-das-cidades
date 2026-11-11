# Notebooks do trabalho

A autora pediu que **todas as etapas analíticas e de visualização sejam feitas em notebooks**. Scripts são reservados à coleta de dados. O [checklist da pesquisa](../CHECKLIST_PESQUISA.md) registra pedidos e decisões; o [guia de conceitos](../CONCEITOS_E_CRITERIOS.md) relaciona o projeto às aulas e ao manual do professor.

## Ordem atual

1. [00_conferencia_dados.ipynb](00_conferencia_dados.ipynb) — auditoria dos dados e arquivos existentes.
2. [01_correcao_setores.ipynb](01_correcao_setores.ipynb) — histórico e conferência da união dos polígonos repetidos.
3. [retomada/01_dados.ipynb](retomada/01_dados.ipynb) — prepara CNES, coordenadas, setores, população e renda.
4. [retomada/02_dijkstra_exemplo.ipynb](retomada/02_dijkstra_exemplo.ipynb) — exemplo pequeno, com ruas de mão única, para entender menor caminho.
5. [retomada/03_distancias_completas.ipynb](retomada/03_distancias_completas.ipynb) — une setores repetidos e recalcula distância mínima total para as 26 capitais e duas versões.
6. [retomada/05_diagnostico_areas_sem_setores.ipynb](retomada/05_diagnostico_areas_sem_setores.ipynb) — explica por que o PA Ilha de Maré não forma área válida no L2 após o filtro aprovado.
7. [02_L2_densidade.ipynb](02_L2_densidade.ipynb) — relaciona densidade de pronto-atendimentos e densidade populacional; 2.000 reamostragens bootstrap.
8. [03_renda_residuos.ipynb](03_renda_residuos.ipynb) — modelo conjunto simples de renda e densidade escolhido pela autora.
9. [04_distancias_L3.ipynb](04_distancias_L3.ipynb) — curvas de distância, Gini e comparação descritiva por renda, sem ajuste de cauda.
10. [retomada/04_mapas_grupos_P90.ipynb](retomada/04_mapas_grupos_P90.ipynb) — 16 grupos renda × densidade, P90, mapas de Fortaleza e áreas de atendimento.
11. [05_L1_escala.ipynb](05_L1_escala.ipynb) — número de unidades em função da população das capitais.
12. [06_figura_final.ipynb](06_figura_final.ipynb) — figura vetorial de síntese.
13. [07_artigo.ipynb](07_artigo.ipynb) — gera e confere o artigo em LaTeX.

## Estado depois da escolha da menor distância total

A autora aprovou a unidade que minimiza **ligação do setor à rua + percurso na rede + ligação da unidade à rua**. O Dijkstra usa fontes auxiliares com o custo de ligação de cada unidade. As 52 tabelas (26 capitais × SUS/Todos) foram refeitas; os notebooks L2, renda, L3, mapas, figura e artigo foram reexecutados com a nova regra.

Em Salvador, no recorte Todos, o PA Ilha de Maré tem ligação de aproximadamente 5,17 km ao componente de ruas usado. Os dois setores atribuídos a esse grupo, com 1.178 moradores, têm ligação à rua acima de 2 km e ficam fora pelo filtro já aprovado. Como não sobra setor válido, o grupo não tem área/densidade para o L2. A autora autorizou excluí-lo **somente dos ajustes por área** e documentar a exceção; o PA continua no cadastro e na contagem municipal. As análises de distância já aplicam o filtro a esses setores.

L2 atualizado: SUS, α=0,861 (IC95% 0,797–0,935), 245 áreas/unidades; Todos, α=0,899 (0,834–0,973), 272 áreas representando 273 unidades. O modelo de renda: δ=−0,196 (−0,353 a −0,029) em SUS; δ=0,029 (−0,122 a 0,188) em Todos. São associações, não causalidade nem prova de localização ótima.

A L3, mapas e figura usam as distâncias atualizadas. O artigo foi compilado com **duas páginas**, referências resolvidas e sem avisos de caixas largas. A conferência visual do PDF foi feita. Ainda falta a revisão interpretativa acompanhada com a autora; execução sem erro não significa que ela já compreendeu e consiga explicar cada etapa.

## Saídas

- Mapas em `figuras/retomada/mapas/` (PNG/PDF); figura vetorial em `figuras/final/`.
- Curvas, gráficos e intervalos em `figuras/L1/`, `figuras/L2/`, `figuras/renda/` e `figuras/distancias/`.
- Tabelas intermediárias em `dados/processados/retomada/` e `dados/processados/analises/`.
- Artigo em `artigo/artigo.pdf`; a autora deve revisar a redação antes de entregar.
