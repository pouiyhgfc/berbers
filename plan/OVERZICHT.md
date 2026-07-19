# OVERZICHT — alle bestanden + stappenplan

Het complete plaatje op één plek: welke bestanden er zijn, waar ze heen gaan, en per stap welk
model + hoeveel "denken" + of het je data raakt.

---

## 1. De bestanden en waar ze heen gaan

**In de repo-root (`berbers/`):**

| Bestand | Wat het is |
|---|---|
| `CLAUDE.md` | Guardrail die Claude Code elke sessie automatisch leest. Vervang je oude, verouderde versie hiermee. |
| `WIJZIGINGEN.md` | Wijzigrecept dat je ná de herstructurering aanroept bij elke woord/les/grammatica-wijziging. |
| `.claudeignore` | Hernoem `dot-claudeignore.txt` hiernaartoe. Beperkt indexering = minder tokens. |

**In een map `plan/`:**

| Bestand | Wat het is |
|---|---|
| `00-LEES-EERST.md` | Je instapbestand: setup + alle copy-paste-prompts. Houd dit ernaast tijdens het werk. |
| `HERSTRUCTURERING-PLAN.md` | Het hoofdplan: bron-model, doelstructuur, keuzes. Eén keer lezen. |
| `fase-0-veiligheid-en-inventaris.md` | Branch + inventaris (niets wijzigt). |
| `fase-1-reconciliatie.md` | Verschillen in kaart brengen; jij beslist. |
| `fase-2-structuur.md` | Opschonen + één-CSV + parser-fix. |
| `fase-3-generatoren-en-borging.md` | Generatoren + checks + guardrail afronden. |
| `OVERZICHT.md` | Dit bestand. |

---

## 2. Het stappenplan (op volgorde)

Elke fase = één verse sessie (`/clear` ertussen). Stel per fase het model in met `/model`. De
prompts staan kant-en-klaar in `00-LEES-EERST.md`.

| Stap | Model | Diep denken | Raakt je data? | Stop bij het einde |
|---|---|---|---|---|
| **0** Inventaris | `/model sonnet` | Nee (adaptief is genoeg) | Nee | GATE — jij bekijkt |
| **1** Reconciliatie | `/model sonnet` | Nee | Nee (alleen rapporten) | GATE — jij beslist over oefeningen |
| **2a** Verplaatsen | `/model sonnet` | Nee | Verplaatst (omkeerbaar, niets gewist) | — |
| **2b** Parser-fix | `/model sonnet` | Optioneel `think` | Wijzigt 2 HTML-bestanden + CSV-koprij | toon diff vóór opslaan |
| **2c** Retireren + config | `/model sonnet` | Nee | Verplaatst | GATE |
| **3a** HTML-structuur bepalen | `/model opus` | **Ja — `think hard`** | Nee (alleen vastleggen) | toon het patroon |
| **3b** Generatoren + Tarifit-check | `/model opus` | **Ja — `ultrathink`** | Genereert `_ai/` (round-trip-check beschermt) | toon check-uitvoer |
| **3c** Makefile, hooks, guardrail | `/model sonnet` | Nee | Config + docs | merge naar `main` |

**Hoe je "diep denken" aanzet:** typ het woord gewoon in je prompt (`think hard …` of
`ultrathink …`) voor die ene beurt, of `/effort high` voor de hele sessie. Voor alle stappen
zonder "Ja" hoef je niets te doen — het model regelt dat zelf.

---

## 3. De drie vaste vangnetten (in elke stap)

1. **Tarifit:** nooit verzonnen of gewijzigd; scripts falen liever dan te gokken.
2. **Niets wordt gewist:** alles gaat naar `_project/archief/` (git bewaart de historie).
3. **Eén commit per fase, op branch `herstructurering`** — pas helemaal aan het eind merge je
   naar `main`.

---

## 4. Ná de herstructurering

Wil je iets aanpassen (woord, les, grammatica, oefening)? Start een sessie en zeg: *"Lees
WIJZIGINGEN.md. Ik wil [wijziging]. Bewerk de juiste bron, draai daarna `make build` en
`make check`, en toon me het resultaat."* Bewerk nooit zelf iets in `_ai/` — die zijn gegenereerd.
