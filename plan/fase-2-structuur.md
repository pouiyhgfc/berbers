# Fase 2 — Structuur, één-CSV-ontwerp en parser-fix

**Doel.** Doelstructuur toepassen, beide woordenlijsten op één canonieke CSV laten lezen, de
parser-bug verhelpen, werkplaats uit de deploy sluiten. **Vereist:** fase 1 afgerond.

## Sessie-setup
- **Model:** `/model sonnet` voor de hele fase (het werk is gelokaliseerd en goed te overzien).
- **Token-aanpak:** houd bij de parser-fix alleen `nl/woordenlijst.html`, `en/wordlist.html` en de
  CSV-koprij erbij; vraag een diff, geen volledige herschrijving.
- **Harde regel:** de parser-fix raakt kolom-mapping, niet de Tarifit-woorden (kolom 0). Een koprij
  toevoegen wijzigt geen data. Niets wordt hard verwijderd — alles naar `_project/archief/`.

## Stap 2.1 — Doelmappen + verplaatsen
```bash
mkdir -p _project/scripts _project/docs _project/archief _project/bronnen _project/generated
git mv tweaks-app.jsx tweaks-panel.jsx extract.py serve.ps1 _project/archief/ 2>/dev/null || true
git mv woordenlijst-min.txt differences.md _project/archief/ 2>/dev/null || true
git mv duplicaten-check.xlsx gh-check.xlsx spellingcheck-j-y-z-g.xlsx _project/archief/ 2>/dev/null || true
git mv "Izran Izran.pdf" "Boekonderzoek Tarifiyt Berber Taal.docx" _project/bronnen/ 2>/dev/null || true
git mv _project/*.py _project/scripts/ 2>/dev/null || true
git mv _project/supabase-setup.md _project/docs/ 2>/dev/null || true
# verouderde/analyse-docs en staged data → archief of generated, naar inzicht uit fase 0/1
git mv _project/cursus-rewrite-fase-a-plan.md _project/plan-tarifit-diacritics.md \
       _project/review-uitleg.md _project/grammatica-verificatie.md \
       _project/izran-zinnen-analyse.md _project/nieuwe-woorden-izran.csv _project/archief/ 2>/dev/null || true
git mv _project/woord-audit.md _project/generated/ 2>/dev/null || true
# dubbele ongebruikte oefen-JSON → archief (ALLEEN als recon-oefeningen.md "niets unieks" zei)
git mv assets/cursus/exercises-nl.json assets/cursus/exercises-en.json _project/archief/ 2>/dev/null || true
```
Controleer lokaal: `python3 -m http.server 8080` en klik door cursus/oefeningen/woordenlijst — geen
404's. Root bevat daarna alleen site- en configbestanden + `nl/ en/ assets/ _ai/ _project/`.

## Stap 2.2 — CSV-koprij
Voeg als eerste regel aan `assets/woordenlijst/woordenlijst.csv` toe:
```
Berbers,Nederlands,Engels,niveau,woordsoort,anki_tag
```
> Zet alleen een kopregel boven bestaande data; geen Tarifit-woord verandert.

## Stap 2.3 — Parser-fix (beide pagina's)
Bug: beide pagina's nemen 5 kolommen aan en lezen `niveau = r[2]`, maar de CSV heeft 6 kolommen en
`r[2]` is het Engelse woord; `rows.slice(1)` gooit zonder echte header de eerste rij weg. Map op
kolomnaam:
```js
const rows = parseCSV(text);
const header = rows[0].map(h => h.trim().toLowerCase());
const col = n => header.indexOf(n);
const iTar=col('berbers'), iNiveau=col('niveau'), iSoort=col('woordsoort'), iAnki=col('anki_tag');
const iMeaning = col(IS_EN ? 'engels' : 'nederlands');
ENTRIES = rows.slice(1)
  .filter(r => r[iTar]?.trim() && r[iMeaning]?.trim())
  .map(r => ({ word:r[iTar].trim(), meaning:r[iMeaning].trim(),
               niveau:(r[iNiveau]||'').trim(), soort:(r[iSoort]||'').trim(),
               ankiTag:(r[iAnki]||'').trim() /* + bestaande afgeleide velden */ }));
```
En in `en/wordlist.html` de fetch naar de canonieke CSV:
```js
fetch('/assets/woordenlijst/woordenlijst.csv', { cache:'no-cache' })
```
Acceptatie: CEFR- en woordsoort-filters werken op beide pagina's, Anki-tags kloppen, het eerste woord
(`a / wa / waḏ`) staat in de lijst; NL toont NL-betekenis, EN toont EN-betekenis uit dezelfde CSV.

## Stap 2.4 — Engelse import-CSV retireren
Alleen ná groen in `recon-engels.md`:
```bash
git mv assets/woordenlijst/woordenlijst-engels-import.csv _project/archief/
git mv assets/woordenlijst/woordenlijst_engels.xlsx _project/archief/
```

## Stap 2.5 — `.vercelignore`
```
_project/
*.xlsx
*.docx
*.pdf
```

## Stap 2.6 — Commit
```bash
git add -A
git commit -m "Fase 2: doelstructuur, één-CSV-ontwerp, parser-fix, .vercelignore"
```

## ✋ GATE naar fase 3
Site werkt lokaal; beide woordenlijsten lezen uit de canonieke CSV met correcte filters; root
opgeschoond; één bron per inhoudstype. Stop; open fase 3 met `/clear`.
