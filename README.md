# Ciência das cidades

Pesquisa sobre acesso a unidades de pronto atendimento nas capitais brasileiras. O projeto reúne coleta e preparação de dados em `scripts/`, análises em `notebooks/`, figuras em `figuras/` e o artigo em `artigo/`.

Para acompanhar a ordem das análises e as decisões metodológicas, consulte [notebooks/README.md](notebooks/README.md), [CHECKLIST_PESQUISA.md](CHECKLIST_PESQUISA.md) e [CONCEITOS_E_CRITERIOS.md](CONCEITOS_E_CRITERIOS.md).

## Dados locais

Os dados em `dados/` (exceto `correcoes_manuais.csv`) ficam fora do Git porque incluem downloads e tabelas intermediárias que somam vários gigabytes. Os scripts documentam as entradas e saídas esperadas; parte dos dados é baixada pelo próprio código. Para reproduzir as análises, obtenha os dados do CNES e do IBGE indicados nos scripts e execute as etapas na ordem descrita em [notebooks/README.md](notebooks/README.md). Os extratos OSM são obtidos do Geofabrik pelo script de distâncias.

O ambiente virtual `.venv/`, as apresentações de aula e as cópias locais dos artigos de referência também não são versionados. As dependências Python estão em [requirements.txt](requirements.txt); as referências bibliográficas constam em `artigo/referencias.bib`.
