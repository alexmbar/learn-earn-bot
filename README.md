# learn-earn-bot

Asistente semiautomático para plataformas **Learn & Earn** de cripto y **Microtask platforms**.  
Incluye tracker de progreso y scheduler para apertura automática diaria o por intervalo.

> **Este proyecto NO automatiza KYC, wallets, quizzes ni transacciones.**  
> Solo abre recursos oficiales, genera un panel HTML y guía con pasos seguros.

## Instalación

```bash
git clone https://github.com/alexmbar/learn-earn-bot.git
cd learn-earn-bot
python learn_earn_helper.py --help
python tracker.py --help
python scheduler.py --help
```

---

## `learn_earn_helper.py` — Abrir plataformas

```bash
python learn_earn_helper.py --all --panel          # Todas + panel HTML
python learn_earn_helper.py --category microtask   # Solo microtareas
python learn_earn_helper.py --category learn_earn  # Solo cripto
python learn_earn_helper.py clickworker --panel    # Plataforma individual
python learn_earn_helper.py --all --print-only     # Solo imprimir pasos
```

---

## `tracker.py` — Registrar progreso

```bash
python tracker.py log clickworker 2.50
python tracker.py log usertesting 10.00 --note "prueba UX completada"
python tracker.py log coinbase_earn 1.25 --currency USDC
python tracker.py summary
python tracker.py set-goal 10
python tracker.py reset
```

---

## `scheduler.py` — Automatizar apertura

```bash
# Ejecutar una vez ahora
python scheduler.py once
python scheduler.py once --category microtask

# Abrir todos los días a las 9:00 AM
python scheduler.py daily --time 09:00

# Solo microtareas todos los días a las 8:30
python scheduler.py daily --time 08:30 --category microtask

# Abrir cada 6 horas
python scheduler.py interval --hours 6

# Generar línea cron para configurar en el sistema
python scheduler.py cron --time 09:00
```

---

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

---

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `learn_earn_helper.py` | Abre plataformas, genera panel HTML |
| `tracker.py` | Registra ingresos y muestra progreso |
| `scheduler.py` | Automatiza apertura diaria o por intervalo |
| `learn_earn_panel.html` | Panel visual (generado con `--panel`) |
| `tracker_data.json` | Historial de ingresos registrados |

---

## Qué NO hace
- No resuelve quizzes ni lecciones.
- No firma transacciones ni interactúa con wallets.
- No evade controles anti-bot o KYC.
- No garantiza recompensas.

## Requerimientos

- Python 3.8+
- Sin dependencias externas (solo stdlib)

## Licencia

MIT
