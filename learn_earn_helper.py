#!/usr/bin/env python3
import argparse, time, sys
from pathlib import Path

BANNER = """
Asistente semiautomático para Learn & Earn / Quests

IMPORTANTE:
- Este script NO evade KYC, NO firma transacciones y NO intenta saltarse controles anti-bot.
- Solo automatiza tareas permitidas: abrir páginas, esperar y guiarte paso a paso.
- Revisa los Términos del proveedor antes de usar.
"""

TASKS = {
    "coinbase_earn": {
        "name": "Coinbase Earn / Wallet Quests",
        "urls": [
            "https://www.coinbase.com/earn",
            "https://www.coinbase.com/wallet/quests",
        ],
        "steps": [
            "Inicia sesión manualmente.",
            "Verifica elegibilidad por país y disponibilidad de campañas.",
            "Completa quizzes o lecciones permitidas.",
            "NO automatices confirmaciones de wallet o transacciones.",
        ],
    },
    "binance_learn": {
        "name": "Binance Academy Learn & Earn",
        "urls": [
            "https://www.binance.com/en/academy/learn-and-earn",
        ],
        "steps": [
            "Inicia sesión manualmente y completa KYC si aplica.",
            "Abre una campaña activa y responde el quiz tú mismo.",
            "Verifica términos de elegibilidad y cupos disponibles.",
        ],
    },
    "kraken_earn": {
        "name": "Kraken Earn (staking / recompensas)",
        "urls": [
            "https://www.kraken.com/earn",
            "https://support.kraken.com/hc/en-us/categories/200122606-Funding",
        ],
        "steps": [
            "Crea o inicia sesión en tu cuenta de Kraken manualmente.",
            "Completa KYC (verificación de identidad) si aún no lo has hecho.",
            "Revisa qué activos están disponibles para Earn en tu región (México puede tener restricciones).",
            "Para ganar recompensas, deposita o transsfiere el activo elegible a Kraken Earn.",
            "Revisa APY, límites de bonificación y mínimos de retiro antes de comprometer fondos.",
            "NO es un Learn & Earn clásico: requiere tener cripto; las recompensas vienen del staking.",
        ],
    },
}

HTML_TEMPLATE = """<!doctype html>
<html lang=\"es\"><meta charset=\"utf-8\"><title>Panel Learn & Earn</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#111;color:#eee;padding:24px;line-height:1.6}}
h1{{color:#7dd3fc}} h2{{color:#a5f3fc}}
.card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:16px;margin:14px 0}}
a{{color:#7dd3fc;text-decoration:none}} a:hover{{text-decoration:underline}}
code{{background:#222;padding:2px 6px;border-radius:6px;font-size:.9em}}
.warn{{background:#2d1a00;border:1px solid #7c4a03;border-radius:8px;padding:10px 14px;margin:8px 0;color:#fbbf24}}
ul{{padding-left:1.2em}}
</style>
<h1>Panel semiautomático Learn & Earn</h1>
<p>Este panel concentra enlaces y pasos seguros. <strong>No automatiza KYC, quizzes ni transacciones.</strong></p>
<div class=\"card\"><h2>Coinbase</h2>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.coinbase.com/earn\">Coinbase Earn</a> &nbsp;|
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.coinbase.com/wallet/quests\">Wallet Quests</a>
</div>
<div class=\"card\"><h2>Binance</h2>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.binance.com/en/academy/learn-and-earn\">Binance Academy Learn & Earn</a>
</div>
<div class=\"card\"><h2>Kraken Earn</h2>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.kraken.com/earn\">Kraken Earn</a> &nbsp;|
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://support.kraken.com/hc/en-us/categories/200122606-Funding\">Soporte / Funding</a>
<div class=\"warn\">&#9888; Kraken Earn requiere depositar cripto (staking). No es un programa quiz/lección gratuito. Verifica disponibilidad en México.</div>
</div>
<div class=\"card\"><h2>Reglas de uso</h2><ul>
<li>Login manual siempre.</li>
<li>No automatices wallet ni aprobaciones de transacciones.</li>
<li>Confirma recompensas y mínimos de retiro antes de continuar.</li>
<li>Verifica disponibilidad regional.</li>
</ul></div>
<div class=\"card\"><h2>Comandos rápidos</h2>
<code>python learn_earn_helper.py coinbase_earn --panel</code><br><br>
<code>python learn_earn_helper.py binance_learn --panel</code><br><br>
<code>python learn_earn_helper.py kraken_earn --panel</code><br><br>
<code>python learn_earn_helper.py coinbase_earn --print-only</code>
</div>
</html>"""

def save_panel(path: Path):
    path.write_text(HTML_TEMPLATE, encoding="utf-8")
    print(f"Panel HTML guardado en: {path.resolve()}")

def main():
    parser = argparse.ArgumentParser(
        description="Asistente semiautomático para plataformas Learn & Earn de cripto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo: python learn_earn_helper.py coinbase_earn --panel"
    )
    parser.add_argument("platform", choices=sorted(TASKS.keys()), help="Plataforma objetivo")
    parser.add_argument("--print-only", action="store_true", help="Solo imprime pasos, no abre nada")
    parser.add_argument("--delay", type=float, default=1.5, help="Segundos entre apertura de URLs (default: 1.5)")
    parser.add_argument("--panel", action="store_true", help="Genera panel HTML local con enlaces")
    args = parser.parse_args()

    print(BANNER)
    task = TASKS[args.platform]
    print(f"Plataforma: {task['name']}")
    print("\nPasos a seguir:")
    for i, step in enumerate(task["steps"], 1):
        print(f"  {i}. {step}")

    if args.panel:
        save_panel(Path("learn_earn_panel.html"))

    if args.print_only:
        print("\nModo solo-lectura. Sin acciones de navegador.")
        return

    import webbrowser
    print("\nAbriendo URLs...")
    for url in task["urls"]:
        print(f"  -> {url}")
        webbrowser.open(url)
        time.sleep(args.delay)

    print("\nListo. Completa manualmente login, KYC, quizzes y transacciones.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
