# Herstructureringsplan — Tarifit-cursus (Claude Code)

> **Wat dit is.** Een uitvoerbaar plan voor Claude Code om de repo `berbers` op te schonen: één
> canonieke bron per inhoudstype, alle andere kopieën automatisch gegenereerd, de site gescheiden
> van de werkplaats, en een ingebouwde manier om bij toekomstige wijzigingen alles in sync te
> houden — ook als iemand anders erin werkt.
>
> **Hoe te gebruiken.** Lees dit één keer. Voer de fasen op volgorde uit, elke fase in een verse
> Claude Code-sessie. Praktische uitvoering + copy-paste: `00-LEES-EERST.md`. Wijzigingen achteraf:
> `WIJZIGINGEN.md`. De altijd-geladen guardrail is `CLAUDE.md` in de repo-root.

---

## 0. Hardste regels — elke fase, elke sessie

1. **Verzin of wijzig NOOIT een Tarifit-woord of -vorm.** Scripts herformatteren alleen bestaande
   brontekst. Ontbreekt een verwachte token, dan faalt het script — het gokt niet.
2. **Niets wordt hard verwijderd.** Wat "weg kan" gaat naar `_project/archief/`. Hard verwijderen
   pas later, na jouw goedkeuring.
3. **Keuze vóór consolidatie.** Waar bronnen verschillen, beslis jij; scripts kiezen niet zelf.
4. **Eén commit per fase, op branch `herstructurering`.** Nooit direct op `main`.

**Bron van waarheid voor woorden:** `assets/woordenlijst/woordenlijst.csv` — de woorden daarin (NL
en EN) zijn correct en leidend. Afgeleiden met meer/andere woorden wijken; de CSV wint.

---

## 1. Principes

- **Single source of truth.** Elk gegeven op één plek; afgeleiden zijn alleen-lezen en worden
  geregenereerd zodra de bron wijzigt.
- **Vibecoding-houdbaarheid.** Heldere structuur, gegenereerde i.p.v. gekopieerde afgeleiden, en
  één accuraat instructiebestand (`CLAUDE.md`) dat elke sessie stuurt.
- **Drift afdwingen.** Controles regenereren en falen bij verschil — afgeleiden lopen niet achter
  en NL/EN lopen niet uit elkaar.

---

## 2. Het bron-model

| Inhoudstype | Canonieke bron (hier bewerk je) | Afgeleiden (gegenereerd — nooit met de hand) |
|---|---|---|
| Woorden | `assets/woordenlijst/woordenlijst.csv` (NL+EN in één bestand) | `_ai/woordenlijst.md`, Anki-export, EN-woordenlijstweergave |
| Lesinhoud | `nl/cursus.html` + `en/course.html` | `_ai/cursus.md` |
| Grammatica | `nl/uitleg.html` + `en/grammar.html` | `_ai/grammatica.md` |
| Oefeningen | `assets/oefeningen/exercises-nl.json` + `-en.json` | (geen) |
| Praktijk-AI-manifest | sjabloon in `_project/docs/conventies.md` | `_ai/index.md` |

**Twee verschillende "AI's", niet verwarren:** `CLAUDE.md` = instructies voor de *coding-agent*
(Claude Code) die de repo onderhoudt — handgeschreven, altijd geladen. `_ai/*.md` = context voor
een *taaloefen-chatbot* — volledig gegenereerd.

**Sync-eisen:**

- CSV leidend; één bestand met NL- én EN-kolom → beide woordenlijstpagina's lezen eruit en zijn per
  definitie synchroon. Het aparte `woordenlijst-engels-import.csv` verdwijnt.
- HTML in `nl/`/`en/` is de zichtbare bron voor lesstof; `_ai/` wordt daaruit afgeleid.
- **NL/EN-pariteit:** de Tarifit-tekst in `nl/cursus.html` en `en/course.html` (idem `uitleg`/
  `grammar`) hoort identiek te zijn; alleen de uitleg-taal verschilt. Een check bewaakt dit.
- `_ai/` bewerk je nooit met de hand; bewerk de bron en draai `make build`.

---

## 3. Doelstructuur

```
/                         ← ALLEEN wat de site nodig heeft (Vercel serveert dit)
  index.html  styles.css  robots.txt  vercel.json
  nl/   en/   assets/
  CLAUDE.md               ← guardrail (Claude Code laadt dit elke sessie); < 200 regels
  WIJZIGINGEN.md          ← wijzigrecept waar je per wijziging naar verwijst
  .claudeignore           ← minder indexeren = minder tokens
  .vercelignore
  Makefile                ← `make build` / `make check`

_ai/                      ← GEGENEREERD (banner: niet met de hand bewerken)
  index.md  woordenlijst.md  cursus.md  grammatica.md

_project/                 ← werkplaats; nooit door de site geladen
  scripts/  docs/  archief/  bronnen/  generated/
```

---

## 4. Vastgelegde keuzes

- **CSV is de enige waarheid voor woorden** (NL+EN correct); afgeleiden wijken.
- CSV krijgt een **koprij**; parsers mappen op **kolomnaam**, niet op index.
- Build = **Python + Makefile**. Borging = **pre-commit hook + GitHub Action**.
- Opruimen = **archiveren**, niet verwijderen.
- Guardrail = **`CLAUDE.md`** (achtergrond) + **`WIJZIGINGEN.md`** (wijzigrecept).
- Gegenereerde bestanden krijgen een **"niet met de hand bewerken"-banner**.
- **NL/EN-pariteitscheck** op de Tarifit-tekst, naast de drift-check.

---

## 5. Fasen, sessies en modellen

Elke fase = één verse sessie. Tussen fasen een GATE die jij beoordeelt.

| Fase | Bestand | Model | Destructief? |
|---|---|---|---|
| 0 | `fase-0-veiligheid-en-inventaris.md` | Sonnet | Nee |
| 1 | `fase-1-reconciliatie.md` | Sonnet | Nee |
| 2 | `fase-2-structuur.md` | Sonnet | Verplaatsend, omkeerbaar |
| 3 | `fase-3-generatoren-en-borging.md` | Opus (generatoren) → Sonnet (rest) | Genereert afgeleiden |

---

## 6. Acceptatiecriteria

- Root bevat alleen site-/configbestanden + `CLAUDE.md`, `WIJZIGINGEN.md`, `Makefile`.
- Eén woordenbron (CSV); beide woordenlijsten lezen daaruit; filters en Anki-export kloppen.
- `_ai/` volledig gegenereerd, met banner; `make build` regenereert alles.
- `make check` faalt bij (a) achterlopende afgeleide of (b) NL/EN-Tarifit-verschil; de pre-commit
  hook blokkeert handmatige bewerking van gegenereerde bestanden.
- `CLAUDE.md` + `WIJZIGINGEN.md` zorgen dat elke volgende sessie of medewerker de juiste workflow
  volgt.
- Geen Tarifit-vorm gewijzigd buiten een door jou goedgekeurde toevoeging aan de CSV.
