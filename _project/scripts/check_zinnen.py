"""
Validator: assets/zinnen/zinnen.csv  — aangehaakt op `make check` (target `zinnen`).

Controleert de canonieke zinnen-CSV tegen `_ai/grammatica.md` en zichzelf. Faalt hard (exit 1)
bij fouten die de zinnenbank onbruikbaar of onbetrouwbaar maken; waarschuwt (exit 0) bij
zaken die legitiem kunnen zijn maar aandacht verdienen.

Faalt (exitcode 1) bij:
  - een `hoofdstuk`-waarde die niet als `## Hoofdstuk`- of `### X.Y`-kop in
    `_ai/grammatica.md` voorkomt (typefout in het §-nummer maakt de zin onvindbaar);
  - een `tarifit`-cel die een niet-geëscapete `|` bevat;
  - een dubbele `id:`-tag in de `tags`-kolom (zelfde id twee keer — migratie- of plakfout).

Waarschuwt (exitcode 0) bij:
  - een duplicaat: dezelfde `tarifit`-zin twee keer (meldt beide regelnummers — kan legitiem
    zijn: korte zinnen komen in een echt corpus op meerdere pagina's voor);
  - een zin zonder `hoofdstuk` (belandt in de restgroep, wordt zelden geoefend);
  - een zin zonder `gloss`.

Draaien:  python _project/scripts/check_zinnen.py
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "assets/zinnen/zinnen.csv"
GRAMMATICA_MD = ROOT / "_ai/grammatica.md"

_HOOFDSTUK_KOP_RE = re.compile(r"^#{2,3}\s+Hoofdstuk\s+(\d+)\b", re.MULTILINE)
_SECTIE_KOP_RE = re.compile(r"^###\s+(\d+\.\d+)\b", re.MULTILINE)
_ID_TAG_RE = re.compile(r"id:([^;]+)")
_UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")


def geldige_hoofdstukken() -> set[str]:
    if not GRAMMATICA_MD.exists():
        sys.exit(f"FOUT: {GRAMMATICA_MD.relative_to(ROOT)} ontbreekt — draai eerst `make build`.")
    text = GRAMMATICA_MD.read_text(encoding="utf-8")
    geldig = set(_HOOFDSTUK_KOP_RE.findall(text))
    geldig |= set(_SECTIE_KOP_RE.findall(text))
    return geldig


def load_rows() -> list[dict]:
    if not CSV_PATH.exists():
        print(f"  LET OP: {CSV_PATH.relative_to(ROOT)} bestaat nog niet — niets te checken.")
        return []
    rows: list[dict] = []
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            tarifit = (row.get("tarifit") or "").strip()
            nl = (row.get("nl") or "").strip()
            en = (row.get("en") or "").strip()
            if not tarifit and not nl and not en:
                continue
            if tarifit == "tarifit":
                continue
            row["_regel"] = i
            rows.append(row)
    return rows


def main() -> None:
    rows = load_rows()
    geldig = geldige_hoofdstukken()

    fouten: list[str] = []
    waarschuwingen: list[str] = []

    tarifit_regels: dict[str, list[int]] = {}
    id_regels: dict[str, list[int]] = {}
    n_zonder_hoofdstuk = 0
    n_zonder_gloss = 0
    hoofdstuk_totaal: set[str] = set()

    for row in rows:
        regel = row["_regel"]
        tarifit = (row.get("tarifit") or "").strip()
        hoofdstukken = [h.strip() for h in (row.get("hoofdstuk") or "").split(";") if h.strip()]

        if _UNESCAPED_PIPE_RE.search(tarifit):
            fouten.append(f"regel {regel}: niet-geëscapete '|' in tarifit-cel: `{tarifit}`")

        if not hoofdstukken:
            n_zonder_hoofdstuk += 1
        for h in hoofdstukken:
            hoofdstuk_totaal.add(h)
            if h not in geldig:
                fouten.append(
                    f"regel {regel}: hoofdstuk '{h}' komt niet voor als kop in "
                    f"{GRAMMATICA_MD.relative_to(ROOT)}"
                )

        if not (row.get("gloss") or "").strip():
            n_zonder_gloss += 1

        tarifit_regels.setdefault(tarifit, []).append(regel)

        m = _ID_TAG_RE.search(row.get("tags") or "")
        if m:
            zid = m.group(1).strip()
            id_regels.setdefault(zid, []).append(regel)

    for zid, regels in id_regels.items():
        if len(regels) > 1:
            fouten.append(f"dubbele id '{zid}' op regels {regels}")

    for tarifit, regels in tarifit_regels.items():
        if len(regels) > 1:
            waarschuwingen.append(f"duplicaat-zin op regels {regels}: `{tarifit}`")
    if n_zonder_hoofdstuk:
        waarschuwingen.append(f"{n_zonder_hoofdstuk} zin(nen) zonder hoofdstuk")
    if n_zonder_gloss:
        waarschuwingen.append(f"{n_zonder_gloss} zin(nen) zonder gloss")

    print(f"{len(rows)} zinnen · {len(hoofdstuk_totaal)} hoofdstukken · {n_zonder_gloss} zonder gloss")

    if waarschuwingen:
        print("\nWAARSCHUWINGEN:")
        for w in waarschuwingen:
            print(f"  - {w}")

    if fouten:
        print("\nFOUTEN:")
        for f in fouten:
            print(f"  - {f}")
        sys.exit(f"\nFOUT: check_zinnen.py vond {len(fouten)} fout(en) — zie hierboven.")


if __name__ == "__main__":
    main()
