# KI-Tools in der Schweiz und Europa 2026: Wo bleiben Ihre Daten?

Diese Analyse ordnet den Markt für KI-Werkzeuge aus Sicht von Schweizer KMU ein: Welche Angebote gibt es, wo werden die Daten gespeichert und verarbeitet, und worauf müssen Sie bei Verträgen und Einstellungen achten? Sie ergänzt das [Verzeichnis](seite:verzeichnis) mit seinen {{ anzahl }} Einträgen um den Überblick. Die einzelnen Tools sind jeweils im Steckbrief verlinkt.

Stand der Daten: {{ stand }}. Dies ist eine redaktionelle Einschätzung auf Basis öffentlicher Quellen, keine Rechtsberatung.

## Das Wichtigste in Kürze

- **«Hosting in der Schweiz» reicht als Angabe nicht.** Wer wissen will, wo die Daten sind, muss vier Dinge prüfen: wo gespeichert wird, wo die KI rechnet, wem der Anbieter gehört und welche weiteren Dienstleister mitlesen (zum Beispiel bei der Websuche). Mehr dazu im nächsten Kapitel.
- **Echte Schweizer Datenhaltung gibt es, aber nur mit offenen Modellen.** Infomaniak, Swisscom, Sunrise/Phoeniqs und weitere Anbieter betreiben frei verfügbare Modelle (z.B. Qwen, Mistral, DeepSeek, gpt-oss oder das Schweizer Apertus) in Schweizer Rechenzentren. Die Preise liegen teils unter einem Franken pro Million Wörter-Bausteine (Tokens).
- **ChatGPT, Claude und Gemini laufen bestenfalls in Europa, kaum je nur in der Schweiz.** Für die bekannten US-Modelle ist die «EU-Datenzone» meist die beste verfügbare Option, und die Schweiz ist darin oft eingeschlossen.
- **Die Websuche ist die grösste Lücke.** Sobald ein KI-Assistent im Internet sucht, gehen Ihre Fragen häufig an eine Suchmaschine, für die der Datenschutzvertrag nicht gilt. Für sensible Daten sollte die Websuche ausgeschaltet sein.
- **Gratis- und Privatversionen sind für Firmendaten ungeeignet.** Das gilt für alle Anbieter ohne Ausnahme.
- **Der Markt bewegt sich schnell.** 2026 hat Cohere Aleph Alpha übernommen, DeepL arbeitet neu mit AWS, Sunrise und Kuble sind mit Schweizer KI-Plattformen gestartet, und GitHub Copilot bietet eine EU-Datenhaltung an. Prüfen Sie Verträge darum regelmässig.

**Das Verzeichnis in Zahlen:** {{ anzahl }} Tools, davon {{ anzahl_schweiz }} von Schweizer, {{ anzahl_europa }} von europäischen und {{ anzahl_usa }} von US-Anbietern. Bei {{ anzahl_ch_moeglich }} Tools können die Daten vollständig in der Schweiz bleiben, bei weiteren {{ anzahl_eu_moeglich }} in Europa (inkl. Schweiz). {{ anzahl_vischer }} Einträge hat die Kanzlei VISCHER rechtlich bewertet.

## Datenhaltung: vier Fragen statt einer

Viele Anbieter werben mit «Swiss hosted» oder «Hosting in Deutschland». Das stimmt oft, beschreibt aber nur einen Teil des Weges, den Ihre Daten nehmen. Für eine verlässliche Aussage braucht es vier Antworten:

| Frage | Was gemeint ist | Typische Falle |
| --- | --- | --- |
| **Wo wird gespeichert?** | Ablageort von Chats, Dateien und Wissensdatenbanken | Speicherung in der Schweiz, aber Verarbeitung in den USA |
| **Wo rechnet die KI?** | Ort des Rechenzentrums, in dem das Modell Ihre Anfrage verarbeitet | Neue Modelle laufen zuerst «global», erst später in Europa |
| **Wem gehört der Anbieter?** | Rechtsordnung, der die Betreiberfirma untersteht | Ein US-Konzern untersteht dem US CLOUD Act, auch mit Rechenzentrum in Europa |
| **Wer hilft im Hintergrund mit?** | Weitere Dienstleister (Sub-Prozessoren) wie Modellhersteller, Cloud oder Suchmaschine | Eine deutsche Plattform nutzt im Hintergrund OpenAI über Microsoft |

**Beispiel:** Eine Chat-Plattform speichert Ihre Gespräche in Frankfurt, schickt die Anfragen aber an GPT bei Microsoft und die Websuche an Bing. Die Speicherung liegt damit in der EU, die Verarbeitung in der EU-Datenzone eines US-Konzerns und die Websuche ausserhalb des Datenschutzvertrags.

Das Verzeichnis leitet den Datenort darum aus mehreren Feldern ab und zeigt bei jedem Tool, unter welcher Bedingung eine Angabe gilt (zum Beispiel «Region explizit wählen» oder «Websuche ausschalten»).

## Wie der Markt aufgebaut ist

KI-Angebote lassen sich in sechs Schichten einteilen. Für den Datenschutz zählt jede Schicht einzeln: Eine Schweizer Oberfläche über einem US-Modell schützt die Daten nicht besser als das US-Modell selbst.

| Schicht | Was es ist | Beispiele |
| --- | --- | --- |
| **Modelle** | Das eigentliche «Gehirn»: offen (Open-Weight) oder geschlossen | [Apertus](tool:ch-apertus-model) (offen, CH), Mistral, Qwen, GPT, Claude, Gemini |
| **Rechenleistung** | GPU-Server, um Modelle selbst zu betreiben | [cloudscale](tool:ch-cloudscale-gpu), [Nine](tool:ch-nine-gpu), [Firestorm](tool:ch-firestorm-gpu) |
| **Modelle per API** | Modelle zum Einbauen in eigene Software | [Infomaniak](tool:ch-infomaniak-ai-services), [Mistral](tool:eu-mistral-api), [Azure OpenAI](tool:us-azure-openai) |
| **Bausteine** | Modell-Router, Vektordatenbanken, Such-Bausteine | [Keera](tool:ch-keera), [Qdrant](tool:eu-qdrant), [Cortecs](tool:eu-cortecs) |
| **Plattformen & Assistenten** | Chat und Wissensdatenbank für das ganze Team | [Euria](tool:ch-infomaniak-euria), [Langdock](tool:eu-langdock), [ChatGPT Business](tool:us-openai-chatgpt-business) |
| **Spezialwerkzeuge & Branchen** | Übersetzung, Meetings, Dokumente, Recht, Finanz | [DeepL](tool:eu-deepl-pro), [Supertext](tool:ch-supertext), [DeepJudge](tool:ch-deepjudge) |

Offene Modelle können von jedem Anbieter betrieben werden, auch in der Schweiz oder auf eigenen Servern. Geschlossene Spitzenmodelle (GPT, Claude, Gemini) gibt es dagegen nur über den Hersteller oder dessen grosse Cloud-Partner.

## Schweiz: echte Schweizer Datenhaltung mit offenen Modellen

Der Schweizer Markt bietet 2026 Verarbeitung ausschliesslich in der Schweiz, aber nur mit offenen Modellen. Wer GPT, Claude oder Gemini braucht, landet in den EU-Zonen der US-Cloud-Anbieter.

### Modelle per API aus Schweizer Rechenzentren

| Anbieter | Rechenzentrum | Modelle (Auswahl) | Besonderheit |
| --- | --- | --- | --- |
| [Infomaniak AI Services](tool:ch-infomaniak-ai-services) | eigenes RZ Genf | Qwen, Kimi, Mistral Small, Apertus | Anfragen werden nicht gespeichert |
| [Swisscom Swiss AI Platform](tool:ch-swisscom-swiss-ai-platform) | Swisscom-RZ | Apertus u.a. | auf Grossunternehmen ausgerichtet |
| [Phoeniqs kvant AI](tool:ch-phoeniqs-kvant-ai) | Basel, Zürich | GLM, DeepSeek, Qwen, Llama, Apertus | auch On-Prem; betreibt Sunrise-Angebot |
| [stepping stone](tool:ch-steppingstone-models) | eigene RZ | DeepSeek, gpt-oss, OCR-Modelle | Partner von Keera |
| [CSCS](tool:ch-cscs-apertus) | Lugano | Apertus, Kimi, GLM | öffentliches Rechenzentrum, sehr günstig |
| [Safe Swiss Cloud](tool:ch-safeswisscloud-pai-api) | CH | über 25 offene Modelle | Schweizer Eigentum |
| [MTF Private Cloud AI](tool:ch-mtf-private-cloud-ai) | MTF-RZ | über 15 offene Modelle | von VISCHER bewertet |
| [Exoscale](tool:ch-exoscale-dedicated-inference) | Zone Genf wählbar | beliebige Hugging-Face-Modelle | eigene, dedizierte Instanz |

**Preisbeispiel Apertus 70B** (CHF pro Million Tokens, Eingabe/Ausgabe): CSCS 0.06/0.40, Phoeniqs 0.62/2.22, Infomaniak 0.78/2.80 ([Keera-Preisliste](https://keera.ch/en/models)). Der Unterschied um den Faktor 10 zeigt, wie jung dieser Markt noch ist.

### Assistenten und Plattformen für KMU

- **Firmen-Chat mit Schweizer Datenhaltung:** [Euria](tool:ch-infomaniak-euria) von Infomaniak (gratis), [Swiss AI Assistant](tool:ch-swisscom-swiss-ai-assistant) von Swisscom (Pauschalpreis), [Sunrise Business AI Assistant](tool:ch-sunrise-business-ai-assistant) (neu seit September 2026, ab CHF 7.90 pro Person und Monat), [SwissGPT](tool:ch-alpineai-swissgpt) von AlpineAI, [Nectos](tool:ch-nectos) sowie PAI Chat, MATE Business und EagleGPT.
- **Mit Vorsicht «Swiss hosted»:** Beim [Swiss AI Desk](tool:ch-kuble-swiss-ai-desk) von Kuble läuft die Plattform in der Schweiz, wählbar sind aber auch ChatGPT, Claude und Gemini. Damit gehen die Anfragen an US-Anbieter.
- **Router und Baukästen:** [Keera](tool:ch-keera) (Bern) bündelt mehrere Schweizer Hoster und sperrt US-Modelle standardmässig. Der [Swiss AI Hub](tool:ch-bbv-swiss-ai-hub) ist ein Open-Source-Baukasten, [Pilae](tool:ch-pilae) betreibt Open-Source-Werkzeuge als Dienstleistung.
- **KI-Server vor Ort:** [onprem.ai](tool:ch-onprem-ai) liefert Hardware und Software für das eigene Haus.
- **Branchenlösungen:** [Unique AI](tool:ch-unique-ai) für Banken (Azure-basiert), [DeepJudge](tool:ch-deepjudge) und [Omnilex](tool:ch-omnilex) für Kanzleien, [Supertext](tool:ch-supertext) für Übersetzungen (auch Schweizerdeutsch), [Parashift](tool:ch-parashift) und [Acodis](tool:ch-acodis) zum Auslesen von Dokumenten.

### Apertus: das Schweizer Modell

[Apertus](tool:ch-apertus-model) ist ein offenes Sprachmodell von ETH, EPFL und CSCS. Mehrere Schweizer Hoster bieten es an. Laut [SRF](https://www.srf.ch/news/schweizer-ki-sprachmodell-warum-hinkt-apertus-der-kommerziellen-konkurrenz-hinterher) liegt es leistungsmässig noch hinter der kommerziellen Konkurrenz und wird bisher erst vereinzelt produktiv genutzt. Die deutlich grössere Version 2.0 ist für 2027 angekündigt ([swissinfo](https://www.swissinfo.ch/eng/swiss-ai/one-year-on-has-swiss-ai-model-apertus-lived-up-to-the-hype/91984276)).

**Achtung:** «Apertus» heisst nicht automatisch «in der Schweiz verarbeitet». Über die [Public-AI-Schnittstelle](tool:ch-publicai-apertus) läuft das Modell auf weltweit verteilten Rechnern.

### Weitere Beobachtungen

- **Proton** betreibt seinen KI-Assistenten [Lumo](tool:ch-proton-lumo) bewusst aus Deutschland und Norwegen, nicht aus der Schweiz.
- **Regulierung:** Die Schweiz hat kein eigenes KI-Gesetz. Es gelten das Datenschutzgesetz (DSG), das Berufsgeheimnis und Branchenregeln wie jene der FINMA. Eine Vorlage zur Umsetzung der KI-Konvention des Europarats ist für Ende 2026 angekündigt ([Bundesamt für Justiz](https://www.bj.admin.ch/de/kuenstliche-intelligenz)).

## Europa: grosse Auswahl, aber den Datenpfad prüfen

Europa hat eine breite Auswahl an Anbietern, die KI-Modelle in eigenen Rechenzentren betreiben. Viele Chat-Plattformen aus dem deutschsprachigen Raum leiten die bekannten Spitzenmodelle aber weiterhin über US-Konzerne. «Hosting in Deutschland» meint dann nur den Speicherort.

### Europäische KI-Modelle per API

| Anbieter | Land | Verarbeitung | Speicherung der Anfragen |
| --- | --- | --- | --- |
| [Mistral](tool:eu-mistral-api) | FR | EU, eigene Rechenzentren | 30 Tage, auf Anfrage keine |
| [Scaleway](tool:eu-scaleway-genapi) | FR | Paris | grundsätzlich keine |
| [OVHcloud](tool:eu-ovh-ai-endpoints) | FR | Frankreich | keine |
| [IONOS](tool:eu-ionos-model-hub) | DE | Deutschland | nur für die Leistung |
| [STACKIT](tool:eu-stackit-model-serving) | DE | Deutschland | noch offen |
| [T-Systems](tool:eu-tsystems-aifs) | DE | Deutschland bzw. EU-Cloud | je nach Modell |
| [Nebius](tool:eu-nebius-token-factory) | NL | Finnland/Frankreich wählbar | Standard teils «global» |
| [Berget AI](tool:eu-berget-ai), [evroc](tool:eu-evroc) | SE | Schweden/EU | noch offen |
| [Regolo](tool:eu-regolo) | IT | Italien | keine |

Für Entwickler gibt es Router mit EU-Beschränkung, zum Beispiel [Cortecs](tool:eu-cortecs) (Sovereign-Modus aktiv einschalten), [EUrouter](tool:eu-eurouter), [Requesty EU](tool:eu-requesty-eu) und [Opper](tool:eu-opper).

### Chat-Plattformen aus dem deutschsprachigen Raum

Laut einem Vergleich von [WZ-IT](https://wz-it.com/blog/ki-plattformen-vergleich/) haben die meisten dieser Plattformen Microsoft, Google, AWS oder OpenAI als Dienstleister im Hintergrund, zwar über deren EU-Gesellschaften, aber mit US-Konzern. Ohne US-Konzern kommen meist nur die Mistral-Modelle aus. Ausnahmen mit rein deutschen Standardmodellen sind [Alan](tool:eu-alan), [plusKI](tool:eu-pluski) und [WZ-IT](tool:eu-wzit).

| Plattform | Zusatz für Berufsgeheimnis (§203 DE) | Einstiegspreis netto |
| --- | --- | --- |
| [Langdock](tool:eu-langdock) | auf Anfrage | EUR 29 pro Person |
| [Logicc](tool:eu-logicc) | ab Plan «Secure+» | EUR 49.90 pro Person |
| [meinGPT](tool:eu-meingpt) | als Zusatzmodul | EUR 20 pro Person plus Modelle |
| [nele.ai](tool:eu-neleai) | im AVV enthalten | Guthaben ab EUR 10 |
| [DeutschlandGPT](tool:eu-deutschlandgpt) | im Business-Plan | EUR 24 pro Person |
| [CompanyGPT](tool:eu-companygpt) | über Microsoft-Zusatz | EUR 14'990 einmalig plus 399 pro Monat |
| [Alan](tool:eu-alan) | nicht erwähnt | EUR 25 pro Person, mind. 100 |

Beide Vergleichsquellen ([WZ-IT](https://wz-it.com/blog/ki-plattformen-vergleich/), [innFactory](https://innfactory.ai/de/leistungen/companygpt/ki-plattformen-vergleich-2026/)) stammen von Firmen, die selbst solche Plattformen anbieten.

### Was sich 2026 verändert hat

- **Cohere übernimmt Aleph Alpha.** Ein Aushängeschild der deutschen KI-Souveränität gehört damit einem kanadischen Unternehmen ([Futurum](https://futurumgroup.com/insights/cohere-acquires-aleph-alpha-a-deal-born-of-sovereignty-necessity/)).
- **DeepL arbeitet mit AWS.** Seit Mai/Juni 2026 ist Amazon Web Services Dienstleister von [DeepL](tool:eu-deepl-pro). Eine reine EU-Verarbeitung gibt es nur noch per Vertrag ([heise](https://heise.de/-11297583)). Eine Schweizer Alternative ist [Supertext](tool:ch-supertext).
- **AWS European Sovereign Cloud:** Seit Januar 2026 in Brandenburg verfügbar, inklusive [KI-Modellen über Bedrock](tool:eu-aws-esc-bedrock) ([AWS](https://aws.amazon.com/blogs/aws/opening-the-aws-european-sovereign-cloud)).
- **Mistral** hat seinen Assistenten Le Chat in [Vibe](tool:eu-mistral-vibe) umbenannt und betreibt eigene Rechenzentren bei Paris.
- **EU AI Act:** Die wesentlichen Pflichten gelten seit dem 2. August 2026. Für Schweizer Firmen mit Kunden in der EU ist das ebenfalls relevant.

## US-Anbieter: Was in der Schweiz und in Europa möglich ist

Die bekannten US-Modelle lassen sich 2026 mit Verarbeitung in Europa nutzen, aber kaum je nur in der Schweiz. Jede Plattform hat ihre eigenen Ausnahmen.

| Produkt | Nur Schweiz? | Nur Europa? | Wichtigste Falle |
| --- | --- | --- | --- |
| [Azure OpenAI](tool:us-azure-openai) | kaum (aktuelle Modelle selten in der Region Schweiz) | Ja, EU-Datenzone inkl. CH | Websuche über Bing ist nicht vom Datenschutzvertrag gedeckt |
| [Microsoft 365 Copilot](tool:us-ms-m365-copilot) | Speicherung ja, Verarbeitung angekündigt | bedingt (EU Data Boundary) | Claude-Modelle und Websuche laufen ausserhalb |
| [OpenAI API](tool:us-openai-api) | Nein | Ja, mit Projekt-Region Europa | ohne Freigabe 30 Tage Speicherung zur Missbrauchskontrolle |
| [ChatGPT Enterprise](tool:us-openai-chatgpt-enterprise) | Nein | Ja, seit Januar 2026 | nur für neu eingerichtete Workspaces |
| [Claude (direkt)](tool:us-anthropic-claude-team-ent) | Nein | Nein | Anthropic kennt nur «USA» und «global» |
| [Claude über AWS Bedrock](tool:us-bedrock-claude) | nur ältere Modelle in Zürich | Ja, mit EU-Profil | das günstigere «Global»-Profil verlockt |
| [Claude in Microsoft Foundry](tool:us-azure-foundry-claude) | Nein | Nein | keine EU-Datenzone |
| [Gemini über Google Cloud](tool:us-google-agent-platform) | Region Zürich, je Modell prüfen | Ja, EU-Multiregion | Standard ist der globale Endpunkt |
| [Gemini API in AI Studio](tool:us-google-ai-studio) | Nein | Nein | keine Vertraulichkeitszusage |
| [GitHub Copilot](tool:us-github-copilot) | Nein | Ja, seit April 2026 (inkl. CH) | muss von der Administration eingeschaltet werden |
| [Zoom AI Companion](tool:us-zoom-ai-companion) | Nein | Ja, mit «nur Zoom-Modelle» | Standard in Europa nutzt Claude über AWS |

**Drei Muster, die sich durchziehen:**

1. **Weg von Länderregionen.** Neue Modelle erscheinen zuerst «global», dann in Datenzonen wie «EU» und zuletzt, wenn überhaupt, in einzelnen Ländern. Wer nur Schweizer Verarbeitung akzeptiert, bekommt die neuesten Modelle erst spät oder gar nicht.
2. **Missbrauchskontrolle.** Viele Anbieter speichern Anfragen eine Zeit lang und lassen sie im Verdachtsfall von Mitarbeitenden ansehen. Für Berufsgeheimnisse ist das das zentrale Problem. Bei Azure kann man das bisher nur als direkt betreuter Kunde abschalten ([VISCHER](https://www.vischer.com/de/insights/teil-31-ki-tools-wie-es-um-den-schutz-der-daten-steht-2026)).
3. **US CLOUD Act.** Alle US-Konzerne unterstehen ihm, auch mit Rechenzentrum in Europa. Zusicherungen wie die AWS European Sovereign Cloud mindern das Risiko, beseitigen es aber nicht. VISCHER hält die Debatte für teilweise überzeichnet und empfiehlt eine Abwägung im Einzelfall.

**Konsumentenprodukte** wie ChatGPT Free/Plus, Claude Free/Pro, Microsoft Copilot für Privatkunden und die Gemini-Apps sind für Firmendaten durchwegs ungeeignet.

## Spezialwerkzeuge: Meetings, Programmieren, Bilder

Neben Chat-Assistenten verbreiten sich in KMU vor allem drei Arten von KI-Werkzeugen, oft ohne dass die IT davon weiss:

- **Meeting-Assistenten** nehmen Besprechungen auf, schreiben mit und fassen zusammen. [Fireflies](tool:us-fireflies) verarbeitet alles in den USA und tritt Meetings selbständig bei, auch bei Kunden. [tl;dv](tool:eu-tldv) speichert in der EU, die Zusammenfassung kann aber über US-Modelle laufen. [Zoom AI Companion](tool:us-zoom-ai-companion) lässt sich auf Europa beschränken. In allen Fällen gilt: Teilnehmende vorher informieren und um Einwilligung bitten.
- **Programmier-Assistenten** wie [GitHub Copilot](tool:us-github-copilot) sehen den ganzen Code, oft samt Zugangsdaten und Kundendaten aus Testsystemen. Nur Business- und Enterprise-Lizenzen schliessen das Training mit Ihren Daten aus.
- **Bild- und Sprachgeneratoren:** [FLUX von Black Forest Labs](tool:eu-bfl-flux) ist eine europäische Alternative für Bilder (EU-Endpunkt verwenden). [ElevenLabs](tool:us-elevenlabs) bietet eine EU-Datenhaltung für Sprache nur im Enterprise-Vertrag an. Stimmen und Fotos echter Personen nur mit deren Einwilligung verwenden.

## Rechtliche Einordnung: die VISCHER-Tabelle

Die Zürcher Kanzlei VISCHER (David Rosenthal) veröffentlicht regelmässig eine Übersicht «Gängige KI-Tools: Wie steht es um den Schutz der Daten?» ([PDF, Stand 8.7.2026](https://rosenthal.ch/downloads/VISCHER_ki-tools-07-26.pdf); [Blogbeitrag](https://www.vischer.com/de/insights/teil-31-ki-tools-wie-es-um-den-schutz-der-daten-steht-2026)). Sie bewertet die Verträge der Anbieter für Schweizer Kunden, nicht aber den Datenstandort. Wo VISCHER ein Tool bewertet hat, übernimmt das Verzeichnis diese Einschätzung und kennzeichnet es mit «VISCHER-geprüft».

### Die Kernaussagen (sinngemäss)

- **Konsumentenangebote** aller Anbieter sind für Unternehmen nicht geeignet.
- **OpenAI und Anthropic:** Die Geschäftsangebote sind grundsätzlich nutzbar, die Verträge schliessen aber besonders schützenswerte Personendaten (z.B. Gesundheitsdaten) aus. Für Berufs- und Amtsgeheimnisse kommen beide direkt nicht in Frage. Für sensible Fälle empfiehlt VISCHER, die Modelle über die grossen Cloud-Anbieter zu nutzen.
- **Microsoft:** Copilot und Azure OpenAI sind mit Zusatzvereinbarungen auch für Berufsgeheimnisse nutzbar, allerdings nur ohne Bing-Websuche, ohne Claude-Modelle und (bei Azure) mit abgeschalteter Missbrauchskontrolle.
- **Google:** Geeignet sind nur Angebote unter dem Google-Cloud-Vertrag, «Gemini Enterprise – Business Edition» trotz des Namens nicht. Googles «Web Grounding for Enterprise» ist laut VISCHER die einzige Websuche am Markt, die auch für Berufsgeheimnisse taugt.
- **DeepL Pro:** nutzbar für Personendaten, für Berufsgeheimnisse nur mit verhandeltem Zusatz.
- **Schweizer Anbieter:** [MTF](tool:ch-mtf-private-cloud-ai) und [AlpineAI](tool:ch-alpineai-swissgpt) sind mit passendem Zusatz auch für Berufsgeheimnisse möglich. VISCHER stellt dafür eine [Musterklausel](https://www.rosenthal.ch/downloads/VISCHER_Musterklausel_Berufsgeheimnis_KI.docx) bereit.

### Was das Verzeichnis ergänzt

| Thema | VISCHER-Tabelle | Verzeichnis |
| --- | --- | --- |
| Verträge und rechtliche Eignung | ausführlich, rund 30 Dienste von 7 Anbietern | übernommen, wo vorhanden |
| Speicherort und Verarbeitungsort | nicht bewertet | bei jedem Tool |
| US CLOUD Act | im Text erwähnt | eigenes Merkmal und Filter |
| Europäische und Schweizer Hoster | nur MTF und AlpineAI | {{ anzahl_schweiz }} Schweizer und {{ anzahl_europa }} europäische Einträge |
| Bausteine, Spezialwerkzeuge, Preise | nicht im Fokus | soweit öffentlich |

VISCHER bietet mit [Red Ink](tool:ch-redink) selbst ein Produkt an. Das schmälert die Qualität der Analyse nicht, sollte aber transparent sein.

## So gehen Sie vor

1. **Daten einordnen.** Geht es um allgemeine Informationen, um Personendaten oder um Berufsgeheimnisse? Davon hängt alles Weitere ab. Der [Berater](seite:berater) führt Sie in drei Fragen dorthin.
2. **Datenort festlegen.** Für die meisten KMU genügt Europa inklusive Schweiz. Nur Schweiz schränkt die Auswahl auf offene Modelle ein.
3. **Geschäftsversion wählen und Vertrag abschliessen.** Ohne Auftragsverarbeitungsvertrag (AVV) keine Personendaten. Den AVV muss man oft aktiv abschliessen.
4. **Richtig einstellen.** Region wählen, Websuche bei sensiblen Daten ausschalten und Training mit Ihren Daten ausschliessen.
5. **Beim Anbieter nachfragen**, wenn im Verzeichnis «noch offen» steht. Bewährte Fragen:
   - Wo werden die Daten gespeichert, und wo rechnet das Modell? Gilt das auch für Backups und Support?
   - Welche Dienstleister (Sub-Prozessoren) sind beteiligt, und wie werden Sie über Änderungen informiert?
   - Werden Eingaben gespeichert oder von Mitarbeitenden eingesehen (Missbrauchskontrolle)? Lässt sich das abschalten?
   - Über welchen Anbieter läuft die Websuche, und gilt dafür der Datenschutzvertrag?
   - Gibt es einen Zusatz zum Berufsgeheimnis, zum Beispiel nach der VISCHER-Musterklausel?
6. **Regelmässig prüfen.** Anbieter ändern Regionen und Dienstleister laufend. Das Verzeichnis prüft jeden Eintrag spätestens alle 45 Tage.

## Was wir beobachten

- **Microsoft 365:** Bis zum **14. Dezember 2026** sollten Administratoren die Tenant-Einstellung «Data Location» setzen, sonst speichert Microsoft Copilot-Daten EU-weit statt in der Schweiz. Die angekündigte Verarbeitung von Copilot-Anfragen in der Schweiz ist noch nicht bestätigt.
- **Anthropic** hat Rechenzentren in Europa in Aussicht gestellt. Bis zum {{ stand }} ist das öffentlich nicht bestätigt.
- **Apertus 2.0** befindet sich im Training, die Veröffentlichung ist für 2027 geplant.
- **Websuche bei Schweizer Assistenten:** Bei Swisscom und Sunrise ist noch offen, über welchen Dienst die Websuche läuft.
- **Berufsgeheimnis bei Schweizer Hostern:** Ob die Anbieter einen Zusatz nach der VISCHER-Musterklausel unterzeichnen, ist bei den meisten noch offen. Die Antwort auf diese Frage hätte für Kanzleien, Arztpraxen und Treuhänder den grössten Nutzen.

## Methodik und Grenzen

- **Quellen:** Öffentlich zugängliche Verträge, Anbieterdokumentation, Fachvergleiche und die VISCHER-Tabelle. Bei Widersprüchen gilt: Vertrag vor Anbieterdokumentation vor Fachvergleich vor Presse. Jeder Steckbrief nennt seine Quellen und das Prüfdatum.
- **Ampeln:** Jedes Tool hat eine Ampel für Personendaten und eine für das Berufsgeheimnis. Wo VISCHER bewertet hat, folgen wir dieser Bewertung, sonst ist es eine eigene Einordnung. Wie wir bewerten, steht in den [Grundlagen](seite:grundlagen).
- **Offene Angaben:** {{ anzahl_pruefpunkte }} Angaben sind öffentlich nicht belegt und im Verzeichnis als «noch offen» markiert. Sie sollten vor einem Einsatz beim Anbieter bestätigt werden.
- **Interessenlagen:** Mehrere Vergleichsquellen stammen von Anbietern, die selbst im Markt sind (z.B. innFactory, WZ-IT, Prem AI). Das ist bei den betroffenen Einträgen vermerkt.
- **Keine Rechtsberatung:** Verträge und Einstellungen ändern sich laufend. Massgeblich ist der Vertrag am Tag der Unterzeichnung.

## Quellen (Auswahl)

- **Recht:** VISCHER-Tabelle ([PDF, 8.7.2026](https://rosenthal.ch/downloads/VISCHER_ki-tools-07-26.pdf)) und [Blogbeitrag Teil 31](https://www.vischer.com/de/insights/teil-31-ki-tools-wie-es-um-den-schutz-der-daten-steht-2026), [Bundesamt für Justiz zu KI](https://www.bj.admin.ch/de/kuenstliche-intelligenz)
- **Vergleiche Europa:** [EVY EU-Residency-Vergleich](https://evy.so/compare/eu-ai-data-residency/), [LLM Radar Datensatz](https://huggingface.co/datasets/llmradar/eu-llm-providers), [WZ-IT Plattformvergleich](https://wz-it.com/blog/ki-plattformen-vergleich/), [innFactory Plattformvergleich](https://innfactory.ai/de/leistungen/companygpt/ki-plattformen-vergleich-2026/)
- **Schweiz:** [Keera Modellkatalog mit CHF-Preisen](https://keera.ch/en/models), [Infomaniak AI Services](https://www.infomaniak.com/en/hosting/ai-services), [Swisscom Swiss AI Assistant](https://www.swisscom.ch/de/about/news/2026/02/18-swiss-ai-assistant.html), [Sunrise Sovereign Swiss AI](https://www.sunrise.ch/business/en/technology-innovation/sovereign-swiss-ai), [SRF zu Apertus](https://www.srf.ch/news/schweizer-ki-sprachmodell-warum-hinkt-apertus-der-kommerziellen-konkurrenz-hinterher), [swissinfo zu Apertus](https://www.swissinfo.ch/eng/swiss-ai/one-year-on-has-swiss-ai-model-apertus-lived-up-to-the-hype/91984276)
- **US-Cloud-Anbieter:** [AWS Bedrock Regionen](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html), [Azure Region Schweiz](https://learn.microsoft.com/en-us/answers/questions/5898946/clarification-needed-future-replacement-for-gpt-4o), [Google Cloud Standorte](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/general/locations), [OpenAI Datenresidenz](https://help.openai.com/en/articles/9903489), [Microsoft 365 Copilot Datenresidenz](https://learn.microsoft.com/en-us/microsoft-365/enterprise/m365-dr-workload-copilot), [GitHub Copilot Datenresidenz](https://github.blog/changelog/2026-04-13-copilot-data-residency-in-us-eu-and-fedramp-compliance-now-available), [Zoom AI Companion Datenresidenz](https://www.zoom.com/en/blog/ai-companion-data-residency-options/)
- **Marktbewegungen:** [Cohere/Aleph Alpha](https://futurumgroup.com/insights/cohere-acquires-aleph-alpha-a-deal-born-of-sovereignty-necessity/), [DeepL und AWS](https://heise.de/-11297583), [AWS European Sovereign Cloud](https://aws.amazon.com/blogs/aws/opening-the-aws-european-sovereign-cloud)

Alle weiteren Quellen sind in den einzelnen Steckbriefen verlinkt.
