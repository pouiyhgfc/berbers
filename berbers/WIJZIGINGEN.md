# WIJZIGINGEN — hoe je iets aanpast zonder de boel uit sync te halen

> Verwijs naar dit bestand bij elke inhoudelijke wijziging. Het zegt per soort wijziging wat je
> bewerkt en hoe alles up-to-date blijft. `CLAUDE.md` is de passieve achtergrondregel die altijd
> meedraait; dit is het actieve recept dat je per wijziging aanroept.

## Voor de agent (lees dit als dit bestand wordt aangeroepen)
1. Bewerk **alleen de canonieke bron** (tabel hieronder). Bewerk **nooit** `_ai/*.md` — gegenereerd.
2. Verzin of wijzig **nooit** een Tarifit-woord. Alleen bestaande vormen; ontbreekt iets, vraag het.
3. Draai na de wijziging **`make build`** en **`make check`**.
4. Faalt `make check`, **fix de bron** (niet het gegenereerde bestand) en draai opnieuw.
5. Commit pas als `make check` slaagt.

## Canonieke bron per wijziging
| Wijzigen… | Bewerk dit | Regenereert | Sync-let-op |
|---|---|---|---|
| Een **woord** | `assets/woordenlijst/woordenlijst.csv` | `_ai/woordenlijst.md`, `_ai/index.md` | NL+EN in één bestand → automatisch synchroon |
| Een **les** | `nl/cursus.html` **én** `en/course.html` | `_ai/cursus.md` | Tarifit in beide identiek; alleen uitleg-taal verschilt |
| **Grammatica** | `nl/uitleg.html` **én** `en/grammar.html` | `_ai/grammatica.md` | idem |
| **Oefeningen** | `assets/oefeningen/exercises-nl.json` **én** `-en.json` | (niets) | beide talen gelijk opbouwen |

## Concreet
- **Woord:** pas de rij in `woordenlijst.csv` aan (`Berbers, Nederlands, Engels, niveau, woordsoort,
  anki_tag`). Tarifit uit een bestaande/eigen lijst, nooit verzonnen. `make build` → `make check` →
  commit.
- **Les / grammatica:** pas NL én EN aan; Tarifit-voorbeelden in beide exact gelijk. `make build` →
  `make check` (de pariteitscheck waarschuwt als NL/EN uit elkaar lopen) → commit.
- **Oefening:** pas `exercises-nl.json` en `exercises-en.json` allebei aan, test de oefenpagina,
  commit.

## Waarom dit standhoudt, ook bij iemand anders
- Elk gegenereerd bestand begint met "NIET met de hand bewerken".
- Bewerkt iemand tóch een `_ai/`-bestand, dan regenereert de pre-commit hook het en **faalt de
  commit**.
- `CLAUDE.md` zorgt dat elke Claude Code-sessie deze regels automatisch meekrijgt.

> Werk je met een oude kopie? `git pull` eerst. De waarheid staat in de canonieke bronnen hierboven.
