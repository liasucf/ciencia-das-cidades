# Artigo

O texto de [artigo.tex](artigo.tex) tem quatro figuras (método setor→PA em três painéis, escala L1/L2, Gini da distância contra a oferta de PAs, e distância por renda e densidade) e autoria **Lia Sucupira — Universidade de Fortaleza**. As análises do artigo usam apenas PAs que atendem ao SUS, sem comparações com os demais cadastrados. Após revisão e recompilação, o PDF tem **5 páginas**, incluindo as figuras, no limite de **5 páginas informado pela autora**. A documentação do manual ainda indica **3 páginas**; confirmar com o professor antes da entrega, pois o texto atual ultrapassa esse limite.

## Respostas da autora em 04/11/2026

- Autoria: **Lia Sucupira**. Afiliação: **Universidade de Fortaleza**.
- L3 descritiva aprovada: curvas e Gini, sem escolher uma cauda, estimar γ ou afirmar rejeição estatística de lei de potência.

As respostas foram incorporadas ao notebook de geração e ao PDF, que está preparado para a revisão da autora antes da entrega ao professor.

## Como atualizar

Use [07_artigo.ipynb](../notebooks/07_artigo.ipynb). Ele contém as configurações de autoria e L3, o texto e a bibliografia; lê os resultados dos notebooks anteriores e gera `artigo.tex`, `referencias.bib` e o PDF. Alterações feitas somente no `.tex` serão substituídas ao reexecutar esse notebook.

O notebook confere referências resolvidas e caixas largas, registra o número de páginas (aceita até 5) e avisa quando passa de 3 por causa da divergência com o manual. [verificacao.json](verificacao.json) registra a compilação e [estado_rascunho.json](estado_rascunho.json) registra as configurações confirmadas. A conferência visual do PDF complementa essas verificações.

O modelo de renda é o conjunto simples escolhido pela autora, sem efeitos fixos por capital. O texto informa essa limitação. As análises, gráficos adicionais e decisões estão nos notebooks listados em [notebooks/README.md](../notebooks/README.md).
