"""Erzeugt das LinkedIn-Vorschaubild grenzgaenger/static/og-bild.png aus design/og-bild.html.

    .venv\\Scripts\\python design\\build_og_bild.py

Braucht Microsoft Edge oder Google Chrome (rendert die HTML-Vorlage headless als Screenshot).
Nur nötig, wenn das Bild geändert werden soll – das PNG liegt fertig im Projekt.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VORLAGE = ROOT / "design" / "og-bild.html"
ZIEL = ROOT / "grenzgaenger" / "static" / "og-bild.png"

KANDIDATEN = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "msedge", "google-chrome", "chromium", "chrome",
]
browser = next((k for k in KANDIDATEN if Path(k).exists() or shutil.which(k)), None)
if not browser:
    sys.exit("Kein Edge/Chrome gefunden.")
subprocess.run([browser, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                "--window-size=1200,627", f"--screenshot={ZIEL}", VORLAGE.as_uri()], check=True)
print(f"{ZIEL.relative_to(ROOT)} erstellt")
