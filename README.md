# learn-earn-bot

Asistente semiautomático para plataformas **Learn & Earn** de cripto (Coinbase, Binance).

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
# Coinbase Earn + panel HTML local
python learn_earn_helper.py coinbase_earn --panel

# Binance Academy Learn & Earn + panel HTML local
python learn_earn_helper.py binance_learn --panel

# Solo imprimir pasos sin abrir nada
python learn_earn_helper.py coinbase_earn --print-only

# Ajustar delay entre apertura de URLs
python learn_earn_helper.py coinbase_earn --delay 2.0
```

## Plataformas soportadas

| Plataforma | Comando |
|---|---|
| Coinbase Earn / Wallet Quests | `coinbase_earn` |
| Binance Academy Learn & Earn | `binance_learn` |

## Qué hace
- Abre las páginas oficiales de cada plataforma en tu navegador.
- Genera `learn_earn_panel.html` con enlaces, comandos y reglas (usa `--panel`).
- Imprime un checklist de pasos seguros para completar tareas.

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
