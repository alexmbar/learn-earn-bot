.PHONY: all open-all open-earn open-micro track summary schedule-daily schedule-cron test lint export

# Configuracion
TIME    ?= 09:00
HOURS   ?= 6
CAT     ?=
GOAL    ?= 5
PY      := python3

## Abrir plataformas
all:
	$(PY) learn_earn_helper.py --all --panel

open-earn:
	$(PY) learn_earn_helper.py --category learn_earn --panel

open-micro:
	$(PY) learn_earn_helper.py --category microtask --panel

open-all:
	$(PY) learn_earn_helper.py --all

## Tracker
track:
	@echo "Uso: make track P=<plataforma> A=<monto> [N='nota']"
	$(PY) tracker.py log $(P) $(A) $(if $(N),--note "$(N)",)

summary:
	$(PY) tracker.py summary

export:
	$(PY) tracker.py export

set-goal:
	$(PY) tracker.py set-goal $(GOAL)

## Scheduler
schedule-once:
	$(PY) scheduler.py once $(if $(CAT),--category $(CAT),)

schedule-daily:
	$(PY) scheduler.py daily --time $(TIME) $(if $(CAT),--category $(CAT),)

schedule-interval:
	$(PY) scheduler.py interval --hours $(HOURS) $(if $(CAT),--category $(CAT),)

schedule-cron:
	$(PY) scheduler.py cron --time $(TIME) $(if $(CAT),--category $(CAT),)

## Dev
test:
	$(PY) tests/run_tests.py

lint:
	flake8 learn_earn_helper.py tracker.py scheduler.py --max-line-length=120

install-dev:
	pip install flake8

help:
	@echo ""
	@echo "  make all                   Abre todas las plataformas + panel HTML"
	@echo "  make open-earn             Solo Learn & Earn cripto"
	@echo "  make open-micro            Solo microtareas"
	@echo "  make track P=clickworker A=2.50 [N='nota']"
	@echo "  make summary               Ver resumen de progreso"
	@echo "  make export                Exportar historial a CSV"
	@echo "  make set-goal GOAL=10      Cambiar meta en USD"
	@echo "  make schedule-daily TIME=09:00"
	@echo "  make schedule-interval HOURS=6"
	@echo "  make schedule-cron TIME=09:00"
	@echo "  make test                  Correr todos los tests"
	@echo "  make lint                  Verificar estilo de codigo"
	@echo ""
