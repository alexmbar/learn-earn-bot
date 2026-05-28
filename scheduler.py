#!/usr/bin/env python3
"""
Scheduler para abrir plataformas Learn & Earn / Microtasks automáticamente.

Modos:
  once      - Abre plataformas una vez ahora.
  daily     - Abre todos los días a la hora especificada (HH:MM).
  interval  - Abre cada N horas.
  cron      - Imprime el comando cron equivalente para configurar en el sistema.

Ejemplos:
  python scheduler.py once --category microtask
  python scheduler.py daily --time 09:00
  python scheduler.py daily --time 09:00 --category microtask
  python scheduler.py interval --hours 6
  python scheduler.py cron --time 09:00
"""
import argparse, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path

HELPER = Path(__file__).parent / "learn_earn_helper.py"


def build_helper_cmd(category: str | None, platform: str | None, print_only: bool, panel: bool, delay: float) -> list:
    cmd = [sys.executable, str(HELPER)]
    if platform:
        cmd.append(platform)
    elif category:
        cmd += ["--category", category]
    else:
        cmd.append("--all")
    if print_only:
        cmd.append("--print-only")
    if panel:
        cmd.append("--panel")
    cmd += ["--delay", str(delay)]
    return cmd


def run_once(args):
    cmd = build_helper_cmd(args.category, getattr(args, "platform", None), args.print_only, args.panel, args.delay)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd)


def seconds_until(target_time: str) -> float:
    now = datetime.now()
    h, m = map(int, target_time.split(":"))
    target = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def cmd_once(args):
    run_once(args)


def cmd_daily(args):
    print(f"Scheduler diario activo: se ejecutará todos los días a las {args.time}")
    print("Presiona Ctrl+C para detener.")
    while True:
        wait = seconds_until(args.time)
        next_run = datetime.now() + timedelta(seconds=wait)
        print(f"Próxima ejecución: {next_run.strftime('%Y-%m-%d %H:%M:%S')} (en {int(wait//3600)}h {int((wait%3600)//60)}m)")
        time.sleep(wait)
        run_once(args)


def cmd_interval(args):
    interval_secs = args.hours * 3600
    print(f"Scheduler de intervalo: se ejecutará cada {args.hours} hora(s).")
    print("Presiona Ctrl+C para detener.")
    while True:
        run_once(args)
        next_run = datetime.now() + timedelta(seconds=interval_secs)
        print(f"Próxima ejecución: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(interval_secs)


def cmd_cron(args):
    h, m = args.time.split(":")
    script = Path(__file__).resolve()
    helper = HELPER.resolve()
    cat_flag = f"--category {args.category}" if args.category else "--all"
    cron_line = f"{m} {h} * * * {sys.executable} {script} once {cat_flag}"
    print("\nAgrega esta línea a tu crontab (ejecuta: crontab -e):\n")
    print(f"  {cron_line}")
    print(f"\nO para abrir el helper directamente:")
    print(f"  {m} {h} * * * {sys.executable} {helper} {cat_flag}")
    print("\nNota: en cron las variables de entorno y el display pueden requerir configuración adicional (DISPLAY, PATH).")


def main():
    parser = argparse.ArgumentParser(
        description="Scheduler para abrir plataformas Learn & Earn / Microtasks automáticamente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python scheduler.py once\n"
            "  python scheduler.py once --category microtask --print-only\n"
            "  python scheduler.py daily --time 09:00\n"
            "  python scheduler.py daily --time 09:00 --category microtask\n"
            "  python scheduler.py interval --hours 6\n"
            "  python scheduler.py cron --time 09:00"
        )
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # Opciones comunes
    def add_common(p):
        p.add_argument("--category", choices=["learn_earn", "microtask"], default=None,
                       help="Categoría: learn_earn | microtask (default: todas)")
        p.add_argument("--platform", default=None, help="Plataforma individual (opcional)")
        p.add_argument("--print-only", action="store_true", help="Solo imprime pasos, no abre navegador")
        p.add_argument("--panel", action="store_true", help="Genera panel HTML")
        p.add_argument("--delay", type=float, default=1.5, help="Segundos entre URLs")

    # once
    p_once = sub.add_parser("once", help="Ejecutar una vez ahora")
    add_common(p_once)
    p_once.set_defaults(func=cmd_once)

    # daily
    p_daily = sub.add_parser("daily", help="Ejecutar todos los días a la hora indicada")
    p_daily.add_argument("--time", default="09:00", help="Hora de ejecución HH:MM (default: 09:00)")
    add_common(p_daily)
    p_daily.set_defaults(func=cmd_daily)

    # interval
    p_interval = sub.add_parser("interval", help="Ejecutar cada N horas")
    p_interval.add_argument("--hours", type=float, default=24, help="Intervalo en horas (default: 24)")
    add_common(p_interval)
    p_interval.set_defaults(func=cmd_interval)

    # cron
    p_cron = sub.add_parser("cron", help="Imprimir linea cron equivalente")
    p_cron.add_argument("--time", default="09:00", help="Hora HH:MM para el cron (default: 09:00)")
    p_cron.add_argument("--category", choices=["learn_earn", "microtask"], default=None)
    p_cron.set_defaults(func=cmd_cron)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nScheduler detenido.")
        sys.exit(0)


if __name__ == "__main__":
    main()
