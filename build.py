"""Baut die statische Website nach _site/ (für GitHub Pages).

    python build.py            # prüfen (datencheck) und bauen
    python build.py --serve    # bauen, lokal unter http://127.0.0.1:8000 anzeigen und bei Änderungen neu bauen
"""
from __future__ import annotations

import argparse
import functools
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

from datencheck import pruefen
from grenzgaenger.data import DATEN_DATEI, DOCS_DIR
from grenzgaenger.site import BuildFehler, bauen

PROJEKT = Path(__file__).resolve().parent
ZIEL = PROJEKT / "_site"
BEOBACHTET = [DOCS_DIR, PROJEKT / "grenzgaenger"]


def build(still_pruefen: bool = False) -> bool:
    ausgabe = (lambda *_: None) if still_pruefen else print
    if not pruefen(DATEN_DATEI, ausgabe=ausgabe):
        if still_pruefen:
            pruefen(DATEN_DATEI)  # Fehler doch anzeigen
        print("Build abgebrochen: Daten enthalten Fehler (siehe oben).")
        return False
    try:
        bauen(ZIEL)
    except BuildFehler as exc:
        print(f"Build abgebrochen: {exc}")
        return False
    return True


def stempel() -> float:
    dateien = [PROJEKT / "build.py", PROJEKT / "datencheck.py"]
    dateien += [p for d in BEOBACHTET for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    return max((p.stat().st_mtime for p in dateien if p.exists()), default=0)


def beobachten():
    letzter = stempel()
    while True:
        time.sleep(1)
        jetzt = stempel()
        if jetzt != letzter:
            letzter = jetzt
            print(time.strftime("%H:%M:%S"), "Änderung erkannt – baue neu …")
            # In einem frischen Prozess bauen: so werden auch Änderungen am Code (grenzgaenger/*.py) übernommen,
            # nicht nur an Daten und Vorlagen.
            erg = subprocess.run([sys.executable, str(PROJEKT / "build.py"), "--still"], cwd=PROJEKT)
            if erg.returncode:
                print("Fehler beim Bauen – die Vorschau zeigt den letzten funktionierenden Stand.")


def serve(port: int):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ZIEL))
    handler.log_message = lambda *a, **k: None
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Vorschau: http://127.0.0.1:{port}/  (Strg+C beendet) – Änderungen in docs/ und grenzgaenger/ werden automatisch übernommen.")
        threading.Thread(target=beobachten, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--serve", action="store_true", help="lokale Vorschau mit automatischem Neubau")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--still", action="store_true", help=argparse.SUPPRESS)  # intern: Neubau aus der Vorschau
    args = parser.parse_args()
    if not build(still_pruefen=args.still):
        return 1
    if args.serve:
        serve(args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
