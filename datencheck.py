"""Prüft docs/ki_tools_verzeichnis.json auf Fehler und Unstimmigkeiten.

    python datencheck.py          # nur prüfen
    python datencheck.py --fix    # Zähler (meta.anzahl, anzahl_pruefpunkte) automatisch korrigieren

Exit-Code 1 bei Fehlern (wird auch vom Build und von GitHub Actions verwendet).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from grenzgaenger.data import DATEN_DATEI, KATEGORIEN, ampel, datenhaltung_key

DATENHALTUNG_WERTE = {"CH möglich", "EU/EWR(+CH) möglich", "EU bedingt", "USA/Global", "China", "unklar – prüfen"}
DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PRUEFZYKLUS_TAGE = 45
LEISTUNG_WERT = re.compile(r"^(Spitze|Stark|Basis|Prüfen|–|n/a)(\b|\s|$)")


def zaehle_pruefpunkte(e: dict) -> int:
    return sum(1 for v in e.values() if isinstance(v, str) and v.strip().startswith("Prüfen"))


def pruefen(path: Path, fix: bool = False, ausgabe=print) -> bool:
    """Gibt True zurück, wenn keine Fehler gefunden wurden."""
    try:
        with open(path, encoding="utf-8") as f:
            roh = json.load(f)
    except json.JSONDecodeError as exc:
        ausgabe(f"FEHLER   Ungültiges JSON: {exc}")
        return False

    fehler, warnungen = [], []
    meta = roh.get("meta") or {}
    eintraege = roh.get("eintraege")
    if not isinstance(eintraege, list):
        ausgabe("FEHLER   'eintraege' fehlt oder ist keine Liste.")
        return False
    felder = list((meta.get("felder") or {}).keys())
    if not felder:
        fehler.append("meta.felder fehlt – darin stehen die Feldnamen und Beschriftungen.")
    if not DATUM.match(str(meta.get("stand", ""))):
        fehler.append("meta.stand muss ein Datum im Format JJJJ-MM-TT sein.")

    for i, n in Counter(e.get("id") for e in eintraege).items():
        if n > 1:
            fehler.append(f"ID doppelt: {i} ({n}x)")

    heute = date.today()
    korrigiert = 0
    for idx, e in enumerate(eintraege):
        tid = e.get("id") or f"#{idx}"
        fehlend = [k for k in felder if k not in e]
        extra = [k for k in e if felder and k not in felder]
        if fehlend:
            fehler.append(f"{tid}: Felder fehlen: {', '.join(fehlend)}")
        if extra:
            warnungen.append(f"{tid}: unbekannte Felder (werden nicht angezeigt): {', '.join(extra)}")
        if not ID.match(str(e.get("id", ""))):
            fehler.append(f"{tid}: ID nur aus Kleinbuchstaben, Ziffern und Bindestrichen (z.B. ch-anbieter-produkt)")
        if not e.get("name"):
            fehler.append(f"{tid}: name ist leer")
        if e.get("datenhaltung_filter") not in DATENHALTUNG_WERTE:
            fehler.append(f"{tid}: datenhaltung_filter '{e.get('datenhaltung_filter')}' – erlaubt: {', '.join(sorted(DATENHALTUNG_WERTE))}")
        for feld in ("ampel_personendaten", "ampel_berufsgeheimnis"):
            v = e.get(feld, "")
            if ampel(v)["key"] == "offen" and not str(v).lower().startswith("offen"):
                fehler.append(f"{tid}: {feld} '{v}' unbekannt – erlaubt: grün, gelb, orange, rot, offen, Abhängig (optional mit Zusatz in Klammern)")
        for feld in ("leistung_ch", "leistung_eu", "leistung_global"):
            if feld in e and not LEISTUNG_WERT.match(str(e.get(feld, ""))):
                fehler.append(f"{tid}: {feld} '{e.get(feld)}' – erlaubt: Spitze, Stark, Basis, Prüfen, – (nicht möglich), n/a (optional mit Zusatz in Klammern)")
        if str(e.get("ch_only_moeglich", "")).lower().startswith("nein") and str(e.get("leistung_ch", "")).split(" ")[0] in ("Spitze", "Stark", "Basis"):
            warnungen.append(f"{tid}: leistung_ch ist gesetzt, aber ch_only_moeglich beginnt mit 'Nein' (sollte '–' sein)")
        kat = e.get("kategorie", "")
        if kat and kat not in KATEGORIEN:
            warnungen.append(f"{tid}: Kategorie '{kat}' ist unbekannt (erscheint unter 'Weitere'). In grenzgaenger/data.py bei KATEGORIEN und GRUPPEN ergänzen.")
        stand = str(e.get("stand", ""))
        if not DATUM.match(stand):
            fehler.append(f"{tid}: stand '{stand}' muss JJJJ-MM-TT sein")
        else:
            alter = (heute - date.fromisoformat(stand)).days
            if alter > PRUEFZYKLUS_TAGE:
                warnungen.append(f"{tid}: zuletzt geprüft vor {alter} Tagen (Prüfzyklus {PRUEFZYKLUS_TAGE} Tage)")
        for q in [x.strip() for x in str(e.get("quellen", "")).split("|") if x.strip()]:
            if not q.startswith(("http://", "https://")):
                fehler.append(f"{tid}: Quelle ist keine URL: {q}")
        if not e.get("quellen"):
            warnungen.append(f"{tid}: keine Quellen angegeben")

        # Konsistenz Datenhaltung <-> Detailfelder
        dh = datenhaltung_key(e.get("datenhaltung_filter", ""))
        ch = str(e.get("ch_only_moeglich", "")).lower()
        if dh == "ch" and ch.startswith("nein"):
            warnungen.append(f"{tid}: datenhaltung_filter ist 'CH möglich', aber ch_only_moeglich beginnt mit 'Nein'")
        if dh in ("us", "cn") and ch.startswith("ja"):
            warnungen.append(f"{tid}: ch_only_moeglich ist 'Ja', aber datenhaltung_filter ist {e.get('datenhaltung_filter')}")

        soll = zaehle_pruefpunkte(e)
        if e.get("anzahl_pruefpunkte") != soll:
            if fix:
                e["anzahl_pruefpunkte"] = soll
                korrigiert += 1
            else:
                warnungen.append(f"{tid}: anzahl_pruefpunkte={e.get('anzahl_pruefpunkte')}, gezählt {soll} (mit --fix korrigieren)")

    if meta.get("anzahl") != len(eintraege):
        if fix:
            meta["anzahl"] = len(eintraege)
            korrigiert += 1
        else:
            warnungen.append(f"meta.anzahl={meta.get('anzahl')}, tatsächlich {len(eintraege)} (mit --fix korrigieren)")

    if fix and korrigiert and not fehler:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(roh, f, ensure_ascii=False, indent=2)
            f.write("\n")
        ausgabe(f"{korrigiert} Zähler korrigiert und gespeichert.")

    for w in warnungen:
        ausgabe(f"WARNUNG  {w}")
    for x in fehler:
        ausgabe(f"FEHLER   {x}")

    offen_total = sum(zaehle_pruefpunkte(e) for e in eintraege)
    dh = Counter(e.get("datenhaltung_filter") for e in eintraege)
    ausgabe("")
    ausgabe(f"{len(eintraege)} Einträge · Stand {meta.get('stand')} · {offen_total} offene Prüfpunkte")
    ausgabe("Datenhaltung: " + ", ".join(f"{k}: {v}" for k, v in dh.most_common()))
    if fehler:
        ausgabe(f"{len(fehler)} Fehler gefunden – bitte korrigieren.")
        return False
    ausgabe(f"OK – keine Fehler ({len(warnungen)} Warnungen).")
    return True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Prüft die JSON-Daten des KI-Tool-Verzeichnisses.")
    parser.add_argument("--fix", action="store_true", help="meta.anzahl und anzahl_pruefpunkte neu berechnen und speichern")
    parser.add_argument("--datei", default=str(DATEN_DATEI))
    args = parser.parse_args()
    return 0 if pruefen(Path(args.datei), fix=args.fix) else 1


if __name__ == "__main__":
    sys.exit(main())
