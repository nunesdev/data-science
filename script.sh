#!/bin/bash

# Caminho do repositório Git
REPO_DIR="/Volumes/Extreme SSD/www/data-science/degree-infnet-brasil-2024-2027"
LOGFILE="/Volumes/Extreme SSD/www/data-science/tmp/watchfolder.log"
LOCKFILE="/Volumes/Extreme SSD/www/data-science/tmp/git_watch.lock"

cd "$REPO_DIR" || exit 1

# Debounce: evita rodar mais de 1 vez dentro de 30 segundos
if [ -f "$LOCKFILE" ] && [ "$(($(date +%s) - $(cat "$LOCKFILE")))" -lt 30 ]; then
  echo "[$(date)] Alteração ignorada (debounce ativo)" >> "$LOGFILE"
  exit 0
fi

# Atualiza o lockfile com o timestamp atual
date +%s > "$LOCKFILE"

# Log de início
echo "[$(date)] Mudança detectada, iniciando commit/push..." >> "$LOGFILE"

# Adiciona todos os arquivos
git add -A

# Faz commit com timestamp (só se houver alterações pendentes)
if ! git diff --cached --quiet; then
  git commit -m "Auto commit em $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOGFILE" 2>&1
  git push origin main >> "$LOGFILE" 2>&1
  echo "[$(date)] Commit e push concluídos." >> "$LOGFILE"
else
  echo "[$(date)] Nenhuma alteração para commit." >> "$LOGFILE"
fi


# remote office not required, pragmatic programmer