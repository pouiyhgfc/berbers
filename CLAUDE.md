# CLAUDE.md — Tarifit-cursus (berbers)

Statische, tweetalige (NL/EN) taalcursus-website. Geen buildstap voor de site zelf; afgeleide
AI-context wordt met Python-generatoren gemaakt. Dit bestand stuurt elke Claude Code-sessie. Houd
het kort.

## Hardste regel
Verzin of wijzig **NOOIT** een Tarifit-woord of -vorm. Gebruik alleen bestaande vormen uit de
canonieke bronnen. Ontbreekt een vorm, **vraag het** — gok niet. Generatoren die een verwachte
Tarifit-token niet terugvinden, falen met een foutmelding (ze vullen niets aan).

## Bron-model (single source of truth)
| Inhoud | Canonieke bron (bewerk hier) | Afgeleide (gegenereerd, niet met de hand) |
|---|---|---|
| Woorden | `assets/woordenlijst/woordenlijst.csv` (NL+EN-kolommen) | `_ai/woordenlijst.md` |
| Lessen | `nl/cursus.html` + `en/course.html` | `_ai/cursus.md` |
| Grammatica | `nl/uitleg.html` + `en/grammar.html` | `_ai/grammatica.md` |
| Oefeningen | `assets/oefeningen/exercises-nl.json` + `-en.json` | — |
| Zinnen | `assets/zinnen/zinnen.csv` (handmatig gecureerd, geattesteerd) | `_ai/zinnen.md`, `nl/en zinnen.html` + "Uit het boek"-blokken in cursus.html (laden runtime, niet gegenereerd) |
| AI-systeemprompt | sjabloon in `_project/scripts/gen_index_md.py` | `_ai/index.md` |

`_ai/*.md` zijn context voor een taaloefen-chatbot en zijn volledig gegenereerd. Bewerk ze nooit
met de hand (ze beginnen met een banner). Bewerk de bron en draai `make build`.

De kolommen `les`/`hoofdstuk` in `zinnen.csv` zijn deels machinaal geclassificeerd (tag `auto` in
`tags`, PLAN-ZINNEN-WEBSITE.md fase 3.1) op basis van de `context`-tag uit de boek-OCR. Handmatige
correctie: waarde aanpassen én de `auto`-tag verwijderen — anders overschrijft een latere
classificatieronde hem weer.

## CSV-schema
6 kolommen met koprij: `tarifit,nl,en,cefr,woordsoort,tags`. Parsers mappen op **kolomnaam**, niet
op vaste index. De Tarifit-vorm staat in kolom `tarifit` en wordt letterlijk overgenomen.

## NL/EN-pariteit
De Tarifit-tekst in `nl/cursus.html` en `en/course.html` (idem `uitleg`/`grammar`) hoort identiek te
zijn; alleen de uitleg-taal verschilt. `make parity` bewaakt dit. **Status:** gekalibreerd op
*waarschuwen* — er is nog één bekend verschil (`uyi` staat alleen in `en/grammar.html`). Zet
`PARITY_MODE = "strict"` in `_project/scripts/check_parity.py` zodra de paren gelijk zijn.

## Werkwijze
1. Bewerk de canonieke bron.
2. `make build` (regenereert `_ai/`). Op een systeem zonder `python3`-binary: `make build PYTHON=python`.
3. `make check` (regenereert + drift-check + NL/EN-pariteit).
4. Commit pas als `make check` slaagt.
Voor het maken van wijzigingen, volg `WIJZIGINGEN.md`.

## Mapstructuur
- Root + `nl/ en/ assets/` = de gepubliceerde site.
- `_ai/` = gegenereerde AI-context.
- `_project/` = werkplaats (scripts, docs, archief, bronnen, generated); nooit door de site geladen,
  uitgesloten via `.vercelignore`.
