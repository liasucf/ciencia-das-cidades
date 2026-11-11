#!/usr/bin/env bash
# Roda o Dijkstra (script 03) em todas as capitais com pronto-atendimento: todos os PAs e só SUS.
# Uso: bash scripts/08_todas_capitais.sh   (log em dados/processados/distancias/log_todas.txt)
cd "$(dirname "$0")/.." || exit 1
LOG=dados/processados/distancias/log_todas.txt
mkdir -p "$(dirname "$LOG")"
: > "$LOG"
.venv/bin/python -c "
import pandas as pd
c = pd.read_csv('dados/processados/capitais_resumo.csv')
print('\n'.join(c[c.n_pa > 0].sort_values('populacao_2022').municipio))
" | while read -r capital; do
  for opcao in "" "--so-sus"; do
    echo "### $capital $opcao" >> "$LOG"
    .venv/bin/python scripts/03_distancias_capital.py "$capital" $opcao 2>&1 | grep -v -i warning >> "$LOG" \
      || echo "FALHOU: $capital $opcao" >> "$LOG"
  done
done
echo "### FIM" >> "$LOG"
