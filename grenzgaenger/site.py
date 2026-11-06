"""Erzeugt die statische Website (für GitHub Pages) aus docs/.

Alle Links sind relativ – die Seite funktioniert darum unter
https://<name>.github.io/<repo>/ genauso wie lokal oder mit eigener Domain.
"""
from __future__ import annotations

import itertools
import json
import os
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined, pass_context, select_autoescape
from markupsafe import Markup, escape

from .data import (AMPEL, ANALYSE_GLOB, DATENHALTUNG, DOCS_DIR, FUNKTION_INFO, FUNKTIONEN, GRUPPE_RANG,
                   GRUPPEN, LEISTUNG, ORT_GRUPPEN, Verzeichnis, empfehlen, filtern, get_verzeichnis)
from .ui import icon, kann_auch

HIER = Path(__file__).resolve().parent
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
          "Dezember"]


class BuildFehler(Exception):
    pass


# ---------------------------------------------------------------------------
# Berater: drei Fragen. Jede Kombination wird als eigene Seite erzeugt:
#   /                                      Frage 1
#   /berater/personendaten/                Frage 2
#   /berater/personendaten/europa/         Frage 3
#   /berater/personendaten/europa/chat/    Ergebnis
# ---------------------------------------------------------------------------

FRAGEN = [
    {"key": "sens", "titel": "Mit welchen Daten möchten Sie die KI nutzen?", "hilfe": "Davon hängt am meisten ab.", "breit": False,
     "optionen": [
         ("", "doc", "Allgemeine Infos", "Texte, Ideen, Recherche – keine Kunden- oder Personendaten"),
         ("pd", "users", "Kunden- & Personendaten", "Namen, Adressen, Kundenakten, Mitarbeiterdaten"),
         ("bg", "lock", "Berufsgeheimnis", "Anwalt, Ärztin, Treuhand, Behörde"),
     ]},
    {"key": "ort", "titel": "Wo sollen Ihre Daten bleiben?", "hilfe": "Für die meisten KMU reicht Europa inkl. Schweiz.", "breit": False,
     "optionen": [
         ("ch", "ch", "Nur in der Schweiz", "Höchste Kontrolle, etwas kleinere Auswahl"),
         ("eu", "eu", "In Europa inkl. Schweiz", "Grösste Auswahl mit europäischem Datenschutz"),
         ("", "globe", "Ist mir egal", "Alle Angebote berücksichtigen"),
     ]},
    {"key": "bed", "titel": "Wofür möchten Sie KI einsetzen?", "hilfe": "Wählen Sie, was am besten passt.", "breit": True,
     "optionen": [
         ("chat", "chat", "Chatten & Texte schreiben", "Ein KI-Assistent für das ganze Team"),
         ("wissen", "doc", "Mit eigenen Dokumenten arbeiten", "Fragen an Ablage, Verträge, Handbücher stellen"),
         ("spezial", "tool", "Übersetzen, Meetings, Dokumente, Bilder", "Spezialisierte Werkzeuge"),
         ("api", "code", "In eigene Software einbauen", "Für Entwickler und IT (API)"),
         ("onprem", "server", "Auf eigenen Servern betreiben", "Maximale Kontrolle im eigenen Haus"),
         ("alle", "spark", "Ich schaue mich erst um", "Alle Arten von Tools zeigen"),
     ]},
]
# Antwort -> lesbarer Teil der Adresse, z.B. /berater/personendaten/europa/chat/.
# Achtung: Diese Namen stehen in geteilten Links – nach der Veröffentlichung nicht mehr ändern.
PFAD_NAMEN = {
    "sens": {"": "allgemein", "pd": "personendaten", "bg": "berufsgeheimnis"},
    "ort": {"ch": "schweiz", "eu": "europa", "": "egal"},
    "bed": {"chat": "chat", "wissen": "dokumente", "spezial": "spezialwerkzeuge", "api": "api",
            "onprem": "eigene-server", "alle": "alle"},
}
SENS_TEXT = {"": "allgemeine Infos", "pd": "Kunden- und Personendaten", "bg": "Daten unter Berufsgeheimnis"}
ORT_TEXT = {"ch": "in der Schweiz", "eu": "in Europa"}
# Kurzform für Seitentitel und LinkedIn-Vorschau eines Ergebnisses
TITEL_TEILE = {
    "sens": {"": "Allgemeine Infos", "pd": "Kundendaten", "bg": "Berufsgeheimnis"},
    "ort": {"ch": "Schweiz", "eu": "Europa", "": "Datenort egal"},
    "bed": {"chat": "Chat & Texte", "wissen": "Eigene Dokumente", "spezial": "Spezialwerkzeuge", "api": "API",
            "onprem": "Eigene Server", "alle": "Alle Tools"},
}


def berater_pfad(antworten: dict) -> str:
    teile = [PFAD_NAMEN[f["key"]][antworten[f["key"]]] for f in FRAGEN if f["key"] in antworten]
    return "berater/" + "".join(f"{t}/" for t in teile) if teile else ""


def berater_kontext(v: Verzeichnis, antworten: dict) -> dict:
    schritt = len(antworten)
    verlauf = []
    for i, frage in enumerate(FRAGEN[: schritt + 1]):
        eintrag = {"frage": frage, "nr": i + 1, "aktiv": i == schritt}
        bisher = {f["key"]: antworten[f["key"]] for f in FRAGEN[:i]}
        if i < schritt:
            wahl = next(o for o in frage["optionen"] if o[0] == antworten[frage["key"]])
            eintrag["antwort"] = {"icon": wahl[1], "label": wahl[2]}
            eintrag["aendern_pfad"] = berater_pfad(bisher)
        else:
            eintrag["optionen"] = [
                {"icon": ic, "label": label, "hilfe": hilfe, "pfad": berater_pfad({**bisher, frage["key"]: wert}),
                 "anzahl": len(filtern(v.tools, **bisher, **{frage["key"]: wert}))}
                for wert, ic, label, hilfe in frage["optionen"]
            ]
        verlauf.append(eintrag)

    ctx = {"verlauf": verlauf, "fragen_total": len(FRAGEN), "prog": range(1, len(FRAGEN) + 1),
           "fertig": schritt >= len(FRAGEN)}
    if ctx["fertig"]:
        sens = antworten.get("sens", "")
        ort = antworten.get("ort", "")
        liste = filtern(v.tools, **antworten)
        rollen, rest = empfehlen(liste, sens, ort, leistung=antworten.get("bed") != "spezial",
                                 nur_anwender=antworten.get("bed") == "alle")
        empf = [r["tool"] for r in rollen]
        rel = "bg" if sens == "bg" else "pd"
        ctx.update({
            "antworten": antworten, "liste": liste, "rollen": rollen, "empfehlungen": empf, "rest": rest, "ort_wahl": ort,
            "mit_leistung": any(r["leistung"]["punkte"] for r in rollen),
            "sens": sens, "rel": rel,
            "sens_text": SENS_TEXT.get(sens, ""), "ort_text": ORT_TEXT.get(antworten.get("ort", ""), ""),
            "verzeichnis_query": _verzeichnis_query(antworten),
        })
        # Eigener Titel und Text pro Ergebnis – das zeigt LinkedIn in der Vorschau eines geteilten Links
        ctx["seiten_titel"] = " · ".join(TITEL_TEILE[f["key"]][antworten[f["key"]]] for f in FRAGEN)
        if liste:
            namen = ", ".join(t.kurzname for t in empf)
            ort_satz = f", Daten {ctx['ort_text']}" if ctx["ort_text"] else ""
            ctx["seiten_text"] = (f"Für {ctx['sens_text']}{ort_satz}: {len(liste)} passende KI-Tools. "
                                  f"Empfehlungen: {namen}. Unabhängig, mit Ampeln für Datenschutz.")
        else:
            ctx["seiten_text"] = "Für diese Kombination gibt es kein passendes KI-Tool – mit Europa statt Schweiz ist die Auswahl grösser."
    return ctx


def _verzeichnis_query(antworten: dict) -> str:
    teile = []
    if antworten.get("sens"):
        teile.append(f"sens={antworten['sens']}")
    if antworten.get("ort") == "ch":
        teile.append("ort=ch")
    elif antworten.get("ort") == "eu":
        teile += ["ort=ch", "ort=eu"]
    return "?" + "&".join(teile) if teile else ""


def alle_berater_zustaende():
    """Alle Antwort-Kombinationen: 1 + 3 + 9 + 54 Seiten."""
    werte = [[o[0] for o in f["optionen"]] for f in FRAGEN]
    for tiefe in range(len(FRAGEN) + 1):
        for kombi in itertools.product(*werte[:tiefe]):
            yield {FRAGEN[i]["key"]: w for i, w in enumerate(kombi)}


# ---------------------------------------------------------------------------
# Verzeichnis: alle Tools werden ausgeliefert, gefiltert wird im Browser (app.js)
# ---------------------------------------------------------------------------


def verzeichnis_kontext(v: Verzeichnis) -> dict:
    total = len(v.tools)
    zaehler = v.zaehler()
    ort_leiste = []
    for key, label, keys in ORT_GRUPPEN:
        n = sum(zaehler[k] for k in keys)
        ort_leiste.append({"key": key, "label": label, "anzahl": n, "keys": keys,
                           "prozent": round(n / total * 100, 2) if total else 0})
    return {
        "tools": filtern(v.tools), "total": total, "ort_leiste": ort_leiste,
        "sens_optionen": [("", "Alle Daten"), ("pd", "Personendaten"), ("bg", "Berufsgeheimnis")],
        "art_optionen": [("", "Alle Arten", "spark")] + [(g["id"], g["label"], g["icon"]) for g in GRUPPEN],
        "funk_optionen": [FUNKTION_INFO[k] for k, *_ in FUNKTIONEN],
        "ampel_legende": [(k, AMPEL[k]["label"]) for k in ("gruen", "gelb", "orange", "rot", "offen")],
        "vz_config": {"orte": {o["key"]: o["keys"] for o in ort_leiste},
                      "leistung": {k: {"label": x["label"], "kurz": x["kurz"], "rang": x["rang"]} for k, x in LEISTUNG.items()}},
        "gruppe_rang": GRUPPE_RANG,
    }


# ---------------------------------------------------------------------------
# Marktanalyse (Markdown aus docs/)
# ---------------------------------------------------------------------------


def _slug(value, separator="-"):
    value = value.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        value = value.replace(a, b)
    return re.sub(r"[^a-z0-9]+", separator, value).strip(separator)


def analyse_platzhalter(v: Verzeichnis) -> dict:
    """Zahlen, die in der Marktanalyse als {{ name }} verwendet werden können."""
    region = {k: 0 for k in ("Schweiz", "EU/EWR", "USA")}
    for t in v.tools:
        r = t.raw.get("region_anbieter", "")
        if r in region:
            region[r] += 1
    z = v.zaehler()
    return {
        "anzahl": len(v.tools),
        "anzahl_schweiz": region["Schweiz"],
        "anzahl_europa": region["EU/EWR"],
        "anzahl_usa": region["USA"],
        "anzahl_andere": len(v.tools) - sum(region.values()),
        "anzahl_ch_moeglich": z["ch"],
        "anzahl_eu_moeglich": z["eu"],
        "anzahl_ch_oder_eu": z["ch"] + z["eu"],
        "anzahl_vischer": sum(t.vischer for t in v.tools),
        "anzahl_pruefpunkte": sum(t.pruefpunkte for t in v.tools),
        "stand": datum_lang(v.stand),
    }


def analyse_html(v: Verzeichnis, root: str):
    files = sorted(DOCS_DIR.glob(ANALYSE_GLOB))
    if not files:
        return None, "", []
    text = files[-1].read_text(encoding="utf-8")
    werte = analyse_platzhalter(v)

    def ersetzen(m):
        name = m.group(1)
        if name not in werte:
            raise BuildFehler(f"Marktanalyse: unbekannter Platzhalter {{{{ {name} }}}} – erlaubt: {', '.join(werte)}")
        return str(werte[name])

    text = re.sub(r"\{\{\s*(\w+)\s*\}\}", ersetzen, text)
    lines = text.splitlines()
    titel = lines.pop(0)[2:].strip() if lines and lines[0].startswith("# ") else ""
    html = markdown.markdown("\n".join(lines), extensions=["tables", "sane_lists", "toc"],
                             extension_configs={"toc": {"slugify": _slug}})
    html = html.replace("<li>[ ] ", '<li class="todo">').replace("<li>[x] ", '<li class="todo erledigt">')

    # Interne Links: [Name](tool:<id>) und [Text](seite:verzeichnis|grundlagen|berater)
    def intern(m):
        art, ziel = m.group(1), m.group(2)
        if art == "tool":
            if ziel not in v.by_id:
                raise BuildFehler(f"Marktanalyse verlinkt unbekanntes Tool: tool:{ziel}")
            return f'href="{root}tool/{ziel}/" data-drawer'
        seiten = {"verzeichnis": "verzeichnis/", "grundlagen": "grundlagen/", "berater": ""}
        if ziel.split("?")[0] not in seiten:
            raise BuildFehler(f"Marktanalyse verlinkt unbekannte Seite: seite:{ziel}")
        basis, _, query = ziel.partition("?")
        return f'href="{root}{seiten[basis] or "./"}{"?" + query if query else ""}"'

    html = re.sub(r'href="(tool|seite):([^"]+)"', intern, html)
    html = html.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html)
    return titel, html, toc


# ---------------------------------------------------------------------------
# Template-Umgebung
# ---------------------------------------------------------------------------


def datum_lang(d) -> str:
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return d
    if not d:
        return ""
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}"


def domain(url: str) -> str:
    try:
        return url.split("//", 1)[1].split("/", 1)[0].removeprefix("www.")
    except IndexError:
        return url


def ton_icon(ton: str) -> str:
    return {"gut": "✓", "schlecht": "✕", "mittel": "!"}.get(ton, "?")


def json_script(wert, element_id: str) -> Markup:
    daten = json.dumps(wert, ensure_ascii=False).replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    return Markup(f'<script id="{escape(element_id)}" type="application/json">{daten}</script>')


@pass_context
def url(ctx, ziel: str = "") -> str:
    """Relativer Link von der aktuellen Seite zu `ziel` (z.B. 'verzeichnis/', 'tool/x/')."""
    return (ctx["root"] + ziel) or "./"


def umgebung() -> Environment:
    env = Environment(loader=FileSystemLoader(HIER / "templates"), autoescape=select_autoescape(["html"]),
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    env.globals.update(icon=icon, kann_auch=kann_auch, url=url)
    env.filters.update(datum=datum_lang, domain=domain, ton_icon=ton_icon, json_script=json_script)
    return env


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


def adressen() -> tuple[str, str]:
    """Öffentliche Adresse der Website und des GitHub-Repositorys.

    Beide setzt der GitHub-Workflow automatisch (.github/workflows/pages.yml). Bei eigener Domain
    GRENZGAENGER_SITE_URL dort überschreiben, z.B. https://ki-grenzgaenger.ch/
    """
    site = os.environ.get("GRENZGAENGER_SITE_URL", "").strip()
    repo = os.environ.get("GRENZGAENGER_REPO_URL", "").strip().rstrip("/") or _repo_aus_git()
    return (site.rstrip("/") + "/" if site else ""), repo


def _repo_aus_git() -> str:
    """Lokal: Repo-Adresse aus `git remote` lesen, damit «Fehler melden» auch in der Vorschau verlinkt ist."""
    try:
        erg = subprocess.run(["git", "remote", "get-url", "origin"], cwd=HIER.parent, capture_output=True,
                             text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    url = erg.stdout.strip() if erg.returncode == 0 else ""
    m = re.match(r"(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?/?$", url)
    return f"https://github.com/{m.group(1)}" if m else ""


def bauen(ziel: Path, log=print) -> int:
    # Nicht den ganzen Ordner löschen (unter Windows sperrt z.B. die laufende Vorschau einzelne Dateien),
    # sondern alles überschreiben und am Schluss nur veraltete Dateien entfernen.
    v = get_verzeichnis()
    ziel.mkdir(parents=True, exist_ok=True)
    env = umgebung()
    site_url, repo_url = adressen()
    if not site_url:
        log("Hinweis: GRENZGAENGER_SITE_URL ist nicht gesetzt – die LinkedIn-Vorschau braucht die öffentliche Adresse "
            "(auf GitHub wird sie automatisch gesetzt).")
    basis = {"daten_stand": v.stand, "daten_anzahl": len(v.tools), "daten_hinweis": v.meta.get("hinweis", ""),
             "site_url": site_url, "repo_url": repo_url,
             "daten_geprueft": sum(1 for t in v.tools if t.pruefpunkte == 0)}
    seiten = 0
    geschrieben: set[Path] = set()

    def datei_schreiben(out: Path, text: str):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        geschrieben.add(out.resolve())

    def schreiben(pfad: str, template: str, datei: str = "index.html", **ctx):
        nonlocal seiten
        tiefe = pfad.count("/")
        html = env.get_template(template).render(**basis, root="../" * tiefe, pfad=pfad, **ctx)
        datei_schreiben(ziel / pfad / datei, html)
        seiten += 1

    # Berater (Startseite + alle Antwort-Kombinationen)
    for antworten in alle_berater_zustaende():
        schreiben(berater_pfad(antworten), "berater.html", seite="berater", **berater_kontext(v, antworten))

    # Verzeichnis
    schreiben("verzeichnis/", "verzeichnis.html", seite="verzeichnis", **verzeichnis_kontext(v))

    # Steckbriefe: ganze Seite + Fragment für die Schublade
    for tool in v.tools:
        ctx = {"tool": tool, "gruppen": tool.detail_gruppen(v.labels)}
        aehnlich = [t for t in v.tools if t.id != tool.id and t.gruppe == tool.gruppe and t.dh["rang"] <= tool.dh["rang"]]
        aehnlich.sort(key=lambda t: (t.ampel_pd["rang"], t.dh["rang"], t.pruefpunkte))
        schreiben(f"tool/{tool.id}/", "detail.html", seite="detail", aehnlich=aehnlich[:4], **ctx)
        schreiben(f"tool/{tool.id}/", "_steckbrief.html", datei="steckbrief.html", **ctx)

    # Grundlagen, Marktanalyse
    schreiben("grundlagen/", "grundlagen.html", seite="grundlagen", ampel=AMPEL, datenhaltung=DATENHALTUNG)
    schreiben("ueber/", "ueber.html", seite="ueber")
    titel, inhalt, toc = analyse_html(v, "../")
    if titel is not None:
        schreiben("marktanalyse/", "marktanalyse.html", seite="marktanalyse", titel=titel, inhalt=Markup(inhalt), toc=toc)

    # 404 (GitHub Pages liefert sie für jede unbekannte Adresse aus – Basis wird per Skript gesetzt)
    schreiben("", "404.html", datei="404.html", seite="404")

    # Für Suchmaschinen: robots.txt immer, sitemap.xml nur mit bekannter öffentlicher Adresse (Google verlangt
    # absolute Links). Die Berater-Zwischenschritte sind «noindex» und fehlen darum bewusst.
    if site_url:
        stand = v.stand.isoformat() if v.stand else ""
        seiten_liste = ["", "verzeichnis/", "grundlagen/", "marktanalyse/", "ueber/"] + [f"tool/{t.id}/" for t in v.tools]
        eintraege = "".join(f"  <url><loc>{escape(site_url + p)}</loc>{f'<lastmod>{stand}</lastmod>' if stand else ''}</url>\n"
                            for p in seiten_liste)
        datei_schreiben(ziel / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
                        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + eintraege + "</urlset>\n")
    datei_schreiben(ziel / "robots.txt", "User-agent: *\nAllow: /\n" + (f"Sitemap: {site_url}sitemap.xml\n" if site_url else ""))

    # Suchdaten für die Vorschläge im Berater (einmal statt in jeder Seite)
    datei_schreiben(ziel / "suche.json", json.dumps(
        [{"id": t.id, "name": t.name, "kat": t.kat["label"], "ort": t.dh["label"], "dh": t.datenhaltung, "such": t.suchtext,
          "n": t.name.lower(), "a": t.anbieter.lower(), "k": t.such_kategorie, "r": t.ampel_pd["rang"]}
         for t in v.tools], ensure_ascii=False))

    # Statische Dateien
    for quelle in (HIER / "static").rglob("*"):
        if quelle.is_file():
            out = ziel / "static" / quelle.relative_to(HIER / "static")
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(quelle, out)
            geschrieben.add(out.resolve())
    datei_schreiben(ziel / ".nojekyll", "")

    # Veraltete Dateien entfernen (z.B. Steckbrief eines gelöschten Tools)
    for alt in sorted(ziel.rglob("*"), reverse=True):
        try:
            if alt.is_file() and alt.resolve() not in geschrieben:
                alt.unlink()
            elif alt.is_dir() and not any(alt.iterdir()):
                alt.rmdir()
        except OSError as exc:
            log(f"Hinweis: konnte {alt} nicht entfernen ({exc})")
    log(f"{seiten} Seiten erzeugt in {ziel}")
    return seiten
