#!/usr/bin/env python3
"""
Normaliseer woordenlijst.csv naar Unicode NFC en rapporteer ongebruikelijke codepoints.

Gebruik:
  python _project/normalize_woordenlijst_csv.py           # alleen rapport + diff-count
  python _project/normalize_woordenlijst_csv.py --write  # overschrijf CSV

Na bewerken van de woordenlijst (aanbevolen vóór commit):
  python _project/normalize_woordenlijst_csv.py --write
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"


def nfc_cell(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def analyze_text(text: str) -> tuple[Counter[str], list[str]]:
    cats: Counter[str] = Counter()
    notes: list[str] = []
    seen_char: set[str] = set()
    for ch in text:
        if ch in seen_char:
            continue
        seen_char.add(ch)
        cat = unicodedata.category(ch)
        cats[cat] += 1
        cp = ord(ch)
        name = unicodedata.name(ch, "<geen naam>")
        if cat in ("Mn", "Mc", "Me"):
            notes.append(f"Combinerend: U+{cp:04X} {name} ({cat})")
        if cp < 32 and ch not in "\n\r\t":
            notes.append(f"Besturing: U+{cp:04X}")
        if 0xD800 <= cp <= 0xDFFF:
            notes.append(f"Surrogaat: U+{cp:04X}")
    return cats, sorted(notes)


def main() -> int:
    p = argparse.ArgumentParser(description="NFC-normaliseer woordenlijst.csv")
    p.add_argument(
        "--write",
        "-w",
        action="store_true",
        help="Schrijf genormaliseerde CSV terug naar bestand",
    )
    args = p.parse_args()

    if not CSV_PATH.is_file():
        print("Niet gevonden:", CSV_PATH, file=sys.stderr)
        return 1

    raw = CSV_PATH.read_text(encoding="utf-8")
    rows_in = list(csv.reader(raw.splitlines()))

    rows_out: list[list[str]] = []
    changed_cells = 0
    changed_rows = 0
    for row in rows_in:
        new_row = [nfc_cell(c) for c in row]
        if new_row != row:
            changed_rows += 1
            changed_cells += sum(1 for a, b in zip(row, new_row) if a != b)
        rows_out.append(new_row)

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerows(rows_out)
    full_after = buf.getvalue()

    print(f"Rijen: {len(rows_out)} | Rijen met minstens één cel gewijzigd door NFC: {changed_rows}")
    print(f"Aangepaste cellen: {changed_cells}")

    cats, notes = analyze_text(full_after)
    print("\nUnieke Unicode-categorieën (per uniek teken):")
    for cat, n in sorted(cats.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {cat}: {n}")
    if notes:
        print("\nOpmerkingen (max. 40 regels):")
        for line in notes[:40]:
            print(" ", line)
        if len(notes) > 40:
            print(f"  ... en {len(notes) - 40} meer")

    if args.write:
        CSV_PATH.write_text(full_after, encoding="utf-8")
        print("\nGeschreven:", CSV_PATH)
    else:
        print("\nDry-run: geen --write; gebruik --write om het bestand bij te werken.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
