# Inventaris — Fase 0 (2026-06-05)

Niet-destructief. Niets verplaatst of verwijderd.

---

## Geverifieerde feiten

| Feit | Waarde |
|---|---|
| CSV rijen | 1782 (geen koprij — rij 0 is al data) |
| CSV kolommen | 6 |
| CSV rij 0 | `['a / wa / waḏ', 'Deze', 'This', 'A1', 'vnw_aanw', 'tarifit::cefr::A1 tarifit::woordsoort::vnw_aanw']` |
| CSV heeft koprij? | **Nee** — eerste rij is al een woord |
| Engine laadt exercises van | `/assets/oefeningen/exercises-<lang>.json` (cursus.js:469) |
| `assets/cursus/exercises-nl.json` vs `assets/oefeningen/exercises-nl.json` | **VERSCHILLEND** — cursus: 311 vragen / oefeningen: 339 vragen (beide 36 lessen) |
| `assets/cursus/exercises-en.json` vs `assets/oefeningen/exercises-en.json` | **VERSCHILLEND** — cursus: 311 vragen / oefeningen: 339 vragen (beide 36 lessen) |
| `nl/woordenlijst.html` laadt | `/assets/woordenlijst/woordenlijst.csv` |
| `en/wordlist.html` laadt | `/assets/woordenlijst/woordenlijst-engels-import.csv` (afwijkend!) |
| `_ai/index.md` noemt | 1848 woorden |
| `_ai/woordenlijst.md` datarijen | 1847 |
| CSV datarijen | 1782 |
| **Drift** | `_ai/` heeft 65 woorden meer dan de CSV |
| `CLAUDE.md` in root | **BESTAAT NIET** (nog te maken in een latere fase) |

---

## Wees-tabel

| Pad | Type | Verwezen door | Oordeel |
|---|---|---|---|
| `tweaks-app.jsx` | JSX-component | — | **WEES** |
| `tweaks-panel.jsx` | JSX-component | — | **WEES** |
| `extract.py` | Python-script | — | **WEES** |
| `serve.ps1` | PowerShell-script | Alleen in helpboodschap (HTML-string, geen import) | **Functioneel wees** |
| `woordenlijst-min.txt` | Tekstbestand | — | **WEES** |
| `differences.md` | Markdown | — | **WEES** |
| `duplicaten-check.xlsx` | Excel-werkblad | — | **WEES** |
| `gh-check.xlsx` | Excel-werkblad | — | **WEES** |
| `spellingcheck-j-y-z-g.xlsx` | Excel-werkblad | — | **WEES** |
| `woordenlijst-engels-import.csv` | CSV | `en/wordlist.html` (actief in gebruik) | **GEEN WEES** — wordt geretireerd na reconciliatie in fase 2 |

---

## Werkplaatsmateriaal in `_project/`

Al het volgende staat in `_project/` (root-niveau, nog niet in submappen geordend):

| Bestand | Aard |
|---|---|
| `grammatica-verificatie.md` | Analyse-document |
| `izran-zinnen-analyse.md` | Analyse-document |
| `nieuwe-woorden-izran.csv` | Mogelijk staged vocabulaire voor de CSV (zie fase 1) |
| `normalize_woordenlijst_csv.py` | Hulpscript |
| `plan-tarifit-diacritics.md` | Plan-document |
| `restructure_i18n.py` | Hulpscript |
| `review-uitleg.md` | Review-document |
| `supabase-setup.md` | Opzet-document (externe service) |
| `woord-audit.md` | Audit-document |
| `woord-toevoegen-prompt.md` | Prompt-sjabloon |
| `cursus-rewrite-fase-a-plan.md` | Plan-document |
| `_apply-spelling-fixes.py` | Hulpscript |
| `_audit-script.py` | Hulpscript |
| `_boek-tekst.txt` | Brontekst |
| `_build-oefeningen-html.py` | Hulpscript |
| `_check-cursus-csv.py` | Hulpscript |
| `_classify-overrides.csv` | Data-override |
| `_classify-words.py` | Hulpscript |
| `_fix-lesson-nav.py` | Hulpscript |
| `_gen_exercises_06_36.py` | Hulpscript |
| `_handoff.md` | Handoff-document |
| `_oefeningen-blocks.txt` | Tekstbestand |
| `_split-oefeningen.py` | Hulpscript |
| `_sync_exercises_json.py` | Hulpscript |

---

## Driftnotities

1. **CSV heeft geen koprij.** Het plan veronderstelt dat er een koprij wordt toegevoegd (fase 3). Parsers moeten nu op index mappen; na toevoeging koprij op kolomnaam.

2. **`_ai/` telt 65 woorden meer dan de CSV.** `_ai/index.md` noemt 1848, `_ai/woordenlijst.md` heeft 1847 datarijen; de CSV heeft 1782 rijen. De `_ai/`-bestanden zijn vermoedelijk gegenereerd uit een oudere/uitgebreidere versie van de CSV of handmatig aangevuld.

3. **`CLAUDE.md` bestaat niet in de root.** Het plan voorziet dit als guardrail. Moet worden aangemaakt in fase 3.

4. **`en/wordlist.html` leest een apart import-CSV** (`woordenlijst-engels-import.csv`) in plaats van de hoofd-CSV. Dit veroorzaakt mogelijke inhoudsdrift tussen de NL- en EN-woordenlijstpagina's. Wordt geadresseerd in fase 2.

5. **Twee sets exercise-JSON's.** `assets/cursus/` bevat oudere kopieën (311 vragen); `assets/oefeningen/` bevat de actieve versie (339 vragen). Engine laadt enkel uit `assets/oefeningen/`. De `assets/cursus/`-versies zijn verouderde kopieën.

6. **`serve.ps1` functioneel wees.** Alleen vermeld in een helpboodschap in HTML, niet geladen als script.
