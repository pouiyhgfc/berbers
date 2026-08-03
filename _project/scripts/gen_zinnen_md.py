"""
Generator: _ai/zinnen.md  <-  assets/zinnen/zinnen.csv

Verliesloze herformatteerder: leest de canonieke zinnen-CSV naam-gebaseerd, groepeert op
grammatica-hoofdstuk (kolom `hoofdstuk`, § uit _ai/grammatica.md) en emit per hoofdstuk een
tabel. Elke Tarifit-zin komt LETTERLIJK uit kolom `tarifit`. De generator synthetiseert,
normaliseert of corrigeert NOOIT Tarifit — hij kopieert en escapet alleen.

Ontbreekt de CSV, dan wordt een leeg zinnen.md met alleen de kop geschreven, zodat
`make build` blijft werken terwijl de zinnenbank nog wordt opgebouwd.

CSV-schema (koprij verplicht, 8 kolommen):
    tarifit    de zin, letterlijk        (VERPLICHT)
    nl         Nederlandse vertaling     (nl OF en verplicht)
    en         Engelse vertaling         (nl OF en verplicht)
    gloss      morfeem-glossering        (optioneel, bv. "3SG:M-zitten in huis:AS")
    hoofdstuk  §-nummer(s) uit grammatica.md, meerdere met ';'  (bv. "4.1" of "4.1;3.4")
    les        lesnummer uit cursus.md   (optioneel)
    bron       vindplaats                (bv. "boek p. 52")
    tags       vrije labels met ';'      (optioneel, bv. "perfectief;negatie")

Draaien:  python _project/scripts/gen_zinnen_md.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "assets/zinnen/zinnen.csv"
OUT_PATH = ROOT / "_ai/zinnen.md"

VERPLICHT = {"tarifit", "nl", "en"}  # kolommen moeten bestaan; per rij: tarifit + (nl of en)
ONGESORTEERD = "Zonder hoofdstuk"

BANNER = (
    "<!-- AUTO-GEGENEREERD uit assets/zinnen/zinnen.csv "
    "door _project/scripts/gen_zinnen_md.py\n"
    "     NIET met de hand bewerken. Bewerk de bron en draai `make build`. "
    "Zie WIJZIGINGEN.md. -->"
)

KOP = """# Tarifit Zinnenbank

> **REGEL:** Dit zijn de ENIGE toegestane oefenzinnen. Gebruik ze letterlijk.
> Verzin nooit een zin, en pas een zin nooit aan "om hem passend te maken".
> Elke zin hier is geattesteerd: hij komt uit de bron die in kolom Bron staat.
> Staat een zin er niet, dan bestaat hij niet — zeg dat, en oefen met wat er wél is.

Gegroepeerd op grammatica-hoofdstuk (§ verwijst naar `grammatica.md`).
Totaal: {n} zinnen."""


def sorteersleutel(hoofdstuk: str) -> tuple:
    """Numeriek sorteren: 3.4 < 4.1 < 4.10 < 5. Niet-numeriek gaat achteraan."""
    if hoofdstuk == ONGESORTEERD:
        return (1, ())
    try:
        return (0, tuple(int(d) for d in hoofdstuk.split(".")))
    except ValueError:
        return (1, ())


def cell(value: str) -> str:
    """Maak een waarde veilig voor een markdown-tabelcel (escape pipe, normaliseer whitespace)."""
    return " ".join((value or "").split()).replace("|", "\\|") or "—"


def load_rows() -> list[dict]:
    if not CSV_PATH.exists():
        print(f"  LET OP: {CSV_PATH.relative_to(ROOT)} bestaat nog niet — lege zinnenbank.")
        return []
    rows: list[dict] = []
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = VERPLICHT - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"FOUT: zinnen.csv mist verplichte kolom(men): {sorted(missing)}")
        for i, row in enumerate(reader, start=2):
            tarifit = (row.get("tarifit") or "").strip()
            nl = (row.get("nl") or "").strip()
            en = (row.get("en") or "").strip()
            if not tarifit and not nl and not en:
                continue  # lege regel
            if not tarifit or not (nl or en):
                sys.exit(
                    f"FOUT: regel {i} mist tarifit of een vertaling (nl of en) — "
                    "repareer de CSV, ik vul niets aan."
                )
            if tarifit == "tarifit":
                print(f"  Overgeslagen: dubbele koprij op regel {i}.")
                continue
            rows.append(row)
    return rows


def build_markdown(rows: list[dict]) -> str:
    groepen: dict[str, list[dict]] = {}
    for row in rows:
        hoofdstukken = [h.strip() for h in (row.get("hoofdstuk") or "").split(";") if h.strip()]
        primair = hoofdstukken[0] if hoofdstukken else ONGESORTEERD
        groepen.setdefault(primair, []).append(row)

    out: list[str] = [BANNER, "", KOP.format(n=len(rows)), ""]

    if not rows:
        out.append("_Nog geen zinnen. Vul `assets/zinnen/zinnen.csv` en draai `make build`._")
        return "\n".join(out) + "\n"

    for hoofdstuk in sorted(groepen, key=sorteersleutel):
        entries = groepen[hoofdstuk]
        titel = hoofdstuk if hoofdstuk == ONGESORTEERD else f"§{hoofdstuk}"
        out.append(f"## {titel}  ({len(entries)})")
        out.append("")
        out.append("| Tarifit | Nederlands | Engels | Gloss | § | Bron |")
        out.append("|---------|------------|--------|-------|---|------|")
        for e in entries:
            # Kolom `tarifit` wordt LETTERLIJK overgenomen — alleen tabel-escaping.
            secties = "; ".join(
                f"§{h.strip()}" for h in (e.get("hoofdstuk") or "").split(";") if h.strip()
            )
            out.append(
                f"| `{cell(e['tarifit'])}` | {cell(e['nl'])} | {cell(e.get('en'))} | "
                f"{cell(e.get('gloss'))} | {secties or '—'} | {cell(e.get('bron'))} |"
            )
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    rows = load_rows()
    OUT_PATH.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Geschreven: {OUT_PATH.relative_to(ROOT)}  ({len(rows)} zinnen)")


if __name__ == "__main__":
    main()
