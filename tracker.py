#!/usr/bin/env python3
"""
Tracker de progreso para Learn & Earn + Microtasks.
Guarda el historial en tracker_data.json.
Compatible con Python 3.8+
"""
import csv, json, sys, argparse
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tracker_data.json")

PLATFORMS = [
    "coinbase_earn", "binance_learn", "kraken_earn",
    "clickworker", "microworkers", "remotasks", "usertesting", "prolific"
]

PLATFORM_NAMES = {
    "coinbase_earn": "Coinbase Earn / Wallet Quests",
    "binance_learn": "Binance Academy Learn & Earn",
    "kraken_earn":   "Kraken Earn",
    "clickworker":   "Clickworker",
    "microworkers":  "Microworkers",
    "remotasks":     "Remotasks",
    "usertesting":   "UserTesting",
    "prolific":      "Prolific",
}


def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"goal": 5.0, "entries": []}


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_log(args) -> None:
    data = load_data()
    if args.platform not in PLATFORMS:
        print(f"Plataforma desconocida: {args.platform}. Opciones: {', '.join(PLATFORMS)}")
        sys.exit(1)
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "platform": args.platform,
        "amount": round(args.amount, 4),
        "currency": args.currency.upper(),
        "note": args.note or "",
    }
    data["entries"].append(entry)
    save_data(data)
    total = sum(e["amount"] for e in data["entries"] if e["currency"] == "USD")
    goal = data.get("goal", 5.0)
    remaining = max(0, goal - total)
    print(f"\n Registrado: ${args.amount:.2f} {entry['currency']} en {PLATFORM_NAMES[args.platform]}")
    print(f" Total USD acumulado: ${total:.2f} / ${goal:.2f}")
    print(f" Faltante para meta:  ${remaining:.2f}")
    if total >= goal:
        print("\n META ALCANZADA. Has superado los $5 USD.")


def cmd_summary(args) -> None:
    data = load_data()
    entries = data.get("entries", [])
    goal = data.get("goal", 5.0)
    if not entries:
        print("No hay entradas registradas aun. Usa: python tracker.py log <plataforma> <monto>")
        return
    total_usd = sum(e["amount"] for e in entries if e["currency"] == "USD")
    print(f"\n{'='*55}")
    print(f" RESUMEN DE PROGRESO")
    print(f" Meta: ${goal:.2f} USD")
    print(f" Total acumulado (USD): ${total_usd:.2f}")
    print(f" Progreso: {min(100, (total_usd/goal)*100):.1f}%")
    print(f" Entradas: {len(entries)}")
    print(f"{'='*55}")
    by_platform: dict = {}
    for e in entries:
        key = (e["platform"], e["currency"])
        by_platform[key] = by_platform.get(key, 0.0) + e["amount"]
    print("\n Por plataforma:")
    for (plat, curr), total in sorted(by_platform.items(), key=lambda x: -x[1]):
        print(f"  {PLATFORM_NAMES.get(plat, plat):35s} ${total:.2f} {curr}")
    print("\n Ultimas 5 entradas:")
    for e in entries[-5:]:
        note = f" ({e['note']})" if e.get("note") else ""
        print(f"  {e['date']}  {PLATFORM_NAMES.get(e['platform'], e['platform']):30s}  ${e['amount']:.2f} {e['currency']}{note}")
    if total_usd >= goal:
        print(f"\n META ALCANZADA: ${total_usd:.2f} / ${goal:.2f}")
    else:
        print(f"\n Falta: ${total_usd - goal + goal - total_usd:.2f} USD. Faltan ${goal - total_usd:.2f} para la meta.")


def cmd_export(args) -> None:
    data = load_data()
    entries = data.get("entries", [])
    if not entries:
        print("No hay entradas para exportar.")
        return
    out = Path(args.output)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "platform", "platform_name", "amount", "currency", "note"])
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "date": e["date"],
                "platform": e["platform"],
                "platform_name": PLATFORM_NAMES.get(e["platform"], e["platform"]),
                "amount": e["amount"],
                "currency": e["currency"],
                "note": e.get("note", ""),
            })
    print(f" Exportado {len(entries)} entradas a: {out.resolve()}")


def cmd_set_goal(args) -> None:
    data = load_data()
    data["goal"] = round(args.amount, 2)
    save_data(data)
    print(f"Meta actualizada a: ${args.amount:.2f} USD")


def cmd_reset(args) -> None:
    confirm = input("Esto borrara todo el historial. Escribe 'si' para confirmar: ").strip().lower()
    if confirm == "si":
        save_data({"goal": 5.0, "entries": []})
        print("Historial borrado.")
    else:
        print("Cancelado.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tracker de progreso para Learn & Earn + Microtasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python tracker.py log clickworker 2.50\n"
            "  python tracker.py log usertesting 10.00 --note 'prueba UX'\n"
            "  python tracker.py summary\n"
            "  python tracker.py export\n"
            "  python tracker.py export --output mis_ganancias.csv\n"
            "  python tracker.py set-goal 10\n"
            "  python tracker.py reset"
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Registrar un ingreso")
    p_log.add_argument("platform", choices=PLATFORMS)
    p_log.add_argument("amount", type=float)
    p_log.add_argument("--currency", default="USD")
    p_log.add_argument("--note", default="")
    p_log.set_defaults(func=cmd_log)

    p_sum = sub.add_parser("summary", help="Ver resumen de progreso")
    p_sum.set_defaults(func=cmd_summary)

    p_exp = sub.add_parser("export", help="Exportar historial a CSV")
    p_exp.add_argument("--output", default="tracker_export.csv", help="Archivo de salida (default: tracker_export.csv)")
    p_exp.set_defaults(func=cmd_export)

    p_goal = sub.add_parser("set-goal", help="Cambiar la meta en USD")
    p_goal.add_argument("amount", type=float)
    p_goal.set_defaults(func=cmd_set_goal)

    p_reset = sub.add_parser("reset", help="Borrar todo el historial")
    p_reset.set_defaults(func=cmd_reset)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
