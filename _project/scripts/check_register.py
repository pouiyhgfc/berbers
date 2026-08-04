#!/usr/bin/env python3
"""
check_register.py — bewaakt canonieke spelling (plan/BOUWPLAN-CURSUS-UITVOERING.md §7).

Als bron/register-spelling.csv ontbreekt: print "register ontbreekt — waarschuwmodus" en
exit 0 (R3 geldt hier bewust niet — Fase 0 van het plan legt vast dat dit in
waarschuwmodus start totdat het register bestaat).

Schema van bron/register-spelling.csv (optioneel, header verplicht): `vorm,canoniek` — elke
rij zegt dat het token in `vorm` overal vervangen moet zijn door het token in `canoniek`.
Wordt `vorm` toch letterlijk aangetroffen (als los token, niet als substring) in
assets/zinnen/zinnen.csv (kolom tarifit), assets/woordenlijst/woordenlijst.csv (kolom
tarifit, variantenlijst gesplitst op " / ") of in de proza-backticks van bron/lessen/*.md
en bron/kaarten/*.md, dan is dat een fout met vindplaats. R1: dit script wijzigt nooit een
Tarifit-string, het meldt alleen.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _manifest import load_kaarten, load_lessen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER_CSV = REPO_ROOT / "bron" / "register-spelling.csv"
ZINNEN_CSV = REPO_ROOT / "assets" / "zinnen" / "zinnen.csv"
WOORDENLIJST_CSV = REPO_ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"
LESSEN_DIR = REPO_ROOT / "bron" / "lessen"
KAARTEN_DIR = REPO_ROOT / "bron" / "kaarten"

_TOKEN_RE = re.compile(r"[^\s.,;:!?()«»„“”\"]+")


def main() -> int:
    if not REGISTER_CSV.exists():
        print("register ontbreekt — waarschuwmodus")
        return 0

    with REGISTER_CSV.open(encoding="utf-8-sig", newline="") as f:
        register = list(csv.DictReader(f))

    fouten: list[str] = []

    with ZINNEN_CSV.open(encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            tokens = {t.strip("-").lower() for t in _TOKEN_RE.findall(row.get("tarifit", ""))}
            for r in register:
                if r["vorm"].lower() in tokens:
                    fouten.append(f"assets/zinnen/zinnen.csv regel {i}: niet-canonieke vorm '{r['vorm']}' (canoniek: '{r['canoniek']}')")

    with WOORDENLIJST_CSV.open(encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            varianten = {v.strip().lower() for v in row.get("tarifit", "").split(" / ")}
            for r in register:
                if r["vorm"].lower() in varianten:
                    fouten.append(f"assets/woordenlijst/woordenlijst.csv regel {i}: niet-canonieke vorm '{r['vorm']}' (canoniek: '{r['canoniek']}')")

    manifests = (load_lessen(LESSEN_DIR) if LESSEN_DIR.exists() else []) + load_kaarten(KAARTEN_DIR)
    for m in manifests:
        for regelnr, regel in enumerate(m.body.split("\n"), start=m.body_start_line):
            for bt in re.finditer(r"`([^`]+)`", regel):
                tokens = {t.strip("-").lower() for t in _TOKEN_RE.findall(bt.group(1))}
                for r in register:
                    if r["vorm"].lower() in tokens:
                        fouten.append(f"{m.path.name} regel {regelnr}: niet-canonieke vorm '{r['vorm']}' (canoniek: '{r['canoniek']}')")

    if fouten:
        print(f"FOUT — {len(fouten)} niet-canonieke vorm(en):", file=sys.stderr)
        for msg in fouten:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    print(f"OK — register.csv ({len(register)} regel(s)), 0 fouten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
