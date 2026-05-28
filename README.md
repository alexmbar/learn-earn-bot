# learn-earn-bot

Asistente semiautomático para plataformas **Learn & Earn** de cripto y **Microtask platforms**.  
Incluye tracker de progreso y scheduler para apertura diaria o por intervalo.

> **Este proyecto NO automatiza KYC, wallets, quizzes ni transacciones.**  
> Solo abre recursos oficiales, genera un panel HTML y guía con pasos seguros.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](#licencia)

---

## Contenido

- [Instalación](#instalación)
- [Archivos del proyecto](#archivos-del-proyecto)
- [Plataformas soportadas](#plataformas-soportadas)
- [learn\_earn\_helper.py](#learn_earn_helperpy--abrir-plataformas)
- [tracker.py](#trackerpy--registrar-progreso)
- [scheduler.py](#schedulerpy--automatizar-apertura)
- [Tests](#tests)
- [Errores corregidos](#errores-corregidos)
- [Requerimientos](#requerimientos)

---

## Instalación

```bash
git clone https://github.com/alexmbar/learn-earn-bot.git
cd learn-earn-bot
python --version  # requiere 3.8+
```

No requiere instalar dependencias externas. Solo stdlib de Python.

---

## Archivos del proyecto

```
learn-earn-bot/
├── learn_earn_helper.py   # Abre plataformas y genera panel HTML
├── tracker.py             # Registra ingresos y muestra progreso
├── scheduler.py           # Automatiza apertura diaria o por intervalo
├── tests/
│   ├── test_helper.py      # Tests para learn_earn_helper.py
│   ├── test_tracker.py     # Tests para tracker.py
│   ├── test_scheduler.py   # Tests para scheduler.py
│   └── run_tests.py        # Runner: ejecuta todos los tests
├── learn_earn_panel.html  # Generado con --panel (no versionado)
└── tracker_data.json      # Historial de ingresos (no versionado)
```

---

## Plataformas soportadas

### Learn & Earn (cripto)

| Plataforma | Comando | Tipo | Pago |
|---|---|---|---|
| Coinbase Earn / Wallet Quests | `coinbase_earn` | Quiz / Quests onchain | Cripto |
| Binance Academy Learn & Earn | `binance_learn` | Quiz / Lecciones | Cripto |
| Kraken Earn | `kraken_earn` | Staking | Cripto (requiere depósito) |

> **Nota Kraken:** Requiere depositar cripto para ganar recompensas vía staking. No es un programa de lecciones gratuitas.

### Microtask Platforms

| Plataforma | Comando | Tipo | Pago |
|---|---|---|---|
| Clickworker | `clickworker` | Redacción, datos, IA | PayPal / Payoneer semanal |
| Microworkers | `microworkers` | Testing, formularios | PayPal / cripto |
| Remotasks | `remotasks` | Etiquetado, IA | PayPal semanal (~$3–7/hr) |
| UserTesting | `usertesting` | Pruebas UX | PayPal (~$22.50/hr prom.) |
| Prolific | `prolific` | Encuestas académicas | PayPal (mín. $9/hr) |

---

## `learn_earn_helper.py` — Abrir plataformas

```bash
# Abrir TODAS las plataformas
python learn_earn_helper.py --all

# Todas + generar panel HTML local
python learn_earn_helper.py --all --panel

# Solo plataformas Learn & Earn (cripto)
python learn_earn_helper.py --category learn_earn

# Solo plataformas de microtareas
python learn_earn_helper.py --category microtask

# Plataforma individual
python learn_earn_helper.py clickworker
python learn_earn_helper.py coinbase_earn --panel

# Solo imprimir pasos sin abrir navegador
python learn_earn_helper.py --all --print-only

# Ajustar delay entre apertura de URLs (segundos)
python learn_earn_helper.py --all --delay 2.0
```

### Flags disponibles

| Flag | Descripción |
|---|---|
| `--all` | Abre todas las plataformas |
| `--category learn_earn` | Solo plataformas Learn & Earn |
| `--category microtask` | Solo plataformas de microtareas |
| `--panel` | Genera `learn_earn_panel.html` con enlaces y reglas |
| `--print-only` | Solo imprime pasos, no abre navegador |
| `--delay N` | Segundos entre apertura de URLs (default: 1.5) |

---

## `tracker.py` — Registrar progreso

```bash
# Registrar un ingreso
python tracker.py log clickworker 2.50
python tracker.py log usertesting 10.00 --note "prueba UX completada"
python tracker.py log coinbase_earn 1.25 --currency USDC

# Ver resumen de progreso
python tracker.py summary

# Cambiar la meta (default: $5 USD)
python tracker.py set-goal 10

# Borrar todo el historial
python tracker.py reset
```

### Ejemplo de salida `summary`

```
=======================================================
 RESUMEN DE PROGRESO
 Meta: $5.00 USD
 Total acumulado (USD): $12.50
 Progreso: 100.0%
 Entradas: 3
=======================================================

 Por plataforma:
  UserTesting                          $10.00 USD
  Clickworker                          $2.50 USD

 Ultimas 5 entradas:
  2026-05-27 09:00  UserTesting    $10.00 USD (prueba UX completada)
  2026-05-27 10:00  Clickworker    $2.50 USD

 META ALCANZADA: $12.50 / $5.00
```

### Comandos disponibles

| Comando | Descripción |
|---|---|
| `log <plataforma> <monto>` | Registrar un ingreso |
| `summary` | Ver resumen, totales y progreso hacia meta |
| `set-goal <monto>` | Cambiar la meta en USD |
| `reset` | Borrar todo el historial |

---

## `scheduler.py` — Automatizar apertura

```bash
# Ejecutar una vez ahora
python scheduler.py once
python scheduler.py once --category microtask --print-only

# Abrir todos los días a las 9:00 AM
python scheduler.py daily --time 09:00

# Solo microtareas todos los días a las 8:30
python scheduler.py daily --time 08:30 --category microtask

# Abrir cada 6 horas
python scheduler.py interval --hours 6

# Generar línea crontab lista para copiar
python scheduler.py cron --time 09:00
python scheduler.py cron --time 09:00 --category microtask
```

### Modos disponibles

| Modo | Descripción |
|---|---|
| `once` | Ejecuta una vez inmediatamente |
| `daily --time HH:MM` | Repite todos los días a la hora indicada |
| `interval --hours N` | Repite cada N horas |
| `cron --time HH:MM` | Imprime la línea cron equivalente |

> El scheduler mantiene el proceso activo (loop). Usa `Ctrl+C` para detenerlo.  
> Para ejecución desatendida en segundo plano, usa el modo `cron` y confíguralo en `crontab -e`.

---

## Tests

```bash
# Correr todos los tests
python tests/run_tests.py

# Módulo específico
python -m unittest tests.test_tracker -v
python -m unittest tests.test_helper -v
python -m unittest tests.test_scheduler -v
```

### Cobertura

| Archivo de test | Qué verifica |
|---|---|
| `test_tracker.py` | load/save, log, meta alcanzada, plataforma inválida, summary vacío, set-goal |
| `test_helper.py` | estructura de TASKS, URLs HTTPS, categorías válidas, `run_task`, `save_panel` |
| `test_scheduler.py` | flags de cmd, `seconds_until`, output cron, `cmd_once` llama subprocess |

---

## Errores corregidos

| Bug | Archivo | Severidad | Fix |
|---|---|---|---|
| `str \| None` requiere Python 3.10+ | `scheduler.py` | 🔴 Crítico | Cambiado a `Optional[str]` de `typing` |
| Currency siempre de `entries[0]` en summary | `tracker.py` | 🟡 Menor | Agrupa por `(plataforma, currency)` |
| `platform` implícito en `daily`/`interval` | `scheduler.py` | 🟢 Code smell | `platform=None` explícito en `add_common` |

---

## Qué NO hace este proyecto

- No resuelve quizzes ni lecciones por ti.
- No firma transacciones ni interactúa con wallets.
- No intenta evadir controles anti-bot o KYC.
- No garantiza recompensas (dependen de disponibilidad regional y elegibilidad).

---

## Requerimientos

- Python 3.8+
- Sin dependencias externas (solo stdlib)

---

## Licencia

MIT
