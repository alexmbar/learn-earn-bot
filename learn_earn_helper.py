#!/usr/bin/env python3
import argparse, time, sys, webbrowser
from pathlib import Path

BANNER = """
Asistente semiautomático para Learn & Earn / Quests / Microtasks

IMPORTANTE:
- Este script NO evade KYC, NO firma transacciones y NO intenta saltarse controles anti-bot.
- Solo automatiza tareas permitidas: abrir páginas, esperar y guiarte paso a paso.
- Revisa los Términos del proveedor antes de usar.
"""

TASKS = {
    # ── Learn & Earn ────────────────────────────────────────
    "coinbase_earn": {
        "name": "Coinbase Earn / Wallet Quests",
        "category": "learn_earn",
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
        "category": "learn_earn",
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
        "category": "learn_earn",
        "urls": [
            "https://www.kraken.com/earn",
            "https://support.kraken.com/hc/en-us/categories/200122606-Funding",
        ],
        "steps": [
            "Crea o inicia sesión en tu cuenta de Kraken manualmente.",
            "Completa KYC si aún no lo has hecho.",
            "Revisa qué activos están disponibles para Earn en tu región.",
            "Deposita o transfiere el activo elegible a Kraken Earn.",
            "Revisa APY, límites y mínimos de retiro antes de comprometer fondos.",
            "Requiere tener cripto; las recompensas vienen del staking.",
        ],
    },
    # ── Microtask platforms ─────────────────────────────────
    "clickworker": {
        "name": "Clickworker (escritura, datos, categorización, IA)",
        "category": "microtask",
        "urls": [
            "https://workplace.clickworker.com/en/worker_registrations/new",
            "https://workplace.clickworker.com",
        ],
        "steps": [
            "Regístrate con tu email; no requiere KYC estricto al inicio.",
            "Completa tu perfil para acceder a más tareas.",
            "Las tareas incluyen redacción, investigación, etiquetado y evaluación de IA.",
            "Pagos semanales vía PayPal o Payoneer al alcanzar el mínimo.",
            "Disponible globalmente incluyendo México.",
        ],
    },
    "microworkers": {
        "name": "Microworkers (tareas rápidas, testing, formularios)",
        "category": "microtask",
        "urls": [
            "https://www.microworkers.com",
        ],
        "steps": [
            "Regístrate gratuitamente; proceso de aprobación rápido.",
            "Elige tareas de app testing, búsquedas, formularios o reseñas cortas.",
            "Algunas tareas toman menos de 5 minutos.",
            "Retiro vía PayPal, Skrill o cripto al alcanzar el mínimo.",
            "Ideal para principiantes; más de 2 millones de trabajadores activos.",
        ],
    },
    "remotasks": {
        "name": "Remotasks (etiquetado de datos e IA)",
        "category": "microtask",
        "urls": [
            "https://www.remotasks.com",
        ],
        "steps": [
            "Regístrate y completa el entrenamiento gratuito para acceder a tareas.",
            "Tareas: etiquetado de imágenes, transcripción, anotación 3D, revisión de contenido.",
            "Pago semanal vía PayPal.",
            "Mejor calidad de trabajo = acceso a tareas mejor pagadas.",
            "Rango típico: $3-$7 USD/hora según precisión y velocidad.",
        ],
    },
    "usertesting": {
        "name": "UserTesting (pruebas de UX / sitios web)",
        "category": "microtask",
        "urls": [
            "https://www.usertesting.com/be-a-user-tester",
        ],
        "steps": [
            "Regístrate y completa una prueba de práctica para ser aprobado.",
            "Cada sesión de prueba paga entre $10-$60 USD.",
            "Las pruebas incluyen navegar sitios web y dar feedback en voz alta.",
            "Requiere micrófono; algunas requieren cámara.",
            "Pago vía PayPal a los 14 días de completar la prueba.",
            "Promedio reportado: ~$22.50 USD/hora en sesiones aprobadas.",
        ],
    },
    "prolific": {
        "name": "Prolific (encuestas académicas pagadas)",
        "category": "microtask",
        "urls": [
            "https://www.prolific.com",
        ],
        "steps": [
            "Regístrate y llena tu perfil demográfico completo.",
            "Recibirás notificaciones de estudios disponibles según tu perfil.",
            "Las encuestas suelen durar 5-30 minutos.",
            "Pago mínimo recomendado por Prolific es de $9 USD/hora.",
            "Retiro vía PayPal; umbral mínimo bajo (~$5).",
            "Verifica disponibilidad en México antes de registrarte.",
        ],
    },
}

CATEGORIES = {
    "learn_earn": "Learn & Earn / Cripto",
    "microtask": "Microtask Platforms",
}

HTML_TEMPLATE = """<!doctype html>
<html lang=\"es\"><meta charset=\"utf-8\"><title>Panel Learn & Earn + Microtasks</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#111;color:#eee;padding:24px;line-height:1.6;max-width:860px;margin:0 auto}}
h1{{color:#7dd3fc}} h2{{color:#a5f3fc}} h3{{color:#86efac;margin:18px 0 6px}}
.card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:16px;margin:14px 0}}
a{{color:#7dd3fc;text-decoration:none}} a:hover{{text-decoration:underline}}
code{{background:#222;padding:2px 6px;border-radius:6px;font-size:.9em}}
.warn{{background:#2d1a00;border:1px solid #7c4a03;border-radius:8px;padding:10px 14px;margin:8px 0;color:#fbbf24}}
.badge{{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.75em;margin-left:6px;vertical-align:middle}}
.badge-earn{{background:#1e3a5f;color:#7dd3fc}}
.badge-micro{{background:#14532d;color:#86efac}}
ul{{padding-left:1.2em}}
</style>
<h1>Panel: Learn & Earn + Microtasks</h1>
<p>Este panel concentra enlaces y pasos seguros. <strong>No automatiza KYC, quizzes ni transacciones.</strong></p>

<div class=\"card\">
<h2>Learn & Earn <span class=\"badge badge-earn\">cripto</span></h2>
<h3>Coinbase</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.coinbase.com/earn\">Coinbase Earn</a> &nbsp;|
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.coinbase.com/wallet/quests\">Wallet Quests</a>
<h3>Binance</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.binance.com/en/academy/learn-and-earn\">Binance Academy Learn & Earn</a>
<h3>Kraken</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.kraken.com/earn\">Kraken Earn</a> &nbsp;|
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://support.kraken.com/hc/en-us/categories/200122606-Funding\">Soporte</a>
<div class=\"warn\">&#9888; Kraken Earn requiere depositar cripto (staking). Verifica disponibilidad en México.</div>
</div>

<div class=\"card\">
<h2>Microtask Platforms <span class=\"badge badge-micro\">$USD</span></h2>
<h3>Clickworker</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://workplace.clickworker.com/en/worker_registrations/new\">Registrarse</a> &nbsp;|
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://workplace.clickworker.com\">Plataforma</a> &mdash; Escritura, datos, IA. Pago semanal PayPal/Payoneer.
<h3>Microworkers</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.microworkers.com\">microworkers.com</a> &mdash; Tareas rápidas, testing, formularios. Retiro PayPal/cripto.
<h3>Remotasks</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.remotasks.com\">remotasks.com</a> &mdash; Etiquetado de datos e IA. Pago semanal PayPal. ~$3-7/hr.
<h3>UserTesting</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.usertesting.com/be-a-user-tester\">usertesting.com</a> &mdash; Pruebas UX. ~$10-60/sesión. ~$22.50/hr promedio.
<h3>Prolific</h3>
<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.prolific.com\">prolific.com</a> &mdash; Encuestas académicas. Mín. $9/hr. Retiro PayPal desde ~$5.
</div>

<div class=\"card\"><h2>Reglas de uso</h2><ul>
<li>Login manual siempre.</li>
<li>No automatices wallet ni aprobaciones de transacciones.</li>
<li>Confirma recompensas y mínimos de retiro antes de continuar.</li>
<li>Verifica disponibilidad regional (especialmente México).</li>
</ul></div>

<div class=\"card\"><h2>Comandos rápidos</h2>
<code>python learn_earn_helper.py --all --panel</code><br><br>
<code>python learn_earn_helper.py --category microtask --panel</code><br><br>
<code>python learn_earn_helper.py --category learn_earn --panel</code><br><br>
<code>python learn_earn_helper.py clickworker --print-only</code>
</div>
</html>"""


def save_panel(path: Path):
    path.write_text(HTML_TEMPLATE, encoding="utf-8")
    print(f"Panel HTML guardado en: {path.resolve()}")


def run_task(key: str, delay: float, print_only: bool):
    task = TASKS[key]
    cat = CATEGORIES.get(task["category"], task["category"])
    print(f"\n{'='*55}")
    print(f"[{cat}] {task['name']}")
    print("Pasos a seguir:")
    for i, step in enumerate(task["steps"], 1):
        print(f"  {i}. {step}")
    if print_only:
        return
    print("Abriendo URLs...")
    for url in task["urls"]:
        print(f"  -> {url}")
        webbrowser.open(url)
        time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(
        description="Asistente semiautomático para plataformas Learn & Earn y Microtasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python learn_earn_helper.py --all --panel\n"
            "  python learn_earn_helper.py --category microtask\n"
            "  python learn_earn_helper.py clickworker --print-only\n"
            "  python learn_earn_helper.py coinbase_earn --panel"
        )
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "platform",
        nargs="?",
        choices=sorted(TASKS.keys()),
        help="Plataforma específica"
    )
    group.add_argument("--all", action="store_true", help="Abre todas las plataformas")
    group.add_argument(
        "--category",
        choices=sorted(CATEGORIES.keys()),
        help="Abre solo plataformas de una categoría: learn_earn | microtask"
    )

    parser.add_argument("--print-only", action="store_true", help="Solo imprime pasos, no abre nada")
    parser.add_argument("--delay", type=float, default=1.5, help="Segundos entre apertura de URLs (default: 1.5)")
    parser.add_argument("--panel", action="store_true", help="Genera panel HTML local")
    args = parser.parse_args()

    print(BANNER)

    if args.panel:
        save_panel(Path("learn_earn_panel.html"))

    if args.all:
        keys = sorted(TASKS.keys())
        print(f"Modo --all: {len(keys)} plataformas")
        for key in keys:
            run_task(key, args.delay, args.print_only)
    elif args.category:
        keys = [k for k, v in TASKS.items() if v["category"] == args.category]
        label = CATEGORIES[args.category]
        print(f"Categoría [{label}]: {len(keys)} plataformas")
        for key in keys:
            run_task(key, args.delay, args.print_only)
    else:
        run_task(args.platform, args.delay, args.print_only)

    if not args.print_only:
        print("\nListo. Completa manualmente login, KYC, quizzes y transacciones.")
    else:
        print("\nModo solo-lectura completado.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
