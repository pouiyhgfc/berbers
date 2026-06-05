# CLAUDE.md — Tarifit-cursus (berbers)

Statische, tweetalige (NL/EN) taalcursus-website. Geen buildstap voor de site zelf; afgeleide
AI-context wordt met Python-generatoren gemaakt. Dit bestand stuurt elke Claude Code-sessie. Houd
het kort.

## Hardste regel
Verzin of wijzig **NOOIT** een Tarifit-woord of -vorm. Gebruik alleen bestaande vormen uit de
canonieke bronnen. Ontbreekt een vorm, **vraag het** — gok niet. Scripts die een verwachte
Tarifit-token niet vinden, falen met een foutmelding (niet aanvullen).

## Bron-model (single source of truth)
| Inhoud | Canonieke bron (bewerk hier) | Afgeleide (gegenereerd, niet met de hand) |
|---|---|---|
| Woorden | `assets/woordenlijst/woordenlijst.csv` (NL+EN kolommen) | `_ai/woordenlijst.md`, Anki-export, EN-woordenlijstweergave |
| Lessen | `nl/cursus.html` + `en/course.html` | `_ai/cursus.md` |
| Grammatica | `nl/uitleg.html` + `en/grammar.html` | `_ai/grammatica.md` |
| Oefeningen | `assets/oefeningen/exercises-nl.json` + `-en.json` | — |
| Oefen-AI-manifest | sjabloon in `_project/docs/conventies.md` | `_ai/index.md` |

`_ai/*.md` zijn context voor een taaloefen-chatbot en zijn volledig gegenereerd. Bewerk ze nooit
met de hand (ze beginnen met een banner). Bewerk de bron en draai `make build`.

## CSV-schema
6 kolommen met koprij: `Berbers,Nederlands,Engels,niveau,woordsoort,anki_tag`. Parsers mappen op
**kolomnaam**, niet op vaste index.

## NL/EN-pariteit
De Tarifit-tekst in `nl/cursus.html` en `en/course.html` (idem `uitleg`/`grammar`) hoort identiek te
zijn; alleen de uitleg-taal verschilt. `make check` bewaakt dit.

## Werkwijze
1. Bewerk de canonieke bron.
2. `make build` (regenereert `_ai/`).
3. `make check` (drift + NL/EN-pariteit).
4. Commit pas als `make check` slaagt.
Voor het maken van wijzigingen, volg `WIJZIGINGEN.md`.

## Mapstructuur
- Root + `nl/ en/ assets/` = de gepubliceerde site.
- `_ai/` = gegenereerde AI-context.
- `_project/` = werkplaats (scripts, docs, archief, bronnen, generated); nooit door de site geladen,
  uitgesloten via `.vercelignore`.
