# Fase 1 — Reconciliatie (licht; CSV is de waarheid)

**Doel.** Vaststellen wat er verschilt tussen dubbele bronnen, vóór fase 2 iets retireert. Omdat de
woorden in `woordenlijst.csv` de waarheid zijn (NL en EN correct), is de woord-reconciliatie licht:
de CSV wint. De echte beslissing zit bij de dubbele oefen-JSON.

## Sessie-setup
- **Model:** `/model sonnet`. Scripts vergelijken; jij beslist over de oefeningen.
- **Token-aanpak:** rapporten naar `_project/generated/`; open ze in je editor, niet in de chat.
- **Harde regel:** `woordenlijst.csv` is de enige bron van waarheid voor woorden. Verzin/wijzig geen
  Tarifit-vorm.
- **Eén sessie** met een korte stop voor jouw beoordeling.

## Stap 1.1 — Woorden: CSV leidend (advisory)
Schrijf `_project/scripts/recon_woorden.py` → `_project/generated/recon-woorden.md` met één lijst:
**woorden die nu in `_ai/woordenlijst.md` staan maar niet in de CSV** (genormaliseerd vergelijken op
de Tarifit-vorm, zonder spelling te wijzigen). Dit is een **kijklijst, geen gate**: zie je er een
woord dat je tóch wilt, dan voeg je dat zelf aan de CSV toe (jij levert de vorm). Fase 3 regenereert
verder gewoon uit de CSV.

> Losse staged/analyse-bestanden in `_project/` (zoals `nieuwe-woorden-izran.csv`,
> `grammatica-verificatie.md`, `izran-zinnen-analyse.md`) zijn **niet van belang** voor dit plan; ze
> worden in fase 2 gewoon gearchiveerd. Geen aparte reconciliatie nodig.

## Stap 1.2 — Oefeningen: `assets/cursus/` ↔ `assets/oefeningen/` (de echte keuze)
De engine laadt alleen `/assets/oefeningen/`; de `/assets/cursus/`-kopie verschilt. Schrijf
`recon_oefeningen.py` → `_project/generated/recon-oefeningen.md`: per taal/les welke items alleen in
de ongebruikte kopie staan. **Jij beslist:** niets unieks → in fase 2 naar archief; wel iets unieks →
eerst toevoegen aan de gebruikte versie.

## Stap 1.3 — Engelse import-CSV (sanity-check)
Schrijf `recon_engels.py` → `_project/generated/recon-engels.md`: Tarifit-sleutels die alleen in
`woordenlijst-engels-import.csv` staan en niet in de canonieke CSV. Omdat de CSV de waarheid is, mag
het import-CSV daarna naar archief; deze lijst is enkel een laatste check.

## Stap 1.4 — Commit
```bash
git add _project/scripts/recon_*.py _project/generated/recon-*.md
git commit -m "Fase 1: reconciliatie-rapporten (CSV leidend; niet-destructief)"
```

## ✋ GATE naar fase 2
De rapporten bestaan, je hebt de oefeningen-keuze gemaakt en de kijklijsten (woorden, engels)
bekeken. Niets verplaatst/verwijderd. Stop; open fase 2 met `/clear`.
