# learn-earn-bot

Asistente semiautomático para plataformas **Learn & Earn** de cripto y **Microtask platforms** (Coinbase, Binance, Kraken, Clickworker, Microworkers, Remotasks, UserTesting, Prolific).

> **Este proyecto NO automatiza KYC, wallets, quizzes ni transacciones.**
> Solo abre recursos oficiales, genera un panel HTML y guía con pasos seguros.

## Instalación

```bash
git clone https://github.com/alexmbar/learn-earn-bot.git
cd learn-earn-bot
python learn_earn_helper.py --help
```

## Uso

```bash
# Abrir TODAS las plataformas a la vez
python learn_earn_helper.py --all

# Solo plataformas Learn & Earn (cripto)
python learn_earn_helper.py --category learn_earn

# Solo plataformas de microtareas
python learn_earn_helper.py --category microtask

# Plataforma individual
python learn_earn_helper.py clickworker --panel
python learn_earn_helper.py coinbase_earn --panel

# Solo imprimir pasos sin abrir nada
python learn_earn_helper.py --all --print-only

# Generar panel HTML local con todos los enlaces
python learn_earn_helper.py --all --panel

# Ajustar delay entre apertura de URLs
python learn_earn_helper.py --all --delay 2.0
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

## Flags disponibles

| Flag | Descripción |
|---|---|
| `--all` | Abre todas las plataformas |
| `--category learn_earn` | Solo plataformas Learn & Earn |
| `--category microtask` | Solo plataformas de microtareas |
| `--panel` | Genera `learn_earn_panel.html` |
| `--print-only` | Solo imprime pasos, no abre navegador |
| `--delay N` | Segundos entre apertura de URLs (default: 1.5) |

## Qué hace
- Abre páginas oficiales de 8 plataformas en tu navegador.
- Soporta `--all`, `--category` y plataforma individual.
- Genera `learn_earn_panel.html` con enlaces, insignias, advertencias y reglas.
- Imprime checklist de pasos seguros para cada plataforma.

## Qué NO hace
- No resuelve quizzes ni lecciones por ti.
- No firma transacciones ni interactúa con wallets.
- No intenta evadir controles anti-bot, KYC o verificación de cuenta.
- No garantiza recompensas (dependen de disponibilidad regional y elegibilidad).

## Requerimientos

- Python 3.8+
- Sin dependencias externas (solo stdlib)

## Licencia

MIT
