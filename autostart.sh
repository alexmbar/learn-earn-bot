#!/usr/bin/env bash
# autostart.sh — Configura el scheduler para arrancar al login (Linux/macOS)
# Uso: bash autostart.sh [--time HH:MM] [--category learn_earn|microtask]

set -e

PY=$(which python3 || which python)
DIR="$(cd "$(dirname "$0")" && pwd)"
TIME="09:00"
CATEGORY=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --time) TIME="$2"; shift 2 ;;
    --category) CATEGORY="$2"; shift 2 ;;
    *) echo "Argumento desconocido: $1"; exit 1 ;;
  esac
done

CAT_FLAG=""
[ -n "$CATEGORY" ] && CAT_FLAG="--category $CATEGORY"

H=$(echo $TIME | cut -d: -f1)
M=$(echo $TIME | cut -d: -f2)

CRON_LINE="$M $H * * * $PY $DIR/scheduler.py once $CAT_FLAG >> $DIR/scheduler.log 2>&1"

echo "Instalando cron para ejecutarse a las $TIME diariamente..."
(crontab -l 2>/dev/null | grep -v "learn-earn-bot\|learn_earn_helper"; echo "# learn-earn-bot"; echo "$CRON_LINE") | crontab -
echo "Cron instalado:"
echo "  $CRON_LINE"
echo ""
echo "Para ver logs: tail -f $DIR/scheduler.log"
echo "Para eliminar: crontab -e y borra la linea con # learn-earn-bot"
