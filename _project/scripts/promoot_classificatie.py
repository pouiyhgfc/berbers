#!/usr/bin/env python3
"""Zet bron/aanlevering/woordenlijst-geclassificeerd.csv om naar de canonieke
assets/woordenlijst/woordenlijst.csv (header: tarifit,nl,en,cefr,woordsoort,thema,tags).

Mapping: cefr_nieuw->cefr, thema blijft, tags_nieuw->tags; cefr_oud/zekerheid vervallen.
Rijvolgorde blijft behouden. Regels die zelf een herhaalde koprij zijn (tarifit == "tarifit")
worden overgeslagen. Verzint of wijzigt geen Tarifit-string (R1/R2): kopieert alleen kolommen.
"""
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BRON = REPO_ROOT / "bron" / "aanlevering" / "woordenlijst-geclassificeerd.csv"
DOEL = REPO_ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"

BRON_KOLOMMEN = {"tarifit", "nl", "en", "cefr_oud", "woordsoort", "cefr_nieuw", "thema", "zekerheid", "tags_nieuw"}
DOEL_HEADER = ["tarifit", "nl", "en", "cefr", "woordsoort", "thema", "tags"]


def main() -> int:
    if not BRON.exists():
        print(f"FOUT: bronbestand ontbreekt: {BRON}", file=sys.stderr)
        return 1

    with BRON.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        ontbrekend = BRON_KOLOMMEN - set(reader.fieldnames or [])
        if ontbrekend:
            print(f"FOUT: bronbestand mist kolommen: {sorted(ontbrekend)}", file=sys.stderr)
            return 1
        rijen = list(reader)

    uitrijen = []
    for i, rij in enumerate(rijen, start=2):
        if rij["tarifit"] == "tarifit" and rij["nl"] == "nl":
            continue  # herhaalde koprij-als-data
        uitrijen.append({
            "tarifit": rij["tarifit"],
            "nl": rij["nl"],
            "en": rij["en"],
            "cefr": rij["cefr_nieuw"],
            "woordsoort": rij["woordsoort"],
            "thema": rij["thema"],
            "tags": rij["tags_nieuw"],
        })

    DOEL.parent.mkdir(parents=True, exist_ok=True)
    with DOEL.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DOEL_HEADER, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(uitrijen)

    print(f"OK — {len(uitrijen)} rijen geschreven naar {DOEL.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
