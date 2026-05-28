# learn-earn-bot

Asistente semiautomático para plataformas **Learn & Earn** de cripto y **Microtask platforms** (Coinbase, Binance, Kraken, Clickworker, Microworkers, Remotasks, UserTesting, Prolific).
Inclye un **tracker de progreso** para registrar ganancias y visualizar el avance hacia tu meta.

> **Este proyecto NO automatiza KYC, wallets, quizzes ni transacciones.**
> Solo abre recursos oficiales, genera un panel HTML y guía con pasos seguros.

## Instalación

```bash
git clone https://github.com/alexmbar/learn-earn-bot.git
cd learn-earn-bot
python learn_earn_helper.py --help
python tracker.py --help
```

## learn_earn_helper.py — Abrir plataformas

```bash
# Abrir TODAS las plataformas
python learn_earn_helper.py --all --panel

# Solo microtareas
python learn_earn_helper.py --category microtask

# Solo Learn & Earn cripto
python learn_earn_helper.py --category learn_earn

# Plataforma individual
python learn_earn_helper.py clickworker --panel

# Solo imprimir pasos sin abrir nada
python learn_earn_helper.py --all --print-only
```

## tracker.py — Registrar progreso

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

## Plataformas soportadas

### Learn & Earn (cripto)

| Plataforma | Comando | Tipo | Pago |
|---|---|---|---|
| Coinbase Earn / Wallet Quests | `coinbase_earn` | Quiz / Quests onchain | Cripto |
| Binance Academy Learn & Earn | `binance_learn` | Quiz / Lecciones | Cripto |
| Kraken Earn | `kraken_earn` | Staking | Cripto (requiere depósito) |

### Microtask Platforms

| Plataforma | Comando | Tipo | Pago |
|---|---|---|---|
| Clickworker | `clickworker` | Redacción, datos, IA | PayPal/Payoneer semanal |
| Microworkers | `microworkers` | Testing, formularios | PayPal/cripto |
| Remotasks | `remotasks` | Etiquetado, IA | PayPal semanal (~$3-7/hr) |
| UserTesting | `usertesting` | Pruebas UX | PayPal (~$22.50/hr prom.) |
| Prolific | `prolific` | Encuestas académicas | PayPal (mín. $9/hr) |

## Flags de learn_earn_helper.py

| Flag | Descripción |
|---|---|
| `--all` | Abre todas las plataformas |
| `--category learn_earn` | Solo plataformas Learn & Earn |
| `--category microtask` | Solo plataformas de microtareas |
| `--panel` | Genera `learn_earn_panel.html` |
| `--print-only` | Solo imprime pasos |
| `--delay N` | Segundos entre URLs (default: 1.5) |

## Comandos de tracker.py

| Comando | Descripción |
|---|---|
| `log <plataforma> <monto>` | Registrar un ingreso |
| `summary` | Ver resumen y progreso hacia la meta |
| `set-goal <monto>` | Cambiar la meta en USD |
| `reset` | Borrar historial |

## Archivos generados

| Archivo | Descripción |
|---|---|
| `learn_earn_panel.html` | Panel visual con enlaces (generado con `--panel`) |
| `tracker_data.json` | Historial de ingresos registrados |

## Qué NO hace
- No resuelve quizzes ni lecciones por ti.
- No firma transacciones ni interactúa con wallets.
- No intenta evadir controles anti-bot, KYC o verificación de cuenta.
- No garantiza recompensas.

## Requerimientos

- Python 3.8+
- Sin dependencias externas (solo stdlib)

## Licencia

MIT
