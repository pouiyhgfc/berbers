# Fase 3 — Generatoren, guardrail & drift-borging

**Doel.** `_ai/` wordt volledig gegenereerd uit CSV + HTML, één commando regenereert alles, controles
voorkomen dat een afgeleide achterloopt óf dat NL/EN uit elkaar lopen, en `CLAUDE.md` +
`WIJZIGINGEN.md` leggen de werkwijze vast. **Vereist:** fase 1 afgerond.

## Sessie-setup
- **Model:** `/model opus` voor stap 3.1–3.4 (generatoren + Tarifit round-trip-check — hoogste
  risico). Daarna `/model sonnet` voor 3.5–3.8 (boilerplate en tekst).
- **Token-aanpak:** generatoren lopen via Python over de bestanden; lees in de chat alleen de
  testuitvoer. Eén HTML-bestand past binnen de context — geen extra context-uitbreiding nodig. Begin
  deze fase met een vers tokenvenster; het is de zwaarste.
- **Harde regel:** een generator is een *verliesloze herformatteerder*. Hij leest bestaande tekst en
  zet die om; synthetiseert nooit Tarifit. Mist een verwachte token, dan faalt hij.

## Stap 3.1 — `_ai/woordenlijst.md` ← CSV
`_project/scripts/gen_woordenlijst_md.py`: lees de CSV naam-gebaseerd, groepeer op `niveau`, emit per
niveau een tabel `| Tarifit | Nederlands | Engels | Soort |` met een **berekend** totaal. Banner
bovenaan (zie 3.4). Elke Tarifit-vorm komt letterlijk uit kolom 0.

## Stap 3.2 — `_ai/cursus.md` en `_ai/grammatica.md` ← HTML
1. **Inspecteer eerst** de HTML van `nl/cursus.html`, `nl/uitleg.html` (en `en/course.html`,
   `en/grammar.html`): welke elementen dragen titels, secties, voorbeeldzinnen, en welke class markeert
   Tarifit (bv. `class="tar"`)? Leg het patroon vast in `_project/docs/conventies.md`. **Schrijf nog
   geen generator** — stop en toon het patroon.
2. **Schrijf de extractors** (`gen_cursus_md.py`, `gen_grammatica_md.py`) die de markdown reproduceren
   in de bestaande kopstructuur; behoud Tarifit letterlijk; banner bovenaan.
3. **Round-trip-check (verplicht):** vergelijk de Tarifit-tokenverzameling uit de bron-HTML met die in
   de gegenereerde markdown; faal bij verschil.
```python
src = set(tarifit_tokens_uit_html(html))
out = set(tarifit_tokens_uit_md(generated_md))
assert src == out, f"Tarifit-mismatch: alleen bron={src-out}; alleen output={out-src}"
```
> Genereer primair uit de NL-HTML (de `_ai/`-bestanden zijn Nederlandstalig).

## Stap 3.3 — `_ai/index.md` ← sjabloon + berekende cijfers
Sjabloon in `_project/docs/conventies.md` met placeholders; `gen_index_md.py` vult de cijfers door te
tellen in de bron (CSV-rijen, `## Les`-koppen, `## Hoofdstuk`-koppen). Banner bovenaan; de harde
Tarifit-regel en tabellen uit het sjabloon.

## Stap 3.4 — Banner in elk gegenereerd bestand
Elke generator schrijft als eerste regels:
```
<!-- AUTO-GEGENEREERD uit <bron> door _project/scripts/<script>.py
     NIET met de hand bewerken. Bewerk de bron en draai `make build`. Zie WIJZIGINGEN.md. -->
```

## Stap 3.5 — Makefile + twee controles  (`/model sonnet`)
```make
.PHONY: build check parity
build:
	python3 _project/scripts/gen_woordenlijst_md.py
	python3 _project/scripts/gen_cursus_md.py
	python3 _project/scripts/gen_grammatica_md.py
	python3 _project/scripts/gen_index_md.py
check: build parity
	@git diff --exit-code _ai/ || (echo "FOUT: _ai/ liep achter op de bron." && exit 1)
parity:
	python3 _project/scripts/check_parity.py
```
`check_parity.py`: vergelijk de Tarifit-tokenverzamelingen tussen `nl/cursus.html` ↔ `en/course.html`
en `nl/uitleg.html` ↔ `en/grammar.html`; meld het verschil en faal bij mismatch.
> **Eerst kalibreren:** draai `check_parity.py` één keer op de huidige bestanden. Zijn er nu al
> bewuste verschillen, zet de check dan eerst op *waarschuwen* en maak hem hard zodra NL/EN gelijk zijn.

## Stap 3.6 — Drift-borging
`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: regen-en-check
        name: Regenereer _ai/ en controleer drift + NL/EN-pariteit
        entry: make check
        language: system
        pass_filenames: false
        files: '^(assets/woordenlijst/woordenlijst\.csv|nl/.*\.html|en/.*\.html)$'
```
`pip install pre-commit && pre-commit install`. Een handmatige bewerking van een `_ai/`-bestand wordt
bij de commit geregenereerd → de commit faalt → oude werkwijze geblokkeerd. Voeg ook
`.github/workflows/check-generated.yml` toe die `make check` bij elke push/PR draait.

## Stap 3.7 — Guardrail: `CLAUDE.md` + `WIJZIGINGEN.md`
Werk de root-`CLAUDE.md` bij (gebruik de meegeleverde versie als basis): bron-model, mapstructuur,
CSV-schema (6 kolommen met koprij, naam-gebaseerd), werkwijze ("bewerk de bron → `make build` →
commit; nooit `_ai/` met de hand"), de harde Tarifit-regel, en een verwijzing naar `WIJZIGINGEN.md`.
Houd hem < 200 regels (hij laadt elke sessie). Plaats `WIJZIGINGEN.md` in de root.

## Stap 3.8 — Commit & merge
```bash
make build
git add -A
git commit -m "Fase 3: generatoren, banners, drift- + pariteitscheck, CLAUDE.md, WIJZIGINGEN.md"
git checkout main && git merge --no-ff herstructurering
```

## ✋ Einde plan — acceptatie
- `make build` regenereert alle `_ai/`-bestanden, elk met "niet met de hand bewerken"-banner.
- `make check` slaagt schoon en faalt bij achterlopende afgeleide óf NL/EN-Tarifit-verschil; de
  pre-commit hook blokkeert handmatige bewerking van gegenereerde bestanden.
- `CLAUDE.md` beschrijft de structuur; `WIJZIGINGEN.md` geeft het wijzigrecept.
- Geen Tarifit-vorm gewijzigd buiten een door jou goedgekeurde toevoeging aan de CSV.
