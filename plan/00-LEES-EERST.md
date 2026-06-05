# 00 — Lees eerst (uitvoering met Claude Code)

Dit is je startpunt. Het zegt hoe je het herstructureringsplan met **Claude Code** draait: setup,
welk model per fase, de werkwijze, en de **copy-paste-prompts**. Lees daarna
`HERSTRUCTURERING-PLAN.md` één keer, en voer dan de fasen op volgorde uit.

---

## 1. Eenmalige setup

1. **Installeer Claude Code** (Node 18+):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
   Controleer de actuele installatie-instructies op
   https://docs.claude.com/en/docs/claude-code/overview
2. **Clone je repo en ga erin staan:**
   ```bash
   git clone https://github.com/pouiyhgfc/berbers.git
   cd berbers
   ```
3. **Start Claude Code** met `claude` in de map. Log in met je Claude-account (Pro/Max) — Claude
   Code zit in dezelfde abonnementslimiet als Claude.ai.
4. **Zet de planbestanden in de repo**, in een map `plan/`. Claude Code leest repo-bestanden zelf;
   je verwijst ernaar in je prompt (met een pad of `@plan/bestand.md`).
5. **Vervang de bestaande `CLAUDE.md`** in de root door de meegeleverde nieuwe `CLAUDE.md` (de
   oude is verouderd). Die wordt automatisch in elke sessie geladen en stuurt de agent.
6. **Zet de meegeleverde `.claudeignore`** in de root (scheelt tokens bij het indexeren).

---

## 2. Model & kosten

Claude Code draait op Claude-modellen; je wisselt met `/model`. Kostenverschil tussen modellen
is groot (factor 5–25), dus:

| Werk | Model | Hoe |
|---|---|---|
| Standaard (inventaris, recon, verplaatsen, parser-fix, boilerplate) | **Sonnet** | `/model sonnet` |
| De zwaarste stap: HTML→markdown-generatoren met Tarifit round-trip-check (fase 3.2) | **Opus** | `/model opus` |
| Triviale losse edits | Haiku (optioneel) | `/model haiku` |

- **Sonnet is je werkpaard.** Opus zet je alleen aan voor fase 3.2; daarna terug naar Sonnet.
- **Kosten:** Pro ($20/mnd) dekt dit, maar werkt met een tokenvenster per 5 uur. De zwaarste fase
  (3) kan daartegenaan lopen; begin die met een vers venster, of stap naar Max 5x als je vastloopt.
- **Token laag houden:** gebruik `/compact` als een sessie lang wordt, `/clear` tussen fasen, en
  houd `CLAUDE.md` kort (hij telt elke beurt mee). Laat **Agent Teams/subagents** met rust — die
  kunnen je verbruik veelvoudig opjagen.

---

## 3. Werkwijze: één fase per sessie

Elke fase doe je in een **verse sessie** (start met `/clear`). Reden: korte context = scherpere
naleving van de regels en lagere kosten. Tussen fasen zit een **GATE** die jij beoordeelt voordat
je verdergaat.

Per fase:
1. `/clear` (verse context).
2. Zet het model: `/model sonnet` (of `/model opus` voor fase 3.2).
3. Plak de openingszin hieronder.
4. **Optioneel maar aangeraden bij fase 2–3:** zet Plan-modus aan (Shift+Tab) zodat de agent eerst
   een plan toont dat jij goedkeurt voordat hij bestanden aanraakt.
5. Bij de GATE: lees de samenvatting, controleer, commit. Pas dan de volgende fase.

---

## 4. Copy-paste-prompts

**Fase 0 — inventaris · `/model sonnet`**
> Lees plan/HERSTRUCTURERING-PLAN.md voor context en daarna plan/fase-0-veiligheid-en-inventaris.md.
> Voer alleen fase 0 uit. Houd je strikt aan de regels bovenaan dat bestand. Verplaats of verwijder
> niets. Stop bij de GATE en vat samen wat je vond; begin niet aan fase 1.

**Fase 1 — reconciliatie · `/model sonnet`**
> Lees plan/fase-1-reconciliatie.md en voer fase 1 uit: schrijf de recon-scripts en genereer de
> rapporten in _project/generated/. De CSV is leidend voor woorden. Wijzig GEEN Tarifit-woord en
> pas geen bronbestanden aan — alleen rapporten. Stop bij de GATE zodat ik kan beoordelen.

**Fase 2a — verplaatsen · `/model sonnet`**
> Lees plan/fase-2-structuur.md en voer stap 2.1 uit: maak de doelmappen en verplaats wezen,
> bronnen en scripts met `git mv` naar _project/. Verwijder niets hard. Stop daarna en toon me de
> nieuwe mapstructuur.

**Fase 2b — CSV-header + parser-fix · `/model sonnet`**
> Voer stap 2.2 en 2.3 uit: voeg de koprij toe aan woordenlijst.csv en repareer de parser in
> nl/woordenlijst.html én en/wordlist.html naar naam-gebaseerd mappen, en laat en/wordlist.html uit
> de canonieke CSV lezen. Verander geen Tarifit-woord. Toon me een diff vóór je opslaat.

**Fase 2c — retireren + config · `/model sonnet`**
> Voer stap 2.4–2.6 uit: retireer de Engelse import-CSV (alleen als recon-engels.md groen was),
> maak .vercelignore en commit fase 2. Stop bij de GATE.

**Fase 3a — HTML-structuur vastleggen · `/model opus`**
> Lees plan/fase-3-generatoren-en-borging.md. Voer eerst stap 3.2 deel 1 uit: inspecteer de
> HTML-structuur van nl/cursus.html en nl/uitleg.html en leg het patroon vast in
> _project/docs/conventies.md. Schrijf nog geen generator. Stop en laat me het patroon zien.

**Fase 3b — generatoren + round-trip-check · `/model opus`**
> Voer stap 3.1–3.4 uit: bouw de generatoren voor _ai/woordenlijst.md, _ai/cursus.md,
> _ai/grammatica.md en _ai/index.md, elk met de "niet met de hand bewerken"-banner en de verplichte
> Tarifit round-trip-check die faalt als een token verdwijnt of bijkomt. Draai ze en toon de
> check-uitvoer.

**Fase 3c — Makefile, checks, borging, guardrail · `/model sonnet`**
> Voer stap 3.5–3.8 uit: Makefile (build + check + parity), de NL/EN-pariteitscheck, pre-commit
> hook, CI-workflow, en werk CLAUDE.md + WIJZIGINGEN.md bij. Draai `make check`, commit, en vat de
> eindtoestand samen tegen de acceptatiecriteria.

---

## 5. Ná de herstructurering: wijzigingen maken

Voor élke latere inhoudswijziging (woord, les, grammatica, oefening) verwijs je naar
**`WIJZIGINGEN.md`**: start een sessie en zeg bijvoorbeeld *"Lees WIJZIGINGEN.md. Ik wil [wijziging].
Bewerk de juiste canonieke bron, draai daarna make build en make check, en toon me het resultaat."*
Bewerk nooit zelf een bestand in `_ai/` — die zijn gegenereerd (ze beginnen met een banner).

## 6. Veelgemaakte fouten

- Hele plan in één sessie laten draaien → niet doen; de GATES zijn er zodat jij beslist.
- Te veel context → houd 1–3 relevante bestanden erbij; vraag nooit "analyseer het hele project".
- Voorbij een GATE doordenderen → herhaal "stop bij de GATE" en begin de volgende fase met `/clear`.
- `_ai/` met de hand bewerken → nooit; bewerk de bron en draai `make build`.
