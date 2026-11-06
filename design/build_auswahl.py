"""Erzeugt design/design-auswahl.html aus der Vorlage und den aktuellen Daten.

    .venv\\Scripts\\python design\\build_auswahl.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
daten = json.loads((ROOT / "docs" / "ki_tools_verzeichnis.json").read_text(encoding="utf-8"))
vorlage = (ROOT / "design" / "design-auswahl.template.html").read_text(encoding="utf-8")
js = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
assert "/*__DATA__*/null" in vorlage
(ROOT / "design" / "design-auswahl.html").write_text(vorlage.replace("/*__DATA__*/null", js), encoding="utf-8")
print("design/design-auswahl.html erstellt")
