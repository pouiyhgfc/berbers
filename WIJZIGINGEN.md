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
| Een **les** | `nl/cursus.html` **én** `en/course.html` | `_ai/cursus.md`, `_ai/index.md` | Tarifit in beide identiek; alleen uitleg-taal verschilt |
| **Grammatica** | `nl/uitleg.html` **én** `en/grammar.html` | `_ai/grammatica.md`, `_ai/index.md` | idem |
| **Oefeningen** | `assets/oefeningen/exercises-nl.json` **én** `-en.json` | (niets) | beide talen gelijk opbouwen |
| Een **zin** | `assets/zinnen/zinnen.csv` | `_ai/zinnen.md`, `_ai/index.md` | NL+EN in één bestand → automatisch synchroon |

## Concreet
- **Woord:** pas de rij in `woordenlijst.csv` aan (kolommen `tarifit, nl, en, cefr, woordsoort,
  tags`). De Tarifit-vorm staat in kolom `tarifit` — uit een bestaande/eigen lijst, nooit verzonnen.
  `make build` → `make check` → commit.
- **Les / grammatica:** pas NL én EN aan; Tarifit-voorbeelden in beide exact gelijk. `make build` →
  `make check`. De round-trip-check faalt als een Tarifit-token uit de HTML niet in de gegenereerde
  markdown terugkomt; de pariteitscheck waarschuwt als NL/EN uit elkaar lopen. → commit.
- **Oefening:** pas `exercises-nl.json` en `exercises-en.json` allebei aan, test de oefenpagina,
  commit.
- **Zin:** een zin komt letterlijk uit het boek of uit een geverifieerde bron; noteer de vindplaats
  in `bron`. Verzin nooit een zin, ook niet "als voorbeeld". `make build` → `make check` → commit.

## Spellingharmonisatie zinnenbank (2026-07-19)
`assets/zinnen/zinnen.csv` kwam uit boek-OCR en week op 205 tokens (376 zinnen) af van de
learntarifit-schrijfwijze in `woordenlijst.csv` (ontbrekende diakrieten: `r`→`ř`, `t`→`ṯ`,
`d`→`ḏ`, `h`→`ḥ`, `s`→`ṣ`, `z`→`ẓ`, `g`→`ɣ`, `c`→`ǧ`). Gedetecteerd met
`_project/scripts/check_spelling_zinnen.py`, per patroon beoordeeld door Idries, toegepast met
`_project/scripts/apply_spelling_zinnen.py --apply`. Rapporten (audit-trail):
`_project/rapporten/spelling-kandidaten.csv` (beoordeeld, alle 205 op `status=ja`),
`spelling-ambigu.csv` (10 dubbelzinnige tokens, 9 met de hand opgelost, `ɛri` bewust ongewijzigd),
`onbekende-tokens.csv` (werklijst voor woordenlijst-uitbreiding, apart traject).

## Bekende afwijking (pariteit)
`make parity` staat op *waarschuwen* omdat er nog één bewust/onbedoeld verschil is: het token `uyi`
(AS-vorm van `aɣi` "milk") staat alleen in `en/grammar.html`, niet in `nl/uitleg.html`. Los je dit op
(voeg het NL-voorbeeld toe of haal het EN-voorbeeld weg), zet dan `PARITY_MODE = "strict"` in
`_project/scripts/check_parity.py` zodat de check voortaan hard faalt bij elk NL/EN-verschil.

## Waarom dit standhoudt, ook bij iemand anders
- Elk gegenereerd bestand begint met "NIET met de hand bewerken".
- Bewerkt iemand tóch een `_ai/`-bestand, dan regenereert de pre-commit hook het en **faalt de
  commit** (`git diff --exit-code _ai/`).
- `CLAUDE.md` zorgt dat elke Claude Code-sessie deze regels automatisch meekrijgt.
- De GitHub-workflow `check-generated.yml` draait dezelfde `make check` bij elke push/PR.

> Werk je met een oude kopie? `git pull` eerst. De waarheid staat in de canonieke bronnen hierboven.
