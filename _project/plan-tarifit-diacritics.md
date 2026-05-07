# Plan: Tarifit-speciale tekens gelijkmatiger weergeven

## Waarom het “hinkt” (kleiner/groter, streepjes scheef)

1. **Italic op Tarifit** — cursieve glyphs zijn geneigd; **combinerende tekens** (streepje onder/boven, puntje onder) worden meegetrokken. Dan lijken `ḏ` / `ṯ` / `ə`-achtige vormen anders dan gewone letters.
2. **-font-synthesis** — als de browser **nep-cursief** of **nep-vet** tekent, kloppen metrics niet tussen base letter en mark. In CSS: `font-synthesis: none` op `.tar` en op woordenlijstwoorden (al gedaan).
3. **Fallback-font** — ontbreekt een glyph in **Literata**, dan pakt de browser **Georgia** of systeemfont; die hebben **andere x-height** → “de ene letter lijkt kleiner”.
4. **NFC vs NFD** — hetzelfde schriftelijk woord kan als **één codepoint** (bijv. voorgecomposeerd) of als **letter + combinerende mark** staan. Die twee routes tekenen niet identiek.
5. **Variantvormen** — zeldzame IPA/Berber-tekenen staan soms in een **ander lettertype** in de fallback-keten.

## Aanpak (laag voor laag)

| Prio | Actie | Werk |
|------|--------|------|
| A | CSS: geen **faux** italic/bold op Tarifit; `text-rendering: optimizeLegibility` | Gedaan op `.tar` en `.wl-word`. |
| B | Woordenlijst: Tarifit **rechtop** (geen italic), **font-weight 500** | Gedaan — minder “dikgedrukt”. |
| C | Data: CSV/normalisatie **Unicode NFC** vóór publicatie | Script: alle entries door `unicodedata.normalize('NFC', …)` (bijv. in `_project` build of eenmalige audit). |
| D | **Glyph-audit** — zoek in `woordenlijst.csv` naar codepoints die vaak fallback geven; evt. **Literata-uitbreiding** of secundair font alleen voor `.tar` (bijv. “Source Serif 4” als tweede keuze vóór Georgia). | Handmatig of klein Python-rapport: welke chars komen voor, test in browser. |
| E | **Precomposed waar mogelijk** — gebruik in bron waar kan **één** teken (bijv. U+1E0F ḏ) i.p.v. d + combinerende underline (minder verschil tussen engines). | Editor/ingest-regel. |

## Niet doen

- Geen “hacks” met `transform: scale` per letter.
- Geen verplichte image/SVG voor gewone woordenlijsttekst.

## Vervolg

1.draai NFC-normalisatie op `assets/woordenlijst/woordenlijst.csv` en diff bekijken.  
2. Visuele steekproef op 20 woorden met `ḥ`, `ɣ`, `ř`, onderstreep-combinaties.  
3. Pas zo nodig `--font-serif`-stack aan voor `.tar` / `.wl-word` alleen.
