#!/usr/bin/env python3
"""
gen_ankers.py — voegt §-ankers toe aan nl/uitleg.html en en/grammar.html
(plan/BOUWPLAN-CURSUS-UITVOERING.md §4.1).

Elke <h2>/<h3> waarvan de tekst matcht op ^(\\d+)\\.(\\d+)(?:\\.(\\d+))?\\s krijgt — als het
element nog geen id heeft — id="s{n1}-{n2}" resp. id="s{n1}-{n2}-{n3}". Bestaande ids
(de h1..h20 <section>-ankers) blijven onaangeroerd: dit script raakt alleen h2/h3 zonder
eigen id-attribuut aan. Idempotent: een tweede run wijzigt niets (elke toegevoegde id
bestaat dan al). Bewerkt alleen de opening-tag (id-attribuut invoegen); de rest van het
bestand blijft byte-gelijk (R1: geen Tarifit-string wordt aangeraakt).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOELEN = [REPO_ROOT / "nl" / "uitleg.html", REPO_ROOT / "en" / "grammar.html"]

HEADING_RE = re.compile(r"<h([23])(\s[^>]*)?>(.*?)</h\1>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
NUM_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?\s")


def anker_id(niveau: str, tekst: str) -> str | None:
    m = NUM_RE.match(tekst.strip())
    if not m:
        return None
    n1, n2, n3 = m.group(1), m.group(2), m.group(3)
    if niveau == "3" and n3:
        return f"s{n1}-{n2}-{n3}"
    return f"s{n1}-{n2}"


def verwerk(pad: Path) -> tuple[int, list[str]]:
    html = pad.read_text(encoding="utf-8")
    toegevoegd: list[str] = []

    def vervang(m: re.Match) -> str:
        niveau, attrs, inner = m.group(1), m.group(2) or "", m.group(3)
        if re.search(r"\bid\s*=", attrs):
            return m.group(0)  # heeft al een id: onaangeroerd laten
        tekst = TAG_RE.sub("", inner)
        aid = anker_id(niveau, tekst)
        if aid is None:
            return m.group(0)
        toegevoegd.append(aid)
        return f'<h{niveau} id="{aid}"{attrs}>{inner}</h{niveau}>'

    nieuw = HEADING_RE.sub(vervang, html)
    if nieuw != html:
        pad.write_text(nieuw, encoding="utf-8")
    return len(toegevoegd), toegevoegd


def main() -> int:
    totaal = 0
    alle_ankers: list[str] = []
    for pad in DOELEN:
        if not pad.exists():
            print(f"FOUT: {pad} ontbreekt", file=sys.stderr)
            return 1
        n, ankers = verwerk(pad)
        print(f"{pad.relative_to(REPO_ROOT)}: {n} anker(s) toegevoegd")
        totaal += n
        alle_ankers.extend(ankers)

    print(f"totaal toegevoegd: {totaal}")
    if alle_ankers:
        print("nieuwe ankers:", ", ".join(sorted(set(alle_ankers))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
