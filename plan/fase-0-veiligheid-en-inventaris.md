# Fase 0 — Veiligheid & inventaris

**Doel.** Veilige uitgangspositie + volledig beeld van wat er in de repo staat. Niets wordt
verplaatst of verwijderd. Uitkomst: `_project/generated/inventaris.md`.

## Sessie-setup
- **Model:** `/model sonnet`. Licht werk: scripts draaien, kleine output lezen.
- **Token-aanpak:** laad geen grote bestanden in de chat; scripts schrijven naar
  `_project/generated/`, lees daar de samenvatting.
- **Harde regel:** raak geen Tarifit-inhoud aan. Deze fase leest en rapporteert alleen.
- **Eén sessie.** Stop bij de GATE; begin niet aan fase 1.

## Stap 0.1 — Branch en ankerpunt
```bash
git checkout -b herstructurering
git tag pre-herstructurering
```

## Stap 0.2 — Feiten verifiëren
Draai en plak de uitvoer in `_project/generated/inventaris.md` onder "Geverifieerde feiten":
```bash
mkdir -p _project/generated
python3 - <<'PY'
import csv
r=list(csv.reader(open('assets/woordenlijst/woordenlijst.csv',encoding='utf-8')))
print('CSV rijen:',len(r),'| kolommen:',len(r[0]),'| rij0:',r[0])
PY
grep -n "exercises-' + lang" assets/cursus/cursus.js
for l in nl en; do diff -q assets/cursus/exercises-$l.json assets/oefeningen/exercises-$l.json \
  && echo "$l identiek" || echo "$l VERSCHILLEND"; done
grep -n "fetch('/assets/woordenlijst" nl/woordenlijst.html en/wordlist.html
```
Verwacht: CSV 6 kolommen, geen header, ~1782 rijen; engine laadt alleen `/assets/oefeningen/`; de
`/assets/cursus/`-JSON's verschillen; `en/wordlist.html` leest het aparte import-CSV.

## Stap 0.3 — Wees-detectie
Tabel in `inventaris.md`: `pad | type | verwezen door | oordeel`.
```bash
for f in tweaks-app.jsx tweaks-panel.jsx extract.py serve.ps1 woordenlijst-min.txt differences.md \
         duplicaten-check.xlsx gh-check.xlsx spellingcheck-j-y-z-g.xlsx; do
  hits=$(grep -rl "$f" --include='*.html' --include='*.js' . 2>/dev/null | grep -v _project)
  echo "$f -> ${hits:-WEES}"
done
```
> `woordenlijst-engels-import.csv` is **wél** in gebruik (`en/wordlist.html`) — geen wees; wordt pas
> in fase 2 geretireerd na reconciliatie.

## Stap 0.4 — Werkplaats- en driftnotities
Noteer in `inventaris.md`:
- Losse analyse-/staged-bestanden in `_project/` (o.a. `grammatica-verificatie.md`,
  `izran-zinnen-analyse.md`, `nieuwe-woorden-izran.csv`) — werkplaatsmateriaal dat in fase 2 wordt
  geordend; `nieuwe-woorden-izran.csv` is mogelijk staged vocabulaire (zie fase 1).
- Drift: bestaande `CLAUDE.md` beschrijft mogelijk het oude 5-koloms schema / verkeerde aantallen;
  `_ai/index.md` en `_ai/woordenlijst.md` noemen ~1848 woorden tegenover ~1782 in de CSV.

## Stap 0.5 — Commit
```bash
git add _project/generated/inventaris.md
git commit -m "Fase 0: inventaris en wees-classificatie (niet-destructief)"
```

## ✋ GATE naar fase 1
`inventaris.md` bevat feiten, wees-tabel en driftlijst. Niets verplaatst/verwijderd. Stop hier;
open fase 1 met `/clear`.
