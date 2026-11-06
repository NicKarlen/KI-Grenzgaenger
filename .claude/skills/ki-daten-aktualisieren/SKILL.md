---
name: ki-daten-aktualisieren
description: Aktualisiert die Daten des KI-Tool-Verzeichnisses (docs/ki_tools_verzeichnis.json) – neue Tools erfassen, bestehende Einträge ändern, Ampeln/Datenorte nachführen, offene Prüfpunkte klären, Stand-Datum setzen und die Daten anschliessend validieren. Verwenden, wenn der Nutzer Tools, Anbieter, Preise, Regionen, VISCHER-Bewertungen oder die Marktanalyse im Verzeichnis aktualisieren will.
---

# KI-Verzeichnis-Daten aktualisieren

Die Website ist statisch (GitHub Pages). `build.py` erzeugt sie aus **nur** zwei Quellen:
`docs/ki_tools_verzeichnis.json` und `docs/Marktanalyse*.md`. Es gibt keine Datenbank und keinen Server.
Lokale Vorschau mit automatischem Neubau: `.venv\Scripts\python build.py --serve`.
Online wird die Seite nach einem Push auf `main` per GitHub Actions neu gebaut – Datenfehler brechen den Build ab.

## Ablauf

1. **Verstehen, was sich ändert.** Nutzer nach Quelle fragen, falls keine genannt ist
   (Anbieter-AVV, Trust Center, Sub-Prozessorliste, VISCHER-Tabelle, Fachartikel).
   Bei Recherche: Quellenhierarchie *Vertrag/AVV > Anbieterdoku > Fachvergleich > Presse*.
2. **Datei bearbeiten.** Einzelne Einträge mit dem Edit-Tool ändern. Für viele Änderungen ein
   kurzes Python-Skript im Scratchpad schreiben, das die JSON lädt, ändert und mit
   `json.dump(..., ensure_ascii=False, indent=2)` zurückschreibt (UTF-8!).
3. **Stand setzen.** Bei jedem geänderten oder geprüften Eintrag `stand` auf das heutige Datum
   (JJJJ-MM-TT). Bei grösseren Updates auch `meta.stand`.
4. **Validieren:**
   ```
   .venv\Scripts\python datencheck.py --fix
   .venv\Scripts\python build.py
   ```
   `--fix` berechnet `meta.anzahl` und `anzahl_pruefpunkte` neu; `build.py` prüft, ob alle Seiten (inkl. Marktanalyse-Links) entstehen. FEHLER müssen behoben werden,
   WARNUNGEN dem Nutzer melden (z.B. Einträge älter als 45 Tage).
5. **Kurz zusammenfassen**, was geändert wurde (welche IDs, welche Felder, alte → neue Ampel).

Die Python-Umgebung liegt im Projekt unter `.venv` – nie global installieren.

## Datenformat

Jeder Eintrag in `eintraege` hat **genau** die Felder aus `meta.felder` (alle als String,
ausser `anzahl_pruefpunkte` = Zahl). Neue Felder nur zusammen mit `meta.felder` einführen und
dann in `grenzgaenger/data.py` (`DETAIL_GRUPPEN`) einer Detailgruppe zuordnen, sonst erscheinen
sie nicht.

| Feld | Regeln |
| --- | --- |
| `id` | eindeutig, `<region>-<anbieter>-<produkt>`, nur `a-z0-9-`. Präfixe: `ch-`, `eu-`, `us-`, `ca-`, `cn-`. **Bestehende IDs nie ändern** (sind URLs). |
| `region_anbieter` | `Schweiz`, `EU/EWR`, `USA`, `Kanada`, `China`, `International` |
| `kategorie` | eine der bestehenden Kategorien (siehe `KATEGORIEN` in `grenzgaenger/data.py`). Neue Kategorie → dort und in `GRUPPEN` ergänzen. |
| `datenhaltung_filter` | genau einer von: `CH möglich`, `EU/EWR(+CH) möglich`, `EU bedingt`, `USA/Global`, `China`, `unklar – prüfen`. **Ableiten** aus `ch_only_moeglich` / `eu_ewr_ch_only_moeglich`, nicht frei wählen. |
| `ch_only_moeglich`, `eu_ewr_ch_only_moeglich`, `on_prem_moeglich`, `open_weight`, `training_kundendaten`, `us_cloud_act` | Beginnen mit `Ja`, `Nein` oder `Prüfen`; Bedingung in Klammern, z.B. `Ja (Region explizit wählen)`. Die App liest das erste Wort. |
| `ampel_personendaten`, `ampel_berufsgeheimnis` | `grün`, `gelb`, `orange`, `rot`, `offen` oder `Abhängig`, optional mit Zusatz: `grün (Self-Host)` |
| `vischer_bewertet` | beginnt mit `Ja` nur wenn in der VISCHER-Tabelle bewertet (ergibt Badge «VISCHER-geprüft»). |
| `vischer_einschaetzung` | **paraphrasiert**, nie wörtlich kopieren (Urheberrecht). Leer, wenn nicht bewertet. |
| `hinweise_fallstricke` | Wichtigster Text für KMU – wird prominent als «Darauf sollten Sie achten» gezeigt. Kurz, konkret, verständlich. |
| `modelle` | Konkrete Modellnamen mit Version (z.B. «Qwen3.5 397B, GLM-5»), nicht nur «Open-Source-LLMs». Grundlage für die Leistung. |
| `leistung_ch`, `leistung_eu`, `leistung_global` | Beste verfügbare Modellklasse, wenn die Daten in der Schweiz / in Europa bleiben müssen / ohne Vorgabe: `Spitze`, `Stark`, `Basis`, `Prüfen`, `–` (in dieser Variante nicht möglich) oder `n/a` (keine Sprachmodell-Leistung, z.B. GPU, Vektor-DB, Übersetzung, Meetings). Zusatz in Klammern erlaubt: `Stark (nur CH-gehostete Modelle)`. Siehe «Leistungs-Logik». |
| `quellen` | URLs, getrennt mit ` | ` |
| `stand` | `JJJJ-MM-TT` |
| `anzahl_pruefpunkte` | nicht von Hand pflegen – `datencheck --fix` zählt Felder, die mit `Prüfen` beginnen. |

Unbekannte Werte immer als `Prüfen` (bzw. `Prüfen – <was genau>`) erfassen – nie raten.
Diese Werte erscheinen in der App als «noch offen».

## Kategorien und Funktionen (Anzeige in der App)

- `kategorie` wird in Alltagssprache übersetzt (z.B. «Inferenz-API» → «KI-Modelle per API») und einer
  Gruppe zugeordnet: `KATEGORIEN` und `GRUPPEN` in `grenzgaenger/data.py`. Neue Kategorie → dort ergänzen (Icon aus `grenzgaenger/ui.py`).
- «Kann auch: …» (Funktionen wie Eigene Dokumente, Agenten, Vektordatenbank, Office & E-Mail, Eigene Server)
  wird **automatisch** aus `name`, `subkategorie`, `kategorie` und `deployment` abgeleitet (`FUNKTIONEN`).
  Darum die `subkategorie` aussagekräftig formulieren, z.B. «Firmen-Chat mit Dokumenten (RAG), Agenten,
  Outlook-Add-in» statt «Enterprise-Workspace». Nach Änderungen kurz prüfen:
  ```
  .venv\Scripts\python -c "from grenzgaenger.data import get_verzeichnis as g; t=g().by_id['<id>']; print(t.kat['label'], [f['label'] for f in t.extra_funktionen])"
  ```

## Ampel-Logik (redaktionell)

- Von VISCHER bewertet → deren Urteil übernehmen.
- `grün` Personendaten: AVV vorhanden, kein Training, Daten in CH/EU, kein relevanter US-Pfad.
- `gelb`: nutzbar mit AVV + richtiger Konfiguration (Region, Websuche aus, Geschäftsplan).
- `orange`: wesentliche Lücken (z.B. AVV mit Ausschlüssen, Daten in USA bei Geschäftskunden).
- `rot`: Konsumentenprodukt, Training mit Daten, kein AVV, China.
- Berufsgeheimnis `offen`, solange kein Zusatz (z.B. VISCHER-Musterklausel) bestätigt ist.

## Leistungs-Logik (redaktionell, grob)

Massstab: Artificial Analysis Intelligence Index (https://artificialanalysis.ai/leaderboards/models). Stand Nov. 2026:
Spitze ≈ Index 50+, Stark ≈ 20–46, Basis < 20. Bei neuen Modellgenerationen die Zuordnung prüfen und in
`grenzgaenger/templates/grundlagen.html` (Abschnitt «Wie wir die Leistung einschätzen») nachführen.

- `Spitze`: aktuelle GPT-, Claude- und Gemini-Modelle (OpenAI, Anthropic, Google).
- `Stark`: grosse aktuelle offene Modelle – Kimi K2/K3, Qwen 3.5+ (gross), DeepSeek V4, GLM-5.x, MiniMax M3, Mistral Large; ausserdem Grok.
- `Basis`: kleinere/ältere Modelle – Apertus, Llama 3.3/4, Mistral Small/Medium, Gemma, Granite, gpt-oss, Command A.
- Hoster, bei denen man beliebige Modelle betreibt (Exoscale, Hugging Face, Pilae …): `Stark (je nach gewähltem Modell)`.
- **Pro Datenort-Variante** bewerten: Was bekommt man, wenn die Daten in der Schweiz bzw. in Europa bleiben müssen?
  Beispiel DACH-Plattformen: `leistung_eu` = `Spitze` (GPT via Azure EU), `leistung_ch` = `–`.
  Ist `ch_only_moeglich` bzw. `eu_ewr_ch_only_moeglich` = `Nein`, muss die Variante `–` sein (datencheck warnt).
- Der Berater kombiniert die Leistung mit der Ampel nur in passender Konfiguration (`Tool.leistung_passend`):
  Ein Schweizer Tool wird mit `leistung_ch` bewertet, auch wenn es optional GPT anbietet.
- Unbekannt → `Prüfen`. Solche Tools werden nie als «Beste Leistung» empfohlen, aber auch nicht abgewertet.

Der Berater zeigt drei Rollen statt einer Rangliste (`empfehlen` in `grenzgaenger/data.py`):
«Beste Leistung», «Bester Datenschutz», «Guter Kompromiss». Erfüllt ein Tool beides, heisst es «Beste Wahl»
und die übrigen Plätze «Ebenfalls passend». Datenschutz ist Bedingung (Filter), nicht Rangfolge.

## Marktanalyse

`docs/Marktanalyse*.md` wird als Seite «Marktanalyse» gerendert (Markdown mit Tabellen).
Bei einer neuen Version die Datei ersetzen (neuster Dateiname alphabetisch gewinnt) –
`## Überschriften` bilden das Inhaltsverzeichnis. Die Seite ist öffentlich: verständlich für KMU schreiben,
keine internen Notizen, keine Autorzeilen oder Verweise auf nicht veröffentlichte Beilagen.

- Tools verlinken mit `[Name](tool:<id>)` (öffnet den Steckbrief), Seiten mit `seite:verzeichnis|grundlagen|berater`.
- Kennzahlen nicht von Hand schreiben, sondern als Platzhalter: `{{ anzahl }}`, `{{ anzahl_schweiz }}`, `{{ anzahl_europa }}`,
  `{{ anzahl_usa }}`, `{{ anzahl_andere }}`, `{{ anzahl_ch_moeglich }}`, `{{ anzahl_eu_moeglich }}`, `{{ anzahl_ch_oder_eu }}`,
  `{{ anzahl_vischer }}`, `{{ anzahl_pruefpunkte }}`, `{{ stand }}`.
- Unbekannte Tool-IDs oder Platzhalter brechen `build.py` ab.
- Wenn neue Tools erfasst werden: prüfen, ob sie in der Marktanalyse erwähnt werden sollten.
