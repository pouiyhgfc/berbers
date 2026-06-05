"""
Fase 3, Stap 3.3 — Generator: _ai/index.md  <-  sjabloon + berekende cijfers

Het sjabloon (statische tekst: harde Tarifit-regel, afkortingen, schrijfwijze-tabel) staat
hieronder met placeholders. De cijfers worden BEREKEND uit de bron/afgeleiden:
  * {n_woorden}      = aantal geldige CSV-rijen (zelfde telling als gen_woordenlijst_md.py)
  * {n_lessen}       = aantal "## Les "-koppen in het gegenereerde _ai/cursus.md
  * {n_hoofdstukken} = aantal "## "-secties in het gegenereerde _ai/grammatica.md

Banner bovenaan (stap 3.4). Draaien:  python _project/scripts/gen_index_md.py
(Draai eerst gen_woordenlijst_md / gen_cursus_md / gen_grammatica_md, of `make build`.)
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "assets/woordenlijst/woordenlijst.csv"
CURSUS_MD = ROOT / "_ai/cursus.md"
GRAMMATICA_MD = ROOT / "_ai/grammatica.md"
OUT = ROOT / "_ai/index.md"

NIVEAU_ORDER = {"A1", "A2", "B1", "B2", "C1", "C2"}

BANNER = (
    "<!-- AUTO-GEGENEREERD uit sjabloon + berekende cijfers (CSV, _ai/cursus.md, _ai/grammatica.md)\n"
    "     door _project/scripts/gen_index_md.py\n"
    "     NIET met de hand bewerken. Bewerk de bron en draai `make build`. Zie WIJZIGINGEN.md. -->"
)

TEMPLATE = """\
# Tarifit Kennisbank — Instructies voor AI

## Wat is dit?
Een gestructureerde kennisbank voor de Tarifit (Riffijnse Berber) taal,
gebaseerd op Mourigh & Kossmann (2019), *An Introduction to Tarifiyt Berber*.

Schrijfwijze: Latijns-Berber alfabet (learntarifit-conventie).

## ⚠ HARDE REGEL — VERPLICHT NALEVEN
**Verzin NOOIT Tarifit-woorden.** Gebruik uitsluitend woorden die letterlijk
in `woordenlijst.md` staan. Als een woord er niet in staat, zeg dat dan
expliciet. Gok nooit op een Tarifit-spelling.

## Hoe te gebruiken
- **Woordvertaling** → `woordenlijst.md`
- **Lesuitleg + voorbeeldzinnen** → `cursus.md`
- **Grammaticaregels** → `grammatica.md`

Laad selectief: laad alleen de bestanden die relevant zijn voor de vraag.

## Afkortingen

| Code | Betekenis |
|------|-----------|
| ww | werkwoord |
| znw | zelfstandig naamwoord |
| vnw | voornaamwoord |
| bvnw | bijvoeglijk naamwoord |
| byw | bijwoord |
| voegw | voegwoord |
| A1–C2 | CEFR-niveau |
| M/V | mannelijk/vrouwelijk |
| ev/mv | enkelvoud/meervoud |
| FS | vrije staat (Free State) |
| AS | verbonden staat (Annexed State) |
| P | Perfectief (afgeronde actie) |
| I | Imperfectief (lopende actie) |

## Schrijfwijze — bijzondere letters

| Letter | Klank | Internet |
|--------|-------|---------|
| ṯ / ḏ | th in think / this | th |
| ḥ | harde h (Arabisch ح) | 7 |
| ɛ | ayn (Arabisch ع) | 3 |
| ɣ | zachte g (Arabisch غ) | gh |
| q | diepe k (Arabisch ق) | 9 |
| c | sj (sjaal) | ch/sh |
| ǧ | j in joke | dj |
| ř | rollende r (was l) | r |
| ṛ / ṣ / ṭ / ẓ | donkere variant | — |

## Inhoud

### Woordenlijst
{n_woorden} woorden → [woordenlijst.md](woordenlijst.md)

### Cursus ({n_lessen} lessen)
Alle {n_lessen} lessen in één bestand → [cursus.md](cursus.md)

### Grammatica ({n_hoofdstukken} hoofdstukken)
Alle {n_hoofdstukken} hoofdstukken in één bestand → [grammatica.md](grammatica.md)
"""


def count_woorden() -> int:
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        return sum(1 for r in csv.DictReader(f) if (r.get("cefr") or "").strip() in NIVEAU_ORDER)


def count_headings(path: Path, pattern: str) -> int:
    text = path.read_text(encoding="utf-8")
    return len(re.findall(pattern, text, re.MULTILINE))


def main() -> None:
    if not CURSUS_MD.exists() or not GRAMMATICA_MD.exists():
        raise SystemExit(
            "FOUT: _ai/cursus.md en/of _ai/grammatica.md ontbreken. "
            "Draai eerst gen_cursus_md.py en gen_grammatica_md.py (of `make build`)."
        )
    n_woorden = count_woorden()
    n_lessen = count_headings(CURSUS_MD, r"^## Les ")
    n_hoofdstukken = count_headings(GRAMMATICA_MD, r"^## ")

    body = TEMPLATE.format(
        n_woorden=n_woorden, n_lessen=n_lessen, n_hoofdstukken=n_hoofdstukken
    )
    OUT.write_text(BANNER + "\n\n" + body, encoding="utf-8")
    print(
        f"Geschreven: {OUT.relative_to(ROOT)}  "
        f"({n_woorden} woorden · {n_lessen} lessen · {n_hoofdstukken} hoofdstukken)"
    )


if __name__ == "__main__":
    main()
