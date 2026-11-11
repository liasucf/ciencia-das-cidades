# Ciência das cidades

Pesquisa sobre acesso a unidades de pronto atendimento nas capitais brasileiras. O projeto reúne coleta e preparação de dados em `scripts/`, análises em `notebooks/`, figuras em `figuras/` e o artigo em `artigo/`.

Para acompanhar a ordem das análises e as decisões metodológicas, consulte [notebooks/README.md](notebooks/README.md), [CHECKLIST_PESQUISA.md](CHECKLIST_PESQUISA.md) e [CONCEITOS_E_CRITERIOS.md](CONCEITOS_E_CRITERIOS.md).

## Dados e execução

O repositório inclui os arquivos de entrada em `dados/` (CNES, IBGE e OpenStreetMap), as redes viárias salvas e as tabelas intermediárias usadas pelos notebooks. Os arquivos maiores ficam no Git LFS. Depois de instalar Git LFS, clone o repositório normalmente ou execute `git lfs pull` em um clone existente para obter os dados completos; sem esse passo, os arquivos grandes serão apenas ponteiros de texto.

Crie um ambiente Python, instale as dependências de [requirements.txt](requirements.txt) e siga a ordem de [notebooks/README.md](notebooks/README.md). Os scripts documentam as entradas e saídas e podem reconstruir as tabelas processadas. O ambiente virtual `.venv/`, as apresentações de aula e as cópias locais dos artigos de referência não são versionados. As referências bibliográficas constam em `artigo/referencias.bib`.

Fontes dos dados: CNES/OpenDataSUS (`dados/cnes/`), Censo 2022/IBGE (`dados/ibge/`) e extratos do OpenStreetMap distribuídos pelo Geofabrik (`dados/osm/`).
