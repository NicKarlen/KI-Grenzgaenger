"""Lädt das KI-Tool-Verzeichnis aus der JSON-Datei und übersetzt die Rohwerte
in einfache, für KMU verständliche Aussagen.

Wird von build.py (statische Website) und datencheck.py verwendet.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJEKT / "docs"
DATEN_DATEI = DOCS_DIR / "ki_tools_verzeichnis.json"
ANALYSE_GLOB = "Marktanalyse*.md"

# ---------------------------------------------------------------------------
# Datenort
# ---------------------------------------------------------------------------

DATENHALTUNG = {
    "ch": {"label": "Schweiz", "kurz": "Daten können in der Schweiz bleiben", "rang": 0, "ton": "gut",
           "satz": "Ihre Daten können vollständig in der Schweiz gespeichert und verarbeitet werden."},
    "eu": {"label": "Europa", "kurz": "Daten können in Europa bleiben", "rang": 1, "ton": "gut",
           "satz": "Ihre Daten können in Europa (EU/EWR inkl. Schweiz) bleiben – meist muss dafür die richtige Region oder Einstellung gewählt werden."},
    "eub": {"label": "Europa mit Ausnahmen", "kurz": "Grösstenteils in Europa", "rang": 2, "ton": "mittel",
            "satz": "Ihre Daten bleiben grösstenteils in Europa, aber einzelne Funktionen (z.B. Websuche oder bestimmte Modelle) können Daten ausserhalb verarbeiten."},
    "unklar": {"label": "Noch unklar", "kurz": "Datenort noch unklar", "rang": 3, "ton": "offen",
               "satz": "Wo Ihre Daten verarbeitet werden, ist öffentlich nicht eindeutig dokumentiert – bitte beim Anbieter nachfragen."},
    "us": {"label": "USA / weltweit", "kurz": "Daten gehen in die USA / weltweit", "rang": 4, "ton": "schlecht",
           "satz": "Ihre Daten werden in den USA oder weltweit verarbeitet. Eine Beschränkung auf die Schweiz oder Europa ist nicht möglich."},
    "cn": {"label": "China", "kurz": "Daten gehen nach China", "rang": 5, "ton": "schlecht",
           "satz": "Ihre Daten werden in China verarbeitet. Für Firmendaten nicht zu empfehlen."},
}

# Gruppen für die Datenort-Leiste im Verzeichnis
ORT_GRUPPEN = [
    ("ch", "Schweiz", ["ch"]),
    ("eu", "Europa", ["eu"]),
    ("eub", "Europa mit Ausnahmen", ["eub"]),
    ("rest", "USA, China, unklar", ["us", "cn", "unklar"]),
]


def datenhaltung_key(raw: str) -> str:
    v = (raw or "").lower().strip()
    if "china" in v:
        return "cn"
    if v == "ch" or v.startswith("ch ") or v.startswith("schweiz"):
        return "ch"
    if "bedingt" in v:
        return "eub"
    if v.startswith("eu"):
        return "eu"
    if "usa" in v or "global" in v:
        return "us"
    return "unklar"


# ---------------------------------------------------------------------------
# Ampeln
# ---------------------------------------------------------------------------

AMPEL = {
    "gruen": {"label": "Geeignet", "rang": 0, "ton": "gut"},
    "gelb": {"label": "Mit Vorkehrungen", "rang": 1, "ton": "mittel"},
    "orange": {"label": "Eingeschränkt", "rang": 2, "ton": "mittel"},
    "rot": {"label": "Nicht geeignet", "rang": 3, "ton": "schlecht"},
    "abh": {"label": "Je nach Betrieb", "rang": 1, "ton": "offen"},
    "offen": {"label": "Noch nicht beurteilt", "rang": 4, "ton": "offen"},
}

AMPEL_SATZ = {
    "pd": {
        "gruen": "Für Kunden- und Personendaten gut geeignet.",
        "gelb": "Für Kunden- und Personendaten geeignet, wenn Vertrag (AVV) und Einstellungen stimmen.",
        "orange": "Für Kunden- und Personendaten nur eingeschränkt geeignet.",
        "rot": "Nicht für Kunden- oder Personendaten verwenden.",
        "abh": "Ob Personendaten erlaubt sind, hängt davon ab, wo und wie Sie das Tool betreiben.",
        "offen": "Für Personendaten noch nicht beurteilt.",
    },
    "bg": {
        "gruen": "Auch für Berufsgeheimnisse (Anwalt, Arzt, Treuhand) geeignet.",
        "gelb": "Für Berufsgeheimnisse nur mit Zusatzvereinbarung und richtigen Einstellungen.",
        "orange": "Für Berufsgeheimnisse nur eingeschränkt – Zusatz muss verhandelt werden.",
        "rot": "Nicht für Berufsgeheimnisse verwenden.",
        "abh": "Ob Berufsgeheimnisse erlaubt sind, hängt vom Betrieb ab (z.B. eigene Server).",
        "offen": "Für Berufsgeheimnisse noch nicht beurteilt – vor dem Einsatz klären.",
    },
}


# ---------------------------------------------------------------------------
# Leistung (Qualität der verfügbaren KI-Modelle) – grobe Stufen, je nach Datenort
# Orientierung: Artificial Analysis Intelligence Index, Stand November 2026
# ---------------------------------------------------------------------------

LEISTUNG = {
    "spitze": {"label": "Spitzenmodelle", "kurz": "Spitze", "rang": 0, "punkte": 3, "ton": "gut",
               "satz": "Bietet Spitzenmodelle (z.B. GPT, Claude, Gemini) – die leistungsfähigsten KI-Modelle."},
    "stark": {"label": "Starke offene Modelle", "kurz": "Stark", "rang": 1, "punkte": 2, "ton": "gut",
              "satz": "Nutzt starke offene Modelle (z.B. Qwen, DeepSeek, GLM, Kimi) – sehr gut für Texte und Zusammenfassungen, bei komplexen Aufgaben etwas hinter den Spitzenmodellen."},
    "basis": {"label": "Kleinere Modelle", "kurz": "Basis", "rang": 2, "punkte": 1, "ton": "mittel",
              "satz": "Nutzt kleinere oder ältere Modelle – für einfache Aufgaben geeignet, bei anspruchsvollen Aufgaben deutlich schwächer."},
    "offen": {"label": "Noch nicht beurteilt", "kurz": "Unbekannt", "rang": 3, "punkte": None, "ton": "offen",
              "satz": "Welche KI-Modelle genutzt werden, ist öffentlich nicht bekannt."},
    "keine": {"label": "Nicht möglich", "kurz": "–", "rang": 4, "punkte": None, "ton": "offen", "satz": ""},
    "na": {"label": "Keine Bewertung", "kurz": "–", "rang": 5, "punkte": None, "ton": "offen", "satz": ""},
}
LEISTUNG_FELD = {"ch": "leistung_ch", "eu": "leistung_eu", "": "leistung_global"}
LEISTUNG_ORT_TEXT = {"ch": "mit Daten nur in der Schweiz", "eu": "mit Daten in Europa"}


def leistung_info(raw: str) -> dict:
    v = (raw or "").strip()
    low = v.lower()
    if low.startswith("spitze"):
        key = "spitze"
    elif low.startswith("stark"):
        key = "stark"
    elif low.startswith("basis"):
        key = "basis"
    elif low.startswith("n/a") or not v:
        key = "na"
    elif low.startswith("–") or low.startswith("-"):
        key = "keine"
    else:
        key = "offen"
    m = re.search(r"\(([^)]*)\)", v)
    return {"key": key, **LEISTUNG[key], "bedingung": m.group(1) if m else "", "raw": v}


def ampel(raw: str) -> dict:
    v = (raw or "").strip()
    low = v.lower()
    if low.startswith("grün") or low.startswith("gruen"):
        key = "gruen"
    elif low.startswith("gelb"):
        key = "gelb"
    elif low.startswith("orange"):
        key = "orange"
    elif low.startswith("rot"):
        key = "rot"
    elif low.startswith("abh"):
        key = "abh"
    else:
        key = "offen"
    m = re.search(r"\(([^)]*)\)", v)
    return {"key": key, "label": AMPEL[key]["label"], "rang": AMPEL[key]["rang"], "ton": AMPEL[key]["ton"],
            "bedingung": m.group(1) if m else "", "raw": v}


# ---------------------------------------------------------------------------
# Kategorien, Funktionen, Gruppen
# ---------------------------------------------------------------------------

# Fachkategorie aus der JSON -> Bezeichnung in Alltagssprache
KATEGORIEN = {
    "Chat-Assistent": ("KI-Assistent", "chat", "Ein KI-Chat für Mitarbeitende – zum Schreiben, Zusammenfassen und Fragen, ähnlich wie ChatGPT."),
    "Enterprise-KI-Plattform": ("KI-Plattform fürs Unternehmen", "layers", "Eine Plattform für das ganze Unternehmen: KI-Chat, eigene Wissensdatenbanken und Assistenten an einem Ort."),
    "Office-Add-in": ("Office-Erweiterung", "office", "Bringt KI direkt in Word, Outlook & Co."),
    "RAG-/Wissensplattform": ("Wissensplattform", "doc", "Lässt eine KI in Ihren eigenen Dokumenten suchen und darauf antworten."),
    "Inferenz-API": ("KI-Modelle per API", "code", "KI-Modelle zum Einbauen in eigene Software – für Entwickler und IT."),
    "Modell (Open-Weight)": ("Offenes KI-Modell", "model", "Ein frei verfügbares KI-Modell, das Sie selbst oder über einen Hoster betreiben können."),
    "LLM-Gateway": ("Modell-Router", "route", "Leitet Anfragen an verschiedene KI-Modelle weiter und kontrolliert, wohin Daten fliessen."),
    "Vektordatenbank (RAG)": ("Vektordatenbank", "db", "Speichert Dokumente so, dass eine KI darin suchen kann – ein Baustein für Wissensdatenbanken."),
    "Embeddings/Reranking": ("Such-Baustein (Embeddings)", "search", "Baustein, mit dem eine KI Inhalte in eigenen Dokumenten findet."),
    "Übersetzung": ("Übersetzung", "lang", "Übersetzt Texte und Dokumente mit KI."),
    "Transkription/Sprache": ("Diktat & Transkription", "mic", "Wandelt Sprache in Text um – zum Diktieren oder für Protokolle."),
    "Dokumentenverarbeitung (IDP)": ("Dokumente auslesen", "scan", "Liest Rechnungen, Formulare und Dokumente automatisch aus und ordnet sie zu."),
    "Meeting-Assistent": ("Meeting-Assistent", "users", "Nimmt Besprechungen auf, schreibt sie mit und fasst sie zusammen."),
    "Bild-/Mediengenerierung": ("Bilder & Medien erzeugen", "image", "Erzeugt Bilder, Grafiken oder Videos aus einer Textbeschreibung."),
    "Coding-Assistent": ("Programmier-Assistent", "code", "Hilft Entwicklern beim Schreiben, Prüfen und Erklären von Programmcode."),
    "Vertikal: Legal": ("Branchenlösung Recht", "brief", "KI speziell für Kanzleien und Rechtsabteilungen."),
    "Vertikal: Finanz": ("Branchenlösung Finanz", "brief", "KI speziell für Banken, Vermögensverwalter und Versicherer."),
    "GPU/Infrastruktur": ("GPU-Server", "server", "Rechenleistung, um KI-Modelle selbst zu betreiben."),
    "On-Prem-Appliance": ("KI-Server vor Ort", "server", "Fertige Hardware mit KI-Software für Ihr eigenes Rechenzentrum."),
}


def kategorie_info(kat: str) -> dict:
    label, icon, text = KATEGORIEN.get(kat, (kat or "Weitere", "spark", ""))
    return {"label": label, "icon": icon, "text": text, "fach": kat}


# Gruppen ("Art des Tools") – Reihenfolge = Sortierung im Verzeichnis
GRUPPEN = [
    {"id": "assistent", "label": "KI-Assistenten", "hilfe": "Chatten, schreiben, zusammenfassen", "icon": "chat",
     "kategorien": ["Chat-Assistent", "Office-Add-in"]},
    {"id": "plattform", "label": "KI-Plattformen fürs Unternehmen", "hilfe": "Chat, Wissensdatenbank und Assistenten", "icon": "layers",
     "kategorien": ["Enterprise-KI-Plattform", "RAG-/Wissensplattform"]},
    {"id": "branche", "label": "Branchenlösungen", "hilfe": "Recht und Finanz", "icon": "brief",
     "kategorien": ["Vertikal: Legal", "Vertikal: Finanz"]},
    {"id": "spezial", "label": "Übersetzen, Meetings, Medien", "hilfe": "Spezialisierte Werkzeuge", "icon": "tool",
     "kategorien": ["Übersetzung", "Transkription/Sprache", "Meeting-Assistent", "Dokumentenverarbeitung (IDP)",
                    "Bild-/Mediengenerierung"]},
    {"id": "api", "label": "KI-Modelle per API", "hilfe": "Für Entwickler und IT", "icon": "code",
     "kategorien": ["Inferenz-API", "Modell (Open-Weight)", "Coding-Assistent"]},
    {"id": "bausteine", "label": "Router & Datenbanken", "hilfe": "Bausteine für eigene KI-Lösungen", "icon": "db",
     "kategorien": ["LLM-Gateway", "Vektordatenbank (RAG)", "Embeddings/Reranking"]},
    {"id": "infra", "label": "Eigene Server", "hilfe": "GPU-Server und Hardware vor Ort", "icon": "server",
     "kategorien": ["GPU/Infrastruktur", "On-Prem-Appliance"]},
]
GRUPPE_RANG = {g["id"]: i for i, g in enumerate(GRUPPEN)} | {"weitere": len(GRUPPEN)}


def gruppe_von(kat: str) -> str:
    for g in GRUPPEN:
        if kat in g["kategorien"]:
            return g["id"]
    return "weitere"


def _rx(muster):
    r = re.compile(muster, re.I)
    return lambda text, raw: bool(r.search(text))


# Funktionen: was ein Tool (zusätzlich) kann. Abgeleitet aus Name, Unterkategorie,
# Kategorie und Deployment – darum lohnt sich eine aussagekräftige Unterkategorie.
FUNKTIONEN = [
    ("chat", "Chat", "chat", lambda text, r: bool(re.search(r"\bchat|(?<!meeting-)(?<!coding-)assistent|workspace|copilot|vibe|lumo|chatgpt|claude (free|team)|gemini (apps|enterprise|in google)", text, re.I))
        or r.get("kategorie") in ("Chat-Assistent", "Enterprise-KI-Plattform")),
    ("wissen", "Eigene Dokumente", "doc", _rx(r"\brag\b|wissensbas|knowledge|dokumenten-assist|libraries|graph-zugriff|enterprise-suche|kanzlei-dokumente|wissensplattform")),
    ("agent", "Agenten & Workflows", "agent", _rx(r"agent|workflow|automation|n8n|dify")),
    ("office", "Office & E-Mail", "office", _rx(r"\bword\b|excel|outlook|office|m365|google workspace|ksuite|mail")),
    ("code", "Programmieren", "code", _rx(r"\bcode\b")),
    ("api", "API", "code", lambda text, r: bool(re.search(r"\bapi\b", r.get("deployment", ""), re.I))
        or bool(re.search(r"\bapi\b|openai-kompatib|endpoint", r.get("subkategorie", "") + " " + r.get("name", ""), re.I))
        or r.get("kategorie") in ("Inferenz-API", "LLM-Gateway")),
    ("router", "Modell-Router", "route", _rx(r"gateway|routing|router")),
    ("vektor", "Vektordatenbank", "db", _rx(r"vektor|milvus|vector")),
    ("embed", "Embeddings", "search", _rx(r"embed|rerank")),
    ("uebers", "Übersetzung", "lang", _rx(r"übersetz")),
    ("sprache", "Diktat & Transkription", "mic", _rx(r"diktat|transkri|speech|whisper")),
    ("ocr", "Dokumente auslesen", "scan", _rx(r"\bocr\b|\bidp\b|extraktion|dokumentverarbeitung|klassifikation")),
    ("meeting", "Meeting-Protokolle", "users", _rx(r"meeting|besprechung")),
    ("medien", "Bilder & Medien", "image", _rx(r"bildgenerier|bilderzeug|text-to-image|bildbearbeit|video")),
    ("gpu", "GPU-Leistung", "server", lambda text, r: r.get("kategorie") == "GPU/Infrastruktur" or "gpu" in r.get("subkategorie", "").lower()),
    ("onprem", "Eigene Server möglich", "server", lambda text, r: ja_nein(r.get("on_prem_moeglich", "")) == "ja"),
]
FUNKTION_INFO = {k: {"key": k, "label": label, "icon": icon} for k, label, icon, _ in FUNKTIONEN}
HAUPT_FUNKTION = {
    "Chat-Assistent": "chat", "Enterprise-KI-Plattform": "chat", "Inferenz-API": "api", "LLM-Gateway": "router",
    "Vektordatenbank (RAG)": "vektor", "Embeddings/Reranking": "embed", "Übersetzung": "uebers",
    "Transkription/Sprache": "sprache", "Dokumentenverarbeitung (IDP)": "ocr", "GPU/Infrastruktur": "gpu",
    "On-Prem-Appliance": "onprem", "RAG-/Wissensplattform": "wissen",
    "Meeting-Assistent": "meeting", "Bild-/Mediengenerierung": "medien", "Coding-Assistent": "code",
}

REGION_KURZ = {"Schweiz": "CH", "EU/EWR": "EU", "USA": "US", "Kanada": "CA", "China": "CN", "International": "INT"}

# Detailbereiche: Feld -> kurze Erklärung für Laien
DETAIL_GRUPPEN = [
    {"id": "datenort", "titel": "Wo sind meine Daten?", "felder": [
        ("speicherort_daten", "Wo Chats, Dateien und Einstellungen gespeichert werden."),
        ("inferenz_ort", "Wo die KI Ihre Anfrage tatsächlich berechnet."),
        ("ch_only_moeglich", "Lässt sich alles auf die Schweiz beschränken?"),
        ("eu_ewr_ch_only_moeglich", "Lässt sich alles auf Europa (inkl. Schweiz) beschränken?"),
        ("hq_land", "Hauptsitz des Anbieters."),
        ("mutter_jurisdiktion", "Welchem Recht der Mutterkonzern untersteht."),
        ("us_cloud_act", "Können US-Behörden Zugriff verlangen – auch in europäischen Rechenzentren?"),
    ]},
    {"id": "vertrag", "titel": "Vertrag & Datenschutz", "felder": [
        ("dpa_avv", "Auftragsverarbeitungsvertrag – Pflicht bei Personendaten."),
        ("training_kundendaten", "Werden Ihre Eingaben zum Trainieren der KI genutzt?"),
        ("retention_zdr", "Wie lange Anfragen gespeichert werden und wer sie sehen kann."),
        ("websuche_hinweis", "Bei der Websuche gehen Fragen oft an Dritte – häufig ohne Datenschutzvertrag."),
        ("berufsgeheimnis", "Eignung für Berufs- oder Amtsgeheimnisse (Art. 320/321 StGB)."),
        ("zertifizierungen", "Sicherheits-Zertifikate wie ISO 27001."),
    ]},
    {"id": "technik", "titel": "Technik & Modelle", "felder": [
        ("kategorie", "Art des Angebots."),
        ("subkategorie", "Was das Tool genau macht."),
        ("deployment", "Wie das Tool betrieben wird (Cloud, eigene Server …)."),
        ("on_prem_moeglich", "Kann das Tool auf eigenen Servern laufen?"),
        ("modelle", "Welche KI-Modelle zur Auswahl stehen."),
        ("modell_typ", "Offene Modelle (Open-Weight) oder geschlossene Modelle eines Herstellers."),
        ("leistung_global", "Beste verfügbare Modellklasse, wenn der Datenort keine Rolle spielt."),
        ("leistung_eu", "Beste Modellklasse, wenn die Daten in Europa (inkl. Schweiz) bleiben müssen."),
        ("leistung_ch", "Beste Modellklasse, wenn die Daten in der Schweiz bleiben müssen."),
        ("open_weight", "Sind die Modelle frei verfügbar und selbst betreibbar?"),
        ("openai_kompatibel", "Lässt sich bestehende Software für OpenAI einfach umstellen?"),
    ]},
    {"id": "preis", "titel": "Preis & Zielgruppe", "felder": [
        ("preis", "Öffentlich bekannte Preise."),
        ("zielgruppe", "Für wen das Angebot gedacht ist."),
        ("anbieter", "Vollständiger Firmenname."),
        ("region_anbieter", "Herkunftsregion des Anbieters."),
    ]},
]


def ist_offen(value) -> bool:
    """Wert, der noch beim Anbieter geprüft werden muss."""
    if not isinstance(value, str):
        return False
    # Ganzes Wort: «Offen – …» ist offen, «Offene Modelle wie Llama» dagegen nicht
    return bool(re.match(r"(prüfen|offen|unklar)\b", value.strip().lower()))


def ja_nein(value: str) -> str:
    v = (value or "").strip().lower()
    if v.startswith("ja"):
        return "ja"
    if v.startswith("nein"):
        return "nein"
    if ist_offen(value):
        return "offen"
    return "teils"


# ---------------------------------------------------------------------------
# Datenobjekte
# ---------------------------------------------------------------------------


@dataclass
class Tool:
    raw: dict
    id: str = ""
    name: str = ""
    anbieter: str = ""
    datenhaltung: str = "unklar"
    gruppe: str = "weitere"
    kat: dict = field(default_factory=dict)
    ampel_pd: dict = field(default_factory=dict)
    ampel_bg: dict = field(default_factory=dict)
    vischer: bool = False
    quellen: list = field(default_factory=list)
    funktionen: set = field(default_factory=set)
    suchtext: str = ""

    def __post_init__(self):
        r = self.raw
        self.id = r.get("id", "")
        self.name = r.get("name", "")
        self.anbieter = r.get("anbieter", "")
        self.datenhaltung = datenhaltung_key(r.get("datenhaltung_filter", ""))
        self.gruppe = gruppe_von(r.get("kategorie", ""))
        self.kat = kategorie_info(r.get("kategorie", ""))
        self.ampel_pd = ampel(r.get("ampel_personendaten", ""))
        self.ampel_bg = ampel(r.get("ampel_berufsgeheimnis", ""))
        self.vischer = (r.get("vischer_bewertet") or "").strip().lower().startswith("ja")
        self.quellen = [q.strip() for q in (r.get("quellen") or "").split("|") if q.strip()]
        text = " ".join(str(r.get(k, "")) for k in ("name", "subkategorie", "kategorie", "deployment"))
        self.funktionen = {k for k, _, _, test in FUNKTIONEN if test(text, r)}
        self.suchtext = " ".join(
            str(r.get(k, "")) for k in ("name", "anbieter", "kategorie", "subkategorie", "modelle", "zielgruppe", "hq_land")
        ).lower()

    def __getattr__(self, item):
        # Erlaubt im Template z.B. {{ tool.preis }}
        raw = self.__dict__.get("raw")
        if raw is not None and item in raw:
            return raw[item]
        raise AttributeError(item)

    # --- Einfache Aussagen -------------------------------------------------
    @property
    def dh(self) -> dict:
        return DATENHALTUNG[self.datenhaltung]

    @property
    def gruppe_info(self) -> dict:
        return next((g for g in GRUPPEN if g["id"] == self.gruppe), {"id": "weitere", "label": "Weitere", "icon": "spark", "hilfe": ""})

    @property
    def region_kurz(self) -> str:
        return REGION_KURZ.get(self.raw.get("region_anbieter", ""), self.raw.get("hq_land", ""))

    @property
    def kurzname(self) -> str:
        return re.sub(r"\s+", " ", re.sub(r"\s*\([^)]*\)\s*", " ", self.name)).strip()

    @property
    def extra_funktionen(self) -> list[dict]:
        """Funktionen zusätzlich zur Hauptkategorie («Kann auch: …»)."""
        haupt = HAUPT_FUNKTION.get(self.raw.get("kategorie", ""))
        out = []
        for k, *_ in FUNKTIONEN:
            if k in self.funktionen and k != haupt and not (k == "api" and "router" in self.funktionen):
                out.append(FUNKTION_INFO[k])
        return out

    @property
    def cloud_act(self) -> str:
        return ja_nein(self.raw.get("us_cloud_act", ""))

    @property
    def training(self) -> str:
        return ja_nein(self.raw.get("training_kundendaten", ""))

    @property
    def on_prem(self) -> bool:
        return "onprem" in self.funktionen

    @property
    def pruefpunkte(self) -> int:
        try:
            return int(self.raw.get("anzahl_pruefpunkte") or 0)
        except (TypeError, ValueError):
            return 0

    def ampel_fuer(self, sens: str) -> dict:
        return self.ampel_bg if sens == "bg" else self.ampel_pd

    # --- Leistung ------------------------------------------------------------
    def leistung_fuer(self, ort: str = "") -> dict:
        """Leistungsstufe für den gewählten Datenort ('ch', 'eu' oder '' = egal)."""
        return leistung_info(self.raw.get(LEISTUNG_FELD.get(ort, "leistung_global"), ""))

    def leistung_passend(self, ort: str = "") -> dict:
        """Leistung in der Konfiguration, auf die sich Datenort und Ampeln beziehen.

        Ein Schweizer Tool ist nur mit seinen Schweizer Modellen «Schweiz / geeignet» – dass es optional
        auch GPT anbietet, darf seine Datenschutz-Bewertung nicht mit Spitzenleistung kombinieren.
        """
        rang = {"ch": 0, "eu": 1, "": 2}
        eng = {"ch": "ch", "eu": "eu"}.get(self.datenhaltung, "")
        x = self.leistung_fuer(min(ort, eng, key=rang.__getitem__))
        return x if x["key"] != "keine" else self.leistung_fuer(ort)

    @property
    def such_kategorie(self) -> str:
        """Kategorie und Unterkategorie, kleingeschrieben – für die Gewichtung in der Suche."""
        return " ".join((self.kat["label"], self.raw.get("kategorie", ""), self.raw.get("subkategorie", ""))).lower()

    @property
    def lstg(self) -> dict:
        return self.leistung_fuer("")

    @property
    def leistung_bewertet(self) -> bool:
        return self.lstg["key"] != "na"

    def leistung_satz(self, ort: str = "", passend: bool = False) -> dict | None:
        """Ein Satz für «Kurz gesagt», inkl. Hinweis, wenn der Datenort die Leistung einschränkt."""
        haupt = self.leistung_passend(ort) if passend else self.leistung_fuer(ort)
        if haupt["key"] in ("na", "keine"):
            return None
        text = haupt["satz"]
        if not ort and not passend:
            for o in ("eu", "ch"):
                x = self.leistung_fuer(o)
                if x["key"] in ("spitze", "stark", "basis") and x["rang"] > haupt["rang"]:
                    text += f" {LEISTUNG_ORT_TEXT[o].capitalize()}: {x['label'].lower()}."
                    break
        return {"ton": haupt["ton"], "text": text}

    def kurz_gesagt_fuer(self, ort: str = "", passend: bool = False) -> list[dict]:
        punkte = list(self.kurz_gesagt)
        satz = self.leistung_satz(ort, passend)
        if satz:
            punkte.insert(1, satz)
        return punkte

    def gruende_fuer(self, ort: str = "") -> list[dict]:
        """Bis zu drei positive Punkte plus der wichtigste Vorbehalt – für Empfehlungen."""
        alle = self.kurz_gesagt_fuer(ort, passend=True)
        gut = [k for k in alle if k["ton"] == "gut"][:3]
        vorbehalt = next((k for k in alle if k["ton"] in ("mittel", "schlecht")), None)
        return (gut + ([vorbehalt] if vorbehalt else []))[:4]

    @property
    def kurz_gesagt(self) -> list[dict]:
        """Die wichtigsten Aussagen in einfacher Sprache, mit Tonalität (gut/mittel/schlecht/offen)."""
        punkte = [{"ton": self.dh["ton"], "text": self.dh["satz"]}]
        for art, a in (("pd", self.ampel_pd), ("bg", self.ampel_bg)):
            text = AMPEL_SATZ[art][a["key"]]
            if a["bedingung"]:
                text = f"{text} ({a['bedingung']})"
            punkte.append({"ton": a["ton"], "text": text})
        t = self.training
        if t == "nein":
            punkte.append({"ton": "gut", "text": "Ihre Eingaben werden nicht zum Trainieren der KI verwendet."})
        elif t == "ja":
            punkte.append({"ton": "schlecht", "text": "Ihre Eingaben können zum Trainieren der KI verwendet werden."})
        elif t == "offen":
            punkte.append({"ton": "offen", "text": "Ob Eingaben zum Training verwendet werden, ist noch offen."})
        c = self.cloud_act
        if c == "ja":
            punkte.append({"ton": "mittel", "text": "Der Anbieter untersteht US-Recht (CLOUD Act): US-Behörden könnten Zugriff verlangen – auch auf Daten in Europa."})
        elif c == "nein":
            punkte.append({"ton": "gut", "text": "Kein US-Konzern im Hintergrund – kein Zugriff über den US CLOUD Act."})
        return punkte

    @property
    def cloud_act_text(self) -> str:
        return {"ja": "Möglich", "nein": "Nein"}.get(self.cloud_act, "Offen")

    @property
    def leistung_text(self) -> str:
        """Kurzfassung für die Kernfakten, z.B. «Spitzenmodelle · nur Schweiz: Starke offene Modelle»."""
        g = self.lstg
        if g["key"] == "na":
            return ""
        teile = [g["label"]]
        for o, name in (("eu", "in Europa"), ("ch", "nur Schweiz")):
            x = self.leistung_fuer(o)
            if x["key"] != g["key"]:
                teile.append(f"{name}: {x['label'].lower() if x['key'] != 'keine' else 'nicht möglich'}")
        return " · ".join(teile)

    @property
    def fakten(self) -> list[dict]:
        r = self.raw
        leistung = [{"titel": "Leistung (KI-Modelle)", "wert": self.leistung_text, "offen": self.lstg["key"] == "offen"}] \
            if self.leistung_bewertet else []
        return leistung + [
            {"titel": "Gespeichert in", "wert": r.get("speicherort_daten", ""), "offen": ist_offen(r.get("speicherort_daten"))},
            {"titel": "Verarbeitet in", "wert": r.get("inferenz_ort", ""), "offen": ist_offen(r.get("inferenz_ort"))},
            {"titel": "Datenschutzvertrag (AVV)", "wert": r.get("dpa_avv", ""), "offen": ist_offen(r.get("dpa_avv"))},
            {"titel": "Preis", "wert": r.get("preis", ""), "offen": ist_offen(r.get("preis"))},
        ]

    def detail_gruppen(self, labels: dict) -> list[dict]:
        out = []
        for g in DETAIL_GRUPPEN:
            zeilen = []
            for key, hilfe in g["felder"]:
                wert = self.raw.get(key, "")
                if wert in ("", None):
                    continue
                zeilen.append({"key": key, "label": labels.get(key, key), "hilfe": hilfe, "wert": wert, "offen": ist_offen(wert)})
            out.append({**g, "zeilen": zeilen, "offen_anzahl": sum(z["offen"] for z in zeilen)})
        return out


@dataclass
class Verzeichnis:
    meta: dict
    tools: list[Tool]
    by_id: dict

    @property
    def stand(self) -> date | None:
        try:
            return date.fromisoformat(self.meta.get("stand", ""))
        except ValueError:
            return None

    @property
    def labels(self) -> dict:
        return self.meta.get("felder", {})

    def zaehler(self) -> dict:
        z = {k: 0 for k in DATENHALTUNG}
        for t in self.tools:
            z[t.datenhaltung] += 1
        return z


# ---------------------------------------------------------------------------
# Filtern & Sortieren (gemeinsam für Berater und Verzeichnis)
# ---------------------------------------------------------------------------

BEDARF = {
    "chat": lambda t: "chat" in t.funktionen and t.gruppe in ("assistent", "plattform", "branche"),
    "wissen": lambda t: "wissen" in t.funktionen,
    "spezial": lambda t: t.gruppe == "spezial" or bool({"uebers", "sprache", "ocr"} & t.funktionen),
    "api": lambda t: "api" in t.funktionen and t.gruppe in ("api", "bausteine"),
    "onprem": lambda t: t.on_prem,
}


def filtern(tools, *, ort="", orte=(), sens="", bed="", gruppe="", funk=(), cloud=False, vischer=False, q=""):
    woerter = q.strip().lower().split()
    ort_keys = set()
    for o in orte:
        for key, _, keys in ORT_GRUPPEN:
            if key == o:
                ort_keys.update(keys)
    out = []
    for t in tools:
        if ort == "ch" and t.datenhaltung != "ch":
            continue
        if ort == "eu" and t.datenhaltung not in ("ch", "eu"):
            continue
        if ort_keys and t.datenhaltung not in ort_keys:
            continue
        if sens == "pd" and t.ampel_pd["key"] not in ("gruen", "gelb"):
            continue
        if sens == "bg" and t.ampel_bg["key"] not in ("gruen", "gelb"):
            continue
        if bed in BEDARF and not BEDARF[bed](t):
            continue
        if gruppe and t.gruppe != gruppe:
            continue
        if funk and not set(funk) <= t.funktionen:
            continue
        if cloud and t.cloud_act != "nein":
            continue
        if vischer and not t.vischer:
            continue
        if woerter and not all(w in t.suchtext for w in woerter):
            continue
        out.append(t)
    rel = "ampel_bg" if sens == "bg" else "ampel_pd"
    out.sort(key=lambda t: (getattr(t, rel)["rang"], t.dh["rang"], GRUPPE_RANG[t.gruppe], t.pruefpunkte, t.name.lower()))
    return out


# ---------------------------------------------------------------------------
# Empfehlungen im Berater: Datenschutz ist die Bedingung (Filter), danach
# zeigen drei Rollen den Zielkonflikt zwischen Leistung und Datenschutz.
# ---------------------------------------------------------------------------

ROLLEN = {
    "beide": {"label": "Beste Wahl", "hilfe": "Stärkste Modelle und bester Datenschutz zugleich"},
    "leistung": {"label": "Beste Leistung", "hilfe": "Die stärksten KI-Modelle, die Ihre Vorgaben erfüllen"},
    "datenschutz": {"label": "Bester Datenschutz", "hilfe": "Die sicherste Wahl für Ihre Daten"},
    "kompromiss": {"label": "Guter Kompromiss", "hilfe": "Gute Leistung bei gutem Datenschutz"},
    "weitere": {"label": "Ebenfalls passend", "hilfe": "Eine weitere gute Wahl"},
}
_P_AMPEL = {"gruen": 2, "gelb": 1.25, "abh": 1, "offen": 0.5, "orange": 0.25, "rot": 0}
_P_ORT = {"ch": 1, "eu": 0.75, "eub": 0.5, "unklar": 0.25, "us": 0, "cn": 0}
_P_CLOUD = {"nein": 0.5, "teils": 0.25, "offen": 0.1, "ja": 0}
_L_NEUTRAL = 1.5  # unbekannte Leistung: weder belohnen noch bestrafen


ANWENDER_GRUPPEN = ("assistent", "plattform", "branche", "spezial")


def empfehlen(liste: list[Tool], sens: str = "", ort: str = "", leistung: bool = True,
              nur_anwender: bool = False) -> tuple[list[dict], list[Tool]]:
    """Gibt (rollen, rest) zurück. rollen = [{'rolle': key, 'tool': Tool, ...}], höchstens drei.
    leistung=False: Leistung nicht berücksichtigen (z.B. Spezialwerkzeuge ohne Sprachmodell-Bewertung)."""
    def lp(t):
        return t.leistung_passend(ort)["punkte"] if leistung else None

    def amp(t):
        return t.ampel_fuer(sens)

    def schutz(t):
        return _P_AMPEL[amp(t)["key"]] + _P_ORT[t.datenhaltung] + _P_CLOUD[t.cloud_act]

    def score(t):
        return (lp(t) or _L_NEUTRAL) + schutz(t)

    def profil(t):
        return (lp(t), amp(t)["key"], t.datenhaltung, t.cloud_act)

    def basis(t):
        return (GRUPPE_RANG[t.gruppe], t.pruefpunkte, t.name.lower())

    def gesamt_key(t):
        return (-score(t), -(lp(t) or _L_NEUTRAL), amp(t)["rang"], t.dh["rang"], *basis(t))

    # nur_anwender: Empfehlungen nur aus Tools für Anwender (keine GPU-Server, Datenbanken, APIs),
    # die vollständige Liste («rest») enthält aber weiterhin alles.
    kandidaten = [t for t in liste if amp(t)["key"] != "rot" and (not nur_anwender or t.gruppe in ANWENDER_GRUPPEN)]
    if not kandidaten:
        return [], list(liste)
    mit_leistung = [t for t in kandidaten if lp(t)]
    gewaehlt: list[tuple[str, Tool]] = []

    beste_ds = min(kandidaten, key=lambda t: (-schutz(t), amp(t)["rang"], -(lp(t) or _L_NEUTRAL), *basis(t)))
    if mit_leistung:
        beste_l = min(mit_leistung, key=lambda t: (-lp(t), amp(t)["rang"], t.dh["rang"], *basis(t)))
        if beste_l is beste_ds:
            gewaehlt.append(("beide", beste_l))
        else:
            gewaehlt += [("leistung", beste_l), ("datenschutz", beste_ds)]
    else:
        gewaehlt.append(("datenschutz", beste_ds))

    # Kompromiss: bester Gesamtwert, aber mit eigenem Profil (nicht nur eine Kopie der anderen Empfehlungen).
    # Nur sinnvoll, wenn Leistung und Datenschutz auseinanderfallen – gibt es eine «Beste Wahl»,
    # gibt es nichts abzuwägen, und die übrigen Plätze heissen «Ebenfalls passend».
    uebrig = [t for t in sorted(kandidaten, key=gesamt_key) if not any(t is x for _, x in gewaehlt)]
    if mit_leistung and gewaehlt[0][0] == "leistung" and len(gewaehlt) < 3 and uebrig:
        profile = {profil(x) for _, x in gewaehlt}
        k = next((t for t in uebrig if profil(t) not in profile and lp(t)), uebrig[0])
        gewaehlt.append(("kompromiss", k))
    for t in uebrig:
        if len(gewaehlt) >= 3:
            break
        if not any(t is x for _, x in gewaehlt):
            gewaehlt.append(("weitere", t))

    rollen = [{"rolle": r, **ROLLEN[r], "tool": t, "leistung": t.leistung_passend(ort)} for r, t in gewaehlt]
    rest = sorted((t for t in liste if not any(t is x for _, x in gewaehlt)), key=gesamt_key)
    return rollen, rest


# ---------------------------------------------------------------------------
# Laden
# ---------------------------------------------------------------------------


def lade_rohdaten(path: Path | None = None) -> dict:
    with open(path or DATEN_DATEI, encoding="utf-8") as f:
        return json.load(f)


def get_verzeichnis(path: Path | None = None) -> Verzeichnis:
    roh = lade_rohdaten(path)
    tools = [Tool(e) for e in roh.get("eintraege", [])]
    return Verzeichnis(meta=roh.get("meta", {}), tools=tools, by_id={t.id: t for t in tools})
